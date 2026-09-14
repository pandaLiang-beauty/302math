import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))

import db
import practice
import server
from fastapi import HTTPException


class ExamPracticeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path_patch = patch.object(db, 'DB_PATH', str(Path(self.temp.name) / 'study.db'))
        self.path_patch.start()
        conn = db.connect()
        db.init_db(conn)
        conn.close()

    def tearDown(self):
        self.path_patch.stop()
        self.temp.cleanup()

    def question(self, paper, year, number, chapter, point='', type_name='', level='基础'):
        conn = db.connect()
        try:
            row = conn.execute(
                'INSERT INTO questions(paper,year,number,qtype,chapter,point,type_name,level,stem_html,options_json,answer,solution_html) '
                'VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                (paper, year, number, 'choice', chapter, point, type_name, level,
                 '<p>测试题干</p>', json.dumps([{'key': 'A', 'text': '选项一'}]), 'A', '<p>保密解析</p>'),
            )
            conn.commit()
            return row.lastrowid
        finally:
            conn.close()

    def add_limits(self):
        origin = self.question('math2', 2020, 1, '函数、极限、连续', '无穷小量的比较')
        base = self.question('lilin880', 0, 7, '函数极限连续')
        advanced = self.question('lilin880', 0, 66, '函数极限连续', level='拓展')
        mixed = self.question('lilin880', 0, 27, '函数极限连续', level='综合')
        self.question('lilin880', 0, 6, '函数极限连续')  # Same chapter, different point.
        self.question('math1', 2020, 7, '函数极限连续', '无穷小量的比较')
        return origin, base, mixed, advanced

    def test_priority_papers_are_chronological_and_old_papers_remain_available(self):
        for year in (2019, 2026, 2022, 2020, 2025, 2023, 2021, 2024, 2027, 2008):
            self.question('math2', year, 1, '函数、极限、连续')
        self.question('math1', 2020, 1, '函数、极限、连续')
        rows = server.papers()
        self.assertEqual([p['year'] for p in rows[:7]], list(range(2020, 2027)))
        self.assertEqual([p['year'] for p in rows[7:]], [2027, 2019, 2008])
        self.assertTrue(all(p['total'] == 1 for p in rows))

    def test_exam_links_use_book_numbers_and_only_same_topic_880_exercises(self):
        origin, base, mixed, advanced = self.add_limits()
        result = server.chapter_practice(question_id=origin)
        self.assertEqual(result['topic']['id'], 'infinitesimals')
        self.assertEqual([p['id'] for p in result['problems']], [base, mixed, advanced])
        self.assertEqual([p['number'] for p in result['problems']], [7, 27, 66])
        self.assertTrue(all(p['paper'] == 'lilin880' for p in result['problems']))
        self.assertEqual((result['origin']['id'], result['origin']['year'], result['origin']['number']), (origin, 2020, 1))
        self.assertNotIn('answer', result['origin'])
        self.assertNotIn('solution_html', result['origin'])
        self.assertTrue(all('answer' not in p and 'solution_html' not in p for p in result['problems']))
        self.assertEqual(server.paper(2020)['problems'][0]['practice']['total'], 3)

    def test_whole_chapter_is_an_explicit_choice_and_keeps_the_return_question(self):
        origin, *_ = self.add_limits()
        result = server.chapter_practice(question_id=origin, chapter='limits')
        self.assertIsNone(result['topic'])
        self.assertEqual(result['progress']['total'], 4)
        self.assertEqual(result['origin']['id'], origin)

    def test_incorrect_source_tags_are_overridden_by_reviewed_exam_links(self):
        curvature = self.question('math2', 2026, 13, '多元函数微分学', '多元函数微分学的几何应用')
        expected = self.question('lilin880', 0, 121, '一元函数微分学及其应用')
        self.question('lilin880', 0, 390, '多元函数微分学及其应用')
        result = server.chapter_practice(question_id=curvature)
        self.assertEqual(result['topic']['id'], 'curvature')
        self.assertEqual([p['id'] for p in result['problems']], [expected])

        integral = self.question('math2', 2023, 20, '一元函数微分学', '导数与微分', '导数概念与杂项')
        expected = self.question('lilin880', 0, 476, '二重积分')
        result = server.chapter_practice(question_id=integral)
        self.assertEqual(result['chapter']['id'], 'double-integrals')
        self.assertEqual([p['id'] for p in result['problems']], [expected])

    def test_composite_question_can_switch_knowledge_points_and_keep_origin(self):
        origin = self.question('math2', 2024, 22, '矩阵的特征值与特征向量', '(未细分)')
        standard = self.question('lilin880', 0, 875, '二次型')
        common = self.question('lilin880', 0, 795, '线性方程组')
        first = server.chapter_practice(question_id=origin)
        second = server.chapter_practice(question_id=origin, topic='linear-common')
        self.assertEqual([p['id'] for p in first['problems']], [standard])
        self.assertEqual([p['id'] for p in second['problems']], [common])
        self.assertEqual(first['origin'], second['origin'])
        self.assertEqual([t['id'] for t in first['suggested_topics']], ['quadratic-standard', 'linear-common'])

    def test_practice_navigation_does_not_change_attempts_and_progress_stays_separate(self):
        origin, base, *_ = self.add_limits()
        server.attempt(server.Attempt(question_id=origin, result='wrong', reason='idea'))
        server.attempt(server.Attempt(question_id=base, result='correct'))
        for _ in range(2):
            practice_result = server.chapter_practice(question_id=origin)
            paper_result = server.paper(2020)
        self.assertEqual(practice_result['progress']['done'], 1)
        self.assertEqual(practice_result['progress']['correct'], 1)
        self.assertEqual(paper_result['problems'][0]['last'], 'wrong')
        self.assertEqual(server.papers()[0]['done'], 1)
        conn = db.connect()
        try:
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM attempts').fetchone()[0], 2)
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM type_progress').fetchone()[0], 0)
        finally:
            conn.close()

    def test_empty_topic_is_not_replaced_by_unrelated_exercises(self):
        origin = self.question('math2', 2020, 1, '函数、极限、连续', '无穷小量的比较')
        self.question('lilin880', 0, 6, '函数极限连续')
        result = server.chapter_practice(question_id=origin)
        self.assertEqual(result['problems'], [])
        self.assertEqual(result['topic']['id'], 'infinitesimals')

    def test_unknown_old_topic_falls_back_honestly_to_its_chapter(self):
        origin = self.question('math2', 2008, 1, '函数、极限、连续', '尚未细分的新知识点')
        self.question('lilin880', 0, 7, '函数极限连续')
        result = server.chapter_practice(question_id=origin)
        self.assertEqual(result['match'], 'chapter')
        self.assertEqual(result['suggested_topics'], [])
        self.assertEqual(result['progress']['total'], 1)

    def test_invalid_navigation_is_rejected(self):
        _, book, *_ = self.add_limits()
        for args, status in (
            ({'question_id': 9999}, 404), ({'question_id': book}, 400),
            ({'chapter': 'missing'}, 404), ({'topic': 'missing'}, 404),
            ({'chapter': 'matrices', 'topic': 'infinitesimals'}, 400),
        ):
            with self.subTest(args=args), self.assertRaises(HTTPException) as error:
                server.chapter_practice(**args)
            self.assertEqual(error.exception.status_code, status)
        with self.assertRaises(HTTPException):
            server.paper(1900)

    def test_books_are_fixed_resources_and_open_as_pdf(self):
        pdf = Path(self.temp.name) / 'answers.pdf'
        pdf.write_bytes(b'%PDF-1.7\n%%EOF')
        with patch.dict(practice.BOOKS, {'880-answers': pdf}):
            response = server.workbook('880-answers')
            self.assertEqual(response.media_type, 'application/pdf')
            self.assertTrue(response.headers['content-disposition'].startswith('inline;'))
        for name in ('../study.db', 'not-a-book', '/etc/passwd'):
            with self.assertRaises(HTTPException):
                server.workbook(name)


if __name__ == '__main__':
    unittest.main()

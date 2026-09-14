import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))

import db
import notes
from fastapi import HTTPException
from pydantic import ValidationError


class NotesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_path = db.DB_PATH
        db.DB_PATH = str(Path(self.tmp.name) / 'study.db')
        with notes.connection() as conn:
            db.init_db(conn)
            conn.execute("INSERT INTO questions(id,paper,year,number,qtype,chapter) VALUES(1,'math2',2020,1,'choice','函数极限连续')")
            conn.execute("INSERT INTO questions(id,paper,year,number,qtype,chapter) VALUES(2,'lilin880',0,1,'choice','函数极限连续')")
            conn.execute("INSERT INTO attempts(question_id,result) VALUES(1,'correct')")

    def tearDown(self):
        db.DB_PATH = self.old_path
        self.tmp.cleanup()

    def create(self, question_id=1, body='===关键步骤===\n\n$\\int_0^1 x^2 dx$'):
        return notes.create_note(notes.CreateNote(question_id=question_id, body=body, client_id='test-question-' + str(question_id) + '-note'))

    def test_notes_persist_raw_markdown_and_remain_separate_between_exam_and_880(self):
        exam, book = self.create(), self.create(2, '**880 的笔记**')
        self.assertEqual(notes.list_notes(1)['notes'], [exam])
        self.assertEqual(notes.list_notes(2)['notes'], [book])
        with notes.connection() as conn:
            db.init_db(conn)
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM attempts').fetchone()[0], 1)
        self.assertEqual(notes.list_notes(1)['notes'][0]['body'], exam['body'])
        self.assertTrue(notes.list_notes(2)['question']['practice_chapter'])

    def test_retrying_create_does_not_duplicate_an_already_saved_note(self):
        first, retry = self.create(), self.create()
        self.assertEqual(first['id'], retry['id'])
        self.assertEqual(len(notes.list_notes(1)['notes']), 1)
        with self.assertRaises(HTTPException) as conflict:
            self.create(body='响应丢失后修改的新草稿')
        self.assertEqual(conflict.exception.status_code, 409)
        self.assertEqual(notes.list_notes(1)['notes'][0]['body'], first['body'])

    def test_edit_retries_and_stale_edits_preserve_the_saved_content(self):
        first = self.create()
        edited = notes.update_note(first['id'], notes.UpdateNote(body='新的解法', revision=first['revision']))
        self.assertEqual(edited['revision'], 2)
        retried = notes.update_note(first['id'], notes.UpdateNote(body='新的解法', revision=first['revision']))
        self.assertEqual(retried, edited)
        with self.assertRaises(HTTPException) as conflict:
            notes.update_note(first['id'], notes.UpdateNote(body='另一页面的旧草稿', revision=1))
        self.assertEqual(conflict.exception.status_code, 409)
        self.assertEqual(notes.list_notes(1)['notes'][0]['body'], '新的解法')

    def test_delete_checks_revision_and_does_not_touch_another_question(self):
        exam, book = self.create(), self.create(2)
        with self.assertRaises(HTTPException) as conflict:
            notes.delete_note(exam['id'], revision=99)
        self.assertEqual(conflict.exception.status_code, 409)
        self.assertEqual(notes.delete_note(exam['id'], revision=1), {'ok': True})
        self.assertEqual(notes.list_notes(1)['notes'], [])
        self.assertEqual(notes.list_notes(2)['notes'], [book])

    def test_notebook_search_and_source_filters(self):
        self.create(body='===泰勒展开===\n精度 100%')
        self.create(2, '代换法')
        self.assertEqual([g['question']['id'] for g in notes.notebook(query='泰勒')], [1])
        self.assertEqual([g['question']['id'] for g in notes.notebook(query='%')], [1])
        self.assertEqual([g['question']['id'] for g in notes.notebook(source='lilin880')], [2])
        self.assertEqual([g['question']['id'] for g in notes.notebook(source='exam')], [1])
        self.assertEqual(notes.notebook(query="' OR 1=1 --"), [])

    def test_invalid_notes_are_rejected_before_any_write(self):
        for qid, body, status in [(999, '未知题目', 404), (1, ' \n ', 400)]:
            with self.assertRaises(HTTPException) as error:
                self.create(qid, body)
            self.assertEqual(error.exception.status_code, status)
        with self.assertRaises(ValidationError):
            notes.CreateNote(question_id=1, body='x' * 20001, client_id='test-invalid-note')
        self.assertEqual(notes.notebook(), [])


if __name__ == '__main__':
    unittest.main()

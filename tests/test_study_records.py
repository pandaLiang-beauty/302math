import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
import db
import study
from notes import connection
from fastapi import HTTPException


class StudyRecordsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.patch = patch.object(db, 'DB_PATH', self.tmp.name + '/study.db'); self.patch.start()
        with connection() as c:
            db.init_db(c)
            c.execute("INSERT INTO questions(id,paper,year,number,qtype,options_json) VALUES(1,'math2',2020,1,'choice',?)", (json.dumps([{'key':k,'text':k} for k in 'ABCD']),))
            c.execute("INSERT INTO questions(id,paper,year,number,qtype) VALUES(2,'math2',2020,2,'subjective')")
        self.session = study.open_session(study.OpenSession(scope='exam:2020',title='2020',question_ids=[1,2]))
        self.sid = self.session['id']

    def tearDown(self):
        self.patch.stop(); self.tmp.cleanup()

    def edit(self, rev=0, mutation='unique-mutation-0001', **kw):
        return study.edit_item(self.sid,1,study.EditItem(revision=rev,mutation=mutation,**kw))

    def test_resume_from_another_browser_and_preserve_text(self):
        self.edit(answer='C',work='先看已知条件')
        resumed=study.open_session(study.OpenSession(scope='exam:2020',title='2020',question_ids=[1,2]))
        self.assertEqual(resumed['id'],self.sid)
        self.assertEqual(resumed['items']['1']['answer'],'C')
        self.assertEqual(resumed['items']['1']['work'],'先看已知条件')
        study.edit_item(self.sid,2,study.EditItem(revision=0,mutation='subjective-text-01',answer='$x=2$',work='代入初值'))
        self.assertEqual(study.summary()[0]['started'],2)

    def test_lost_response_is_idempotent_and_other_browser_cannot_overwrite(self):
        saved=self.edit(answer='C')
        self.assertEqual(self.edit(answer='C'),saved)
        with self.assertRaises(HTTPException) as cm:self.edit(mutation='second-browser-001',answer='D')
        self.assertEqual(cm.exception.status_code,409)
        self.assertEqual(cm.exception.detail['current']['answer'],'C')

    def test_completed_attempt_is_immutable_and_redo_keeps_history(self):
        saved=self.edit(answer='C',phase='done',rating='wrong',reason='idea')
        self.edit(answer='C',phase='done',rating='wrong',reason='idea')
        self.assertEqual(len(study.history(1)),1)
        with connection() as c:self.assertEqual(c.execute('SELECT count(*) FROM attempts').fetchone()[0],1)
        with self.assertRaises(HTTPException):self.edit(rev=1,mutation='cannot-overwrite-01',answer='A')
        redo=study.redo(self.sid,1,study.Redo(revision=saved['revision'],mutation='redo-mutation-0001'))
        self.assertEqual(redo['answer'],'')
        self.edit(rev=redo['revision'],mutation='next-attempt-00001',answer='A',phase='done',rating='correct')
        self.assertEqual([h['snapshot']['answer'] for h in study.history(1)],['A','C'])

    def test_invalid_answer_and_missing_question_do_not_write(self):
        for kw in ({'answer':'E'},{'phase':'done'},{'rating':'correct'}):
            with self.assertRaises(HTTPException):self.edit(**kw)
        with self.assertRaises(HTTPException):study.open_session(study.OpenSession(scope='missing',title='missing',question_ids=[999]))
        with connection() as c:self.assertEqual(c.execute('SELECT revision FROM study_items WHERE question_id=1').fetchone()[0],0)

    def test_legacy_import_never_overwrites_server_answers(self):
        first=study.import_choices(study.LegacyChoices(choices={'1':'B','999':'A'}))
        self.assertEqual(first['imported'],[1])
        self.assertEqual(study.import_choices(study.LegacyChoices(choices={'1':'C'}))['conflicts'],[1])
        with connection() as c:self.assertEqual(c.execute('SELECT answer FROM study_items WHERE question_id=1').fetchone()[0],'B')

    def test_wrong_choice_cannot_be_recorded_as_correct_and_keeps_reference(self):
        with connection() as c:c.execute("UPDATE questions SET answer='B' WHERE id=1")
        saved=self.edit(answer='D',phase='done',rating='correct')
        self.assertEqual(saved['rating'],'wrong')
        self.assertEqual(study.history(1)[0]['snapshot']['reference_answer'],'B')

    def test_uncertain_exam_reference_does_not_force_an_automatic_judgment(self):
        with connection() as c:
            c.execute("UPDATE questions SET answer='B' WHERE id=1")
            c.execute("INSERT INTO exam_explanations(question_id,content_hash,solution_markdown,solution_source,answer_checkable) VALUES(1,'hash','条件有差异','独立推导',0)")
        saved=self.edit(answer='D',phase='done',rating='correct')
        self.assertEqual(saved['rating'],'correct')
        self.assertFalse(study.history(1)[0]['snapshot']['reference_checkable'])

if __name__ == '__main__':unittest.main()

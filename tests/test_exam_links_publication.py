import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'backend'), str(ROOT/'scripts')]
import db
import study
import publish_exam_links as publication


class ExamLinksPublicationTest(unittest.TestCase):
    def test_publication_is_atomic_and_preserves_work(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(db, 'DB_PATH', tmp+'/study.db'), patch.object(publication, 'ROOT', Path(tmp)):
            folder = Path(tmp)/'content'; folder.mkdir()
            conn = db.connect(); db.init_db(conn)
            conn.execute("INSERT INTO questions(id,paper,year,number,qtype,stem_html) VALUES(1,'math2',2020,1,'blank','exam')")
            conn.execute("INSERT INTO questions(id,paper,year,number,qtype) VALUES(2,'lilin880',0,1,'blank')")
            conn.execute("INSERT INTO workbook_text(question_id,source_key,book,chapter_number,source_pages,stem_markdown,options_markdown,content_hash) VALUES(2,'sample','calculus',1,'1','question','[]','v1')")
            conn.commit(); conn.close()
            session = study.open_session(study.OpenSession(scope='exam:2020',title='2020',question_ids=[1]))
            study.edit_item(session['id'],1,study.EditItem(revision=0,mutation='before-publication',answer='my answer',work='my work'))
            fingerprint = study.question_hash('exam','[]')
            pair = dict(source_id=1,target_id=2,skill='specific method',reason='shared operation',stage='同法练习',source_hash=fingerprint,target_hash='v1')
            def put(name,value): (folder/name).write_text(json.dumps(value))
            put('relations.json',[pair]);put('relation-sources.json',[dict(id=1,source_hash=fingerprint)])
            answer = dict(answer='$1$',note='',source_pages=[3],checkable=True,content_hash='v1')
            put('reference-answers.json',{'sample':answer})
            self.assertEqual(publication.apply()['answers'],1)
            put('relations.json',[])
            put('reference-answers.json',{'sample':{**answer,'content_hash':'stale'}})
            with self.assertRaises(ValueError): publication.apply()
            conn=db.connect()
            self.assertEqual(conn.execute('SELECT count(*) FROM math_relations').fetchone()[0],1)
            self.assertEqual(tuple(conn.execute('SELECT answer,work FROM study_items').fetchone()),('my answer','my work'))
            conn.close()
            put('reference-answers.json',{'sample':{**answer,'checkable':False,'note':'原题存在疑点'}})
            publication.apply()
            conn=db.connect()
            self.assertEqual(conn.execute('SELECT count(*) FROM math_relations').fetchone()[0],0)
            self.assertEqual(conn.execute('SELECT answer FROM questions WHERE id=2').fetchone()[0],'')
            self.assertEqual(conn.execute('SELECT answer FROM reference_answers').fetchone()[0],'$1$')
            conn.close()

if __name__=='__main__':unittest.main()

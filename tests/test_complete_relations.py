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
import publish_relations as publication

class CompleteRelationsTest(unittest.TestCase):
    def test_committed_coverage_and_hashes(self):
        conn = db.connect()
        try:
            rows = json.loads(publication.OUTPUT.read_text())
            publication.validate(conn, rows)
            self.assertEqual(len({p['target_id'] for p in rows}), 929)
            core = {r[0] for r in conn.execute("SELECT id FROM questions WHERE paper='math2' AND year BETWEEN 2020 AND 2026")}
            self.assertEqual(len(core),155)
            self.assertTrue(core <= {p['source_id'] for p in rows})
            self.assertTrue(any(p['source_id']==17283 and p['target_id']==13519 and p['stage']=='同法练习' for p in rows))
        finally: conn.close()

    def test_links_only_atomic_and_reverse_hash_filter(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(db,'DB_PATH',tmp+'/study.db'), patch.object(publication,'OUTPUT',Path(tmp)/'links.json'):
            conn=db.connect();db.init_db(conn)
            conn.execute("INSERT INTO questions(id,paper,year,number,qtype,stem_html,answer) VALUES(1,'math2',2020,1,'blank','exam','original')")
            conn.execute("INSERT INTO questions(id,paper,year,number,qtype) VALUES(2,'lilin880',0,1,'blank')")
            conn.execute("INSERT INTO workbook_text(question_id,source_key,book,chapter_number,source_pages,stem_markdown,options_markdown,content_hash) VALUES(2,'sample','calculus',1,'1','question','[]','v1')")
            conn.execute("INSERT INTO reference_answers(question_id,content_hash,answer) VALUES(2,'v1','reference')")
            conn.commit();conn.close()
            session=study.open_session(study.OpenSession(scope='test',title='test',question_ids=[1]))
            study.edit_item(session['id'],1,study.EditItem(revision=0,mutation='save-before-publish',answer='mine',work='work'))
            pair=dict(source_id=1,target_id=2,skill='step',reason='shared step',stage='基础衔接',source_hash=study.question_hash('exam','[]'),target_hash='v1')
            publication.OUTPUT.write_text(json.dumps([pair]));publication.apply();publication.apply()
            self.assertEqual(study.linked_exams(2)['exams'][0]['id'],1)
            for bad in ([{**pair,'target_hash':'stale'}],[{**pair,'source_hash':'stale'}],[],[pair,pair]):
                publication.OUTPUT.write_text(json.dumps(bad))
                with self.assertRaises(ValueError):publication.apply()
                self.assertEqual(len(study.linked_exams(2)['exams']),1)
            conn=db.connect()
            self.assertEqual(conn.execute('SELECT answer FROM reference_answers').fetchone()[0],'reference')
            self.assertEqual(conn.execute('SELECT answer FROM questions WHERE id=1').fetchone()[0],'original')
            self.assertEqual(tuple(conn.execute('SELECT answer,work FROM study_items').fetchone()),('mine','work'))
            conn.execute("UPDATE questions SET stem_html='edited' WHERE id=1");conn.commit();conn.close()
            self.assertEqual(study.linked_exams(2)['exams'],[])

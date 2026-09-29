import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'backend'),str(ROOT/'scripts')]
import db
import study
import publish_content


class PublicationTest(unittest.TestCase):
    def test_exact_review_replacement_and_stale_content_preserve_learning(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(db,'DB_PATH',tmp+'/study.db'),patch.object(publish_content,'ROOT',Path(tmp)):
            (Path(tmp)/'content').mkdir();(Path(tmp)/'content/exam-solutions.json').write_text('{}')
            c=db.connect();db.init_db(c)
            c.execute("INSERT INTO questions(id,paper,year,number,qtype,stem_html) VALUES(1,'math2',2020,1,'blank','original')")
            c.execute("INSERT INTO questions(id,paper,year,number,qtype) VALUES(2,'lilin880',0,1,'choice')")
            c.execute("INSERT INTO workbook_text(question_id,source_key,book,chapter_number,source_pages,stem_markdown,options_markdown,content_hash) VALUES(2,'test','calculus',1,'1','practice','[]','target-v1')")
            c.commit();c.close()
            session=study.open_session(study.OpenSession(scope='exam:2020',title='2020',question_ids=[1]))
            study.edit_item(session['id'],1,study.EditItem(revision=0,mutation='saved-before-content-update',work='保留我的演算'))
            source_hash=study.question_hash('original','[]')
            sources=[{'id':1,'source_hash':source_hash}]
            pair={'source_id':1,'target_id':2,'skill':'method','reason':'specific reasoning','stage':'同法练习','source_hash':source_hash,'target_hash':'target-v1'}
            self.assertEqual(publish_content.apply({},[pair],sources)['relations'],1)
            stale={**pair,'target_hash':'wrong-version'}
            self.assertEqual(publish_content.apply({},[stale],sources)['stale_relations'],[[1,2]])
            c=db.connect();self.assertEqual(c.execute('SELECT count(*) FROM math_relations').fetchone()[0],1);c.close()
            publish_content.apply({},[],sources)
            c=db.connect()
            self.assertEqual(c.execute('SELECT count(*) FROM math_relations').fetchone()[0],0)
            self.assertEqual(c.execute('SELECT work FROM study_items').fetchone()[0],'保留我的演算')
            c.close()


if __name__=='__main__':unittest.main()

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'backend'),str(ROOT/'scripts')]
import db
import import_workbook


class WorkbookImportTest(unittest.TestCase):
    def test_complete_source_and_repeatable_import_preserve_question_links(self):
        incoming=import_workbook.records()
        self.assertEqual(len(incoming),929)
        self.assertEqual(sum(r['original_number'] is None for r in incoming),4)
        diagram=next(r for r in incoming if r['source_key']=='calculus-Q179')
        self.assertIn('图示文字转写',diagram['stem_markdown'])
        self.assertNotIn('图示文字转写',diagram['options'][-1]['text'])
        with tempfile.TemporaryDirectory() as tmp,patch.object(db,'DB_PATH',tmp+'/study.db'):
            c=db.connect();db.init_db(c)
            number=0
            for r in incoming:
                if r['original_number'] is None:continue
                number+=1
                c.execute("INSERT INTO questions(id,paper,year,number,qtype,chapter,level) VALUES(?,'lilin880',0,?,?,?,?)",(10000+number,number,r['qtype'],r['chapter'],r['level']))
            c.execute("INSERT INTO notes(question_id,body,client_id) VALUES(10001,'旧笔记','existing-note-client')")
            c.execute("INSERT INTO attempts(question_id,result) VALUES(10001,'wrong')")
            c.commit()
            with c:import_workbook.apply(c,incoming)
            first=[tuple(r) for r in c.execute('SELECT question_id,source_key FROM workbook_text ORDER BY source_key')]
            with c:import_workbook.apply(c,incoming)
            self.assertEqual(first,[tuple(r) for r in c.execute('SELECT question_id,source_key FROM workbook_text ORDER BY source_key')])
            self.assertEqual(c.execute('SELECT count(*) FROM questions').fetchone()[0],929)
            self.assertEqual(c.execute('SELECT question_id FROM notes').fetchone()[0],10001)
            self.assertEqual(c.execute('SELECT question_id FROM attempts').fetchone()[0],10001)
            text=c.execute("SELECT stem_markdown FROM workbook_text WHERE source_key='calculus-Q021'").fetchone()[0]
            self.assertIn('x^{\\sin x}',text)
            self.assertEqual(len(json.loads(c.execute('SELECT options_json FROM questions WHERE id=10001').fetchone()[0])),4)
            c.execute("UPDATE workbook_text SET solution_markdown='old solution' WHERE question_id=10001")
            c.execute("UPDATE questions SET answer='A' WHERE id=10001")
            changed=[{**r} for r in incoming]
            changed[0]['content_hash']='changed-content'
            with c:import_workbook.apply(c,changed)
            self.assertEqual(c.execute('SELECT solution_markdown FROM workbook_text WHERE question_id=10001').fetchone()[0],'')
            self.assertEqual(c.execute('SELECT answer FROM questions WHERE id=10001').fetchone()[0],'')
            self.assertEqual(c.execute('SELECT question_id FROM notes').fetchone()[0],10001)
            c.close()

if __name__=='__main__':unittest.main()

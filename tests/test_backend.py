import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))

import db  # noqa: E402
import server  # noqa: E402
from fastapi import HTTPException  # noqa: E402


class BackendDataTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.original_db_path = db.DB_PATH
        db.DB_PATH = str(Path(self.tmpdir.name) / 'study.db')
        conn = db.connect()
        db.init_db(conn)
        conn.execute(
            "INSERT INTO questions(paper,year,number,qtype,subject,chapter) "
            "VALUES('lilin880',0,1,'choice','高等数学','函数极限连续')"
        )
        conn.commit()
        db.sync_880_fallback_types(conn)
        conn.execute("INSERT INTO types(name,subject,chapter,point) VALUES('测试题型','高等数学','测试章','测试点')")
        conn.commit()
        conn.close()

    def tearDown(self):
        db.DB_PATH = self.original_db_path
        self.tmpdir.cleanup()

    def test_unclassified_880_gets_a_reachable_pending_cluster(self):
        conn = db.connect()
        question = conn.execute("SELECT type_name,point FROM questions").fetchone()
        type_row = conn.execute("SELECT name,curated FROM types WHERE name=?", (question['type_name'],)).fetchone()
        conn.close()

        self.assertEqual(question['type_name'], '李林880·函数极限连续·待归纳')
        self.assertEqual(question['point'], '待归纳')
        self.assertIsNotNone(type_row)
        self.assertEqual(type_row['curated'], 0)

    def test_write_endpoints_reject_unknown_references(self):
        with self.assertRaises(HTTPException) as attempt_error:
            server.attempt(server.Attempt(question_id=999, result='wrong'))
        self.assertEqual(attempt_error.exception.status_code, 404)

        with self.assertRaises(HTTPException) as progress_error:
            server.type_status(server.TypeStatus(name='不存在的题型', status='mastered'))
        self.assertEqual(progress_error.exception.status_code, 404)

    def test_write_endpoints_accept_existing_references(self):
        conn = db.connect()
        question_id = conn.execute("SELECT id FROM questions").fetchone()['id']
        type_name = '测试题型'
        conn.close()

        self.assertEqual(
            server.attempt(server.Attempt(question_id=question_id, result='wrong', reason='idea', elapsed_seconds=31)),
            {'ok': True},
        )
        self.assertEqual(server.type_status(server.TypeStatus(name=type_name, status='mastered')), {'ok': True})
        conn = db.connect()
        attempt = conn.execute("SELECT result,reason,elapsed_seconds FROM attempts").fetchone()
        conn.close()
        self.assertEqual(dict(attempt), {'result': 'wrong', 'reason': 'idea', 'elapsed_seconds': 31})

    def test_pending_cluster_cannot_be_marked_mastered(self):
        conn = db.connect()
        pending_name = conn.execute("SELECT name FROM types WHERE name LIKE '李林880·%·待归纳'").fetchone()['name']
        conn.close()
        with self.assertRaises(HTTPException) as error:
            server.type_status(server.TypeStatus(name=pending_name, status='mastered'))
        self.assertEqual(error.exception.status_code, 400)


if __name__ == '__main__':
    unittest.main()

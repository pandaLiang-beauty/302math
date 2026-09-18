import base64
from concurrent.futures import ThreadPoolExecutor
import io
from pathlib import Path
import secrets
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))

import db
import drafts
import notes
import practice
import server
from fastapi import HTTPException
from PIL import Image


def photo(fmt='PNG', color='white'):
    output = io.BytesIO()
    Image.new('RGB', (24, 32), color).save(output, format=fmt)
    return output.getvalue()


def payload(blob=None, client_id=None):
    return drafts.UploadImage(
        image_base64='data:image/png;base64,' + base64.b64encode(blob if blob is not None else photo()).decode(),
        client_id=client_id or secrets.token_hex(16),
    )


class DraftsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.patch = patch.object(db, 'DB_PATH', str(Path(self.tmp.name) / 'study.db'))
        self.patch.start()
        with notes.connection() as conn:
            db.init_db(conn)
            conn.execute("INSERT INTO questions(id,paper,year,number,qtype,chapter) "
                         "VALUES(1,'math2',2020,1,'choice','函数极限连续')")
            conn.execute("INSERT INTO questions(id,paper,year,number,qtype,chapter) "
                         "VALUES(2,'math2',2021,1,'choice','函数极限连续')")
            conn.execute("INSERT INTO questions(id,paper,year,number,qtype,chapter) "
                         "VALUES(3,'lilin880',0,1,'choice','函数极限连续')")
            conn.execute("INSERT INTO attempts(question_id,result) VALUES(1,'correct')")
        self.note = notes.create_note(notes.CreateNote(
            question_id=1, body='保留原来的笔记 $x^2$', client_id='existing-note-client-id'))

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def token(self, question_id=1):
        return drafts.issue_token(question_id)['path'].rsplit('/', 1)[1]

    def assert_status(self, status, operation, *args, **kwargs):
        with self.assertRaises(HTTPException) as error:
            operation(*args, **kwargs)
        self.assertEqual(error.exception.status_code, status)

    def test_appending_photos_and_reinitializing_keep_every_image_and_existing_study_data(self):
        images = [drafts.upload_draft(1, payload(photo(fmt))) for fmt in ('PNG', 'JPEG', 'WEBP', 'GIF')]
        with notes.connection() as conn:
            db.init_db(conn)
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM attempts').fetchone()[0], 1)
        self.assertEqual(drafts.list_drafts(1)['drafts'], images)
        for image, fmt in zip(images, ('PNG', 'JPEG', 'WEBP', 'GIF')):
            response = drafts.get_image(image['id'])
            self.assertEqual(Path(response.path).read_bytes(), photo(fmt))
            self.assertEqual(response.media_type, drafts.FORMATS[fmt][1])
            self.assertEqual(response.headers['cache-control'], 'no-store')
        self.assertEqual(notes.list_notes(1)['notes'], [self.note])

    def test_photos_are_shared_by_question_views_but_never_across_questions(self):
        exam = drafts.upload_draft(1, payload())
        book = drafts.upload_draft(3, payload())
        self.assertEqual(drafts.list_drafts(1)['drafts'], [exam])
        self.assertEqual(drafts.list_drafts(2)['drafts'], [])
        self.assertEqual(drafts.list_drafts(3)['drafts'], [book])
        self.assertEqual(server.paper(2020)['problems'][0]['draft_count'], 1)
        self.assertEqual(server.paper(2020)['problems'][0]['note_count'], 1)
        self.assertEqual(server.paper(2021)['problems'][0]['draft_count'], 0)
        rows, _ = server._progress('')
        self.assertEqual({row['id']: row['draft_count'] for row in rows}, {1: 1, 2: 0, 3: 1})
        with notes.connection() as conn:
            data = practice.get_practice(conn, chapter='limits')
        self.assertEqual(data['problems'][0]['draft_count'], 1)

    def test_retry_after_lost_response_does_not_duplicate_or_replace_a_photo(self):
        original = payload()
        first = drafts.upload_draft(1, original)
        self.assertEqual(drafts.upload_draft(1, original), first)
        self.assert_status(409, drafts.upload_draft, 1, payload(photo(color='red'), original.client_id))
        self.assert_status(409, drafts.upload_draft, 2, original)
        self.assertEqual(drafts.list_drafts(1)['drafts'], [first])
        self.assertEqual(len(list(drafts.image_directory().iterdir())), 1)

    def test_phone_links_append_without_exposing_other_saved_photos(self):
        local = drafts.upload_draft(1, payload())
        token = self.token()
        page = drafts.phone_page(token)
        self.assertIn('2020 年', page.body.decode())
        self.assertNotIn(local['url'], page.body.decode())
        result = drafts.phone_upload(token, payload(photo('JPEG')))
        self.assertEqual(set(result), {'ok', 'id'})
        self.assertTrue(result['ok'])
        self.assertEqual(len(drafts.list_drafts(1)['drafts']), 2)
        self.assertEqual(drafts.list_drafts(2)['drafts'], [])
        next_result = drafts.phone_upload(self.token(), payload(photo('GIF')))
        self.assertNotEqual(next_result['id'], result['id'])
        self.assertEqual(len(drafts.list_drafts(1)['drafts']), 3)

    def test_phone_link_allows_only_the_original_upload_to_retry(self):
        token = self.token()
        original = payload()
        first = drafts.phone_upload(token, original)
        self.assertEqual(drafts.phone_upload(token, original), first)
        self.assert_status(410, drafts.phone_upload, token, payload())
        self.assert_status(410, drafts.phone_page, token)
        self.assertEqual(len(drafts.list_drafts(1)['drafts']), 1)
        drafts.delete_image(first['id'])
        self.assert_status(410, drafts.phone_upload, token, original)

    def test_concurrent_phone_uploads_cannot_reuse_one_token(self):
        token = self.token()
        def send(_):
            try:
                return drafts.phone_upload(token, payload())['ok']
            except HTTPException as error:
                return error.status_code
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(send, range(2)))
        self.assertEqual(sorted(results), [True, 410])
        self.assertEqual(len(drafts.list_drafts(1)['drafts']), 1)
        self.assertEqual(len(list(drafts.image_directory().iterdir())), 1)

    def test_expired_unknown_or_cross_question_tokens_cannot_write(self):
        token = self.token()
        digest = drafts.token_digest(token)
        self.assert_status(404, drafts.save_image, 2, payload(), digest=digest)
        with notes.connection() as conn:
            conn.execute('UPDATE draft_tokens SET expires_at=?', (int(time.time()) - 1,))
        self.assert_status(410, drafts.phone_upload, token, payload())
        self.assert_status(404, drafts.phone_upload, secrets.token_urlsafe(32), payload())
        self.assert_status(404, drafts.phone_upload, '../notes', payload())
        self.assertEqual(drafts.list_drafts(1)['drafts'], [])

    def test_invalid_images_do_not_use_up_a_token_or_damage_existing_photos(self):
        first = drafts.upload_draft(1, payload())
        token = self.token()
        for invalid in (b'<svg xmlns="http://www.w3.org/2000/svg"></svg>',
                        b'\x89PNG\r\n\x1a\nnot an image', photo('JPEG')[:-30], b'x' * 9_000_001):
            self.assert_status(400, drafts.phone_upload, token, payload(invalid))
        self.assert_status(400, drafts.upload_draft, 1,
                           drafts.UploadImage(image_base64='not-base64!', client_id=secrets.token_hex(16)))
        with notes.connection() as conn:
            self.assertIsNone(drafts.load_token(conn, drafts.token_digest(token))['used_at'])
        self.assertEqual(drafts.list_drafts(1)['drafts'], [first])
        self.assertTrue(drafts.phone_upload(token, payload())['ok'])

    def test_database_failure_rolls_back_token_and_removes_only_the_new_file(self):
        first = drafts.upload_draft(1, payload())
        token = self.token()
        with notes.connection() as conn:
            conn.execute("CREATE TRIGGER fail_draft BEFORE INSERT ON draft_images "
                         "BEGIN SELECT RAISE(ABORT, 'test failure'); END")
        with self.assertRaises(Exception):
            drafts.phone_upload(token, payload(photo('JPEG')))
        self.assertEqual(drafts.list_drafts(1)['drafts'], [first])
        self.assertEqual(len(list(drafts.image_directory().iterdir())), 1)
        with notes.connection() as conn:
            self.assertIsNone(drafts.load_token(conn, drafts.token_digest(token))['used_at'])
            conn.execute('DROP TRIGGER fail_draft')
        self.assertTrue(drafts.phone_upload(token, payload())['ok'])

    def test_deleting_a_photo_is_retryable_and_preserves_the_rest(self):
        first = drafts.upload_draft(1, payload())
        second = drafts.upload_draft(1, payload(photo('JPEG')))
        other = drafts.upload_draft(2, payload())
        path = Path(drafts.get_image(first['id']).path)
        self.assertEqual(drafts.delete_image(first['id']), {'ok': True})
        self.assertEqual(drafts.delete_image(first['id']), {'ok': True})
        self.assertFalse(path.exists())
        self.assert_status(404, drafts.get_image, first['id'])
        self.assertEqual(drafts.list_drafts(1)['drafts'], [second])
        self.assertEqual(drafts.list_drafts(2)['drafts'], [other])
        self.assertEqual(notes.list_notes(1)['notes'], [self.note])

    def test_unknown_questions_do_not_create_upload_links_or_files(self):
        self.assert_status(404, drafts.upload_draft, 999, payload())
        self.assert_status(404, drafts.issue_token, 999)
        self.assert_status(404, drafts.list_drafts, 999)
        self.assertFalse(drafts.image_directory().exists())
        with notes.connection() as conn:
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM draft_tokens').fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()

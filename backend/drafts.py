"""Paper-work photos, saved per question; phone links authorize one upload only."""
import base64
import binascii
import hashlib
import html
import io
import logging
import re
import secrets
import time
import warnings
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, Field

import db
from notes import connection, question_info

router = APIRouter(prefix='/api')
MAX_IMAGE_BYTES = 9_000_000
MAX_IMAGE_PIXELS = 40_000_000
TOKEN_TTL_SECONDS = 600
FORMATS = {'JPEG': ('.jpg', 'image/jpeg'), 'PNG': ('.png', 'image/png'),
           'WEBP': ('.webp', 'image/webp'), 'GIF': ('.gif', 'image/gif')}
PAGE = Path(__file__).with_name('draft_upload.html').read_text(encoding='utf-8')
PRIVATE_HEADERS = {'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff',
                   'Referrer-Policy': 'no-referrer'}


class UploadImage(BaseModel):
    image_base64: str = Field(min_length=1, max_length=12_000_128)
    client_id: str = Field(min_length=16, max_length=80, pattern=r'^[a-zA-Z0-9_-]+$')


def image_directory():
    return Path(db.DB_PATH).parent / 'drafts'


def image_record(row):
    return {'id': row['id'], 'question_id': row['question_id'],
            'url': f"/api/draft-images/{row['id']}", 'byte_size': row['byte_size'],
            'created_at': row['created_at']}


def decode_image(raw):
    encoded = raw.split(',', 1)[1] if raw.startswith('data:') and ',' in raw else raw
    try:
        blob = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        raise HTTPException(400, '图片格式不正确')
    if not blob or len(blob) > MAX_IMAGE_BYTES:
        raise HTTPException(400, '单张草稿图片最多 9 MB')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(blob)) as source:
                if source.format not in FORMATS:
                    raise HTTPException(400, '请选择 JPG、PNG、WebP 或 GIF 图片')
                if source.width * source.height > MAX_IMAGE_PIXELS:
                    raise HTTPException(400, '图片尺寸过大，请缩小后上传')
                extension, content_type = FORMATS[source.format]
                source.verify()
            # verify() alone does not detect truncated JPEG pixel data.
            with Image.open(io.BytesIO(blob)) as source:
                source.load()
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError,
            Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(400, '图片损坏或尺寸过大，请重新选择')
    return blob, extension, content_type


def token_digest(token):
    if not re.fullmatch(r'[A-Za-z0-9_-]{43}', token):
        raise HTTPException(404, '上传链接无效')
    return hashlib.sha256(token.encode()).hexdigest()


def load_token(conn, digest, *, allow_used=False):
    row = conn.execute('SELECT * FROM draft_tokens WHERE token_hash=?', (digest,)).fetchone()
    if row is None:
        raise HTTPException(404, '上传链接无效')
    if row['expires_at'] <= int(time.time()) or (row['used_at'] is not None and not allow_used):
        raise HTTPException(410, '链接已使用或过期，请在电脑上重新生成二维码')
    return row


def save_image(question_id, payload, *, digest=None):
    blob, extension, content_type = decode_image(payload.image_base64)
    content_hash = hashlib.sha256(blob).hexdigest()
    written_path = None
    try:
        with connection() as conn:
            # Serialize retries and token claims along with the image association.
            conn.execute('BEGIN IMMEDIATE')
            question_info(conn, question_id)
            token = load_token(conn, digest, allow_used=True) if digest else None
            if token is not None and token['question_id'] != question_id:
                raise HTTPException(404, '上传链接无效')
            existing = conn.execute('SELECT * FROM draft_images WHERE client_id=?',
                                    (payload.client_id,)).fetchone()
            if token is not None and token['used_at'] is not None:
                if existing is None or token['image_id'] != existing['id']:
                    raise HTTPException(410, '链接已使用，请在电脑上重新生成二维码')
            if existing:
                if existing['question_id'] != question_id or existing['content_hash'] != content_hash:
                    raise HTTPException(409, '这次上传已经保存，请刷新草稿纸后核对')
                record = image_record(existing)
            else:
                directory = image_directory()
                directory.mkdir(parents=True, exist_ok=True)
                name = secrets.token_hex(24) + extension
                path = directory / name
                with path.open('xb') as output:
                    written_path = path
                    output.write(blob)
                cursor = conn.execute(
                    'INSERT INTO draft_images(question_id,stored_name,content_type,byte_size,content_hash,client_id) '
                    'VALUES(?,?,?,?,?,?)',
                    (question_id, name, content_type, len(blob), content_hash, payload.client_id),
                )
                row = conn.execute('SELECT * FROM draft_images WHERE id=?', (cursor.lastrowid,)).fetchone()
                record = image_record(row)
            if token is not None and token['used_at'] is None:
                conn.execute('UPDATE draft_tokens SET used_at=?,image_id=? WHERE token_hash=?',
                             (int(time.time()), record['id'], digest))
        return record
    except Exception:
        if written_path is not None:
            written_path.unlink(missing_ok=True)
        raise


@router.get('/questions/{question_id}/drafts')
def list_drafts(question_id: int):
    with connection() as conn:
        question = question_info(conn, question_id)
        images = [image_record(row) for row in conn.execute(
            'SELECT * FROM draft_images WHERE question_id=? ORDER BY id', (question_id,))]
        return {'question': question, 'drafts': images}


@router.post('/questions/{question_id}/drafts', status_code=201)
def upload_draft(question_id: int, payload: UploadImage):
    return save_image(question_id, payload)


@router.api_route('/draft-images/{image_id}', methods=['GET', 'HEAD'])
def get_image(image_id: int):
    with connection() as conn:
        row = conn.execute('SELECT stored_name,content_type FROM draft_images WHERE id=?', (image_id,)).fetchone()
    if row is None:
        raise HTTPException(404, '这张草稿已不存在')
    path = image_directory() / Path(row['stored_name']).name
    if not path.is_file():
        raise HTTPException(404, '草稿图片文件不存在')
    return FileResponse(path, media_type=row['content_type'], headers=PRIVATE_HEADERS)


@router.delete('/draft-images/{image_id}')
def delete_image(image_id: int):
    with connection() as conn:
        conn.execute('BEGIN IMMEDIATE')
        row = conn.execute('SELECT stored_name FROM draft_images WHERE id=?', (image_id,)).fetchone()
        conn.execute('DELETE FROM draft_images WHERE id=?', (image_id,))
    if row:
        try:
            (image_directory() / Path(row['stored_name']).name).unlink(missing_ok=True)
        except OSError:
            logging.getLogger(__name__).warning('Could not remove unreferenced draft file for image %s', image_id)
    return {'ok': True}


@router.post('/questions/{question_id}/draft-token')
def issue_token(question_id: int):
    token = secrets.token_urlsafe(32)
    expires_at = int(time.time()) + TOKEN_TTL_SECONDS
    with connection() as conn:
        question_info(conn, question_id)
        conn.execute('DELETE FROM draft_tokens WHERE expires_at<=?', (int(time.time()),))
        conn.execute('INSERT INTO draft_tokens(token_hash,question_id,expires_at) VALUES(?,?,?)',
                     (token_digest(token), question_id, expires_at))
    return {'path': '/api/draft-upload/' + token, 'expires_at': expires_at}


@router.api_route('/draft-upload/{token}', methods=['GET', 'HEAD'], response_class=HTMLResponse)
def phone_page(token: str):
    with connection() as conn:
        row = load_token(conn, token_digest(token))
        label = question_info(conn, row['question_id'])['source']
    return HTMLResponse(PAGE.replace('__QUESTION_LABEL__', html.escape(label)), headers={
        **PRIVATE_HEADERS, 'X-Frame-Options': 'DENY',
        'Content-Security-Policy': "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
                                   "img-src blob: data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'",
    })


@router.post('/draft-upload/{token}')
def phone_upload(token: str, payload: UploadImage):
    digest = token_digest(token)
    with connection() as conn:
        row = load_token(conn, digest, allow_used=True)
        question_id = row['question_id']
    image = save_image(question_id, payload, digest=digest)
    # A phone upload link never grants access to existing photos or notes.
    return {'ok': True, 'id': image['id']}

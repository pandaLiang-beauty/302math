# -*- coding: utf-8 -*-
"""MinerU 精准解析客户端。用法:
  python mineru.py gs [page_ranges] [outdir]   # gs=高数篇 xd=线代篇 ans=参考答案
本地文件走 batch 上传流:申请上传URL -> PUT 上传 -> 轮询 -> 下载zip解压。
"""
import os, sys, time, json, zipfile, io, glob
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import requests

BACKEND = os.path.dirname(os.path.abspath(__file__))
MATH = os.path.dirname(BACKEND)
TARGETS = {'gs': '高数篇', 'xd': '线代篇', 'ans': '参考答案'}

def token():
    for line in open(os.path.join(BACKEND, '.env.local'), encoding='utf-8'):
        if line.startswith('MINERU_TOKEN='):
            return line.split('=', 1)[1].strip()
    raise SystemExit('no MINERU_TOKEN in .env.local')

TOK = token()
H = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOK}', 'Accept': '*/*'}
BASE = 'https://mineru.net/api/v4'

def find(key):
    sub = TARGETS.get(key, key)
    m = [f for f in glob.glob(os.path.join(MATH, '*.pdf')) if sub in os.path.basename(f)]
    if not m: raise SystemExit(f'no pdf match {sub}')
    return m[0]

def submit(path, page_ranges=None, model='vlm', is_ocr=False):
    f = {'name': os.path.basename(path)}
    if page_ranges: f['page_ranges'] = page_ranges
    if is_ocr: f['is_ocr'] = True
    data = {'files': [f], 'model_version': model, 'enable_formula': True, 'enable_table': True}
    r = requests.post(f'{BASE}/file-urls/batch', headers=H, json=data, timeout=60)
    j = r.json()
    print('submit:', r.status_code, 'code=', j.get('code'), 'msg=', j.get('msg'))
    if j.get('code') != 0: raise SystemExit(json.dumps(j, ensure_ascii=False))
    bid = j['data']['batch_id']; up = j['data']['file_urls'][0]
    print('batch_id:', bid)
    sz = os.path.getsize(path)
    print(f'uploading {sz/1e6:.1f}MB ...')
    with open(path, 'rb') as fh:
        ru = requests.put(up, data=fh, timeout=1200)
    print('upload http:', ru.status_code)
    if ru.status_code not in (200, 201): raise SystemExit('upload failed')
    return bid

def poll(bid, timeout=2400, interval=6):
    start = time.time()
    while time.time() - start < timeout:
        r = requests.get(f'{BASE}/extract-results/batch/{bid}', headers=H, timeout=60)
        j = r.json()
        res = (j.get('data') or {}).get('extract_result') or []
        el = int(time.time() - start)
        if res:
            e = res[0]; st = e.get('state'); pr = e.get('extract_progress') or {}
            print(f'[{el}s] {st} {pr.get("extracted_pages","")}/{pr.get("total_pages","")}')
            if st == 'done': return e['full_zip_url']
            if st == 'failed': raise SystemExit('failed: ' + str(e.get('err_msg')))
        else:
            print(f'[{el}s] waiting queue...')
        time.sleep(interval)
    raise SystemExit('poll timeout, batch=' + bid)

def fetch(url, outdir):
    os.makedirs(outdir, exist_ok=True)
    r = requests.get(url, timeout=1200)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(outdir)
    print('extracted ->', outdir)
    print('files:', z.namelist()[:30])
    return outdir

if __name__ == '__main__':
    key = sys.argv[1]
    pr = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '-' else None
    outdir = sys.argv[3] if len(sys.argv) > 3 else os.path.join(BACKEND, '_mineru_' + key)
    path = find(key)
    print('target:', os.path.basename(path), '| pages:', pr or 'ALL')
    bid = submit(path, pr)
    url = poll(bid)
    print('zip_url:', url)
    fetch(url, outdir)
    print('DONE')

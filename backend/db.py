"""SQLite 连接 + 建表。数二·题型体系,单用户,业务表不带 user_id。"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, 'data', 'study.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS questions(
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  paper       TEXT NOT NULL, year INTEGER NOT NULL, number INTEGER NOT NULL,
  qtype       TEXT NOT NULL,                       -- choice | blank | subjective
  subject     TEXT NOT NULL DEFAULT '',            -- 科目
  chapter     TEXT NOT NULL DEFAULT '',            -- 章
  point       TEXT NOT NULL DEFAULT '',            -- 具体点
  type_name   TEXT NOT NULL DEFAULT '',            -- 题型(定积分应用=细分;其余=具体点直通)
  level       TEXT NOT NULL DEFAULT '基础',        -- 基础 | 综合(暂用题型代理,后续接880难度)
  stem_html   TEXT NOT NULL DEFAULT '',
  answer      TEXT NOT NULL DEFAULT '',
  answer_html TEXT NOT NULL DEFAULT '',
  solution_html TEXT NOT NULL DEFAULT '',
  score       INTEGER NOT NULL DEFAULT 0,
  source_url  TEXT NOT NULL DEFAULT '',
  plain       TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_q_type ON questions(type_name);
CREATE INDEX IF NOT EXISTS idx_q_point ON questions(point);
CREATE INDEX IF NOT EXISTS idx_q_chapter ON questions(chapter, point);

CREATE TABLE IF NOT EXISTS types(
  name          TEXT PRIMARY KEY,
  subject       TEXT NOT NULL DEFAULT '',
  chapter       TEXT NOT NULL DEFAULT '',
  point         TEXT NOT NULL DEFAULT '',
  intuition     TEXT NOT NULL DEFAULT '',          -- 一句话直觉:为什么这么做
  example_src   TEXT NOT NULL DEFAULT '',          -- 母题出处
  example_qid   INTEGER,                           -- 母题对应的库内题(可空)
  example_stem  TEXT NOT NULL DEFAULT '',          -- 母题题面(LaTeX)
  example_steps_json TEXT NOT NULL DEFAULT '[]',   -- 母题逐步演算
  variants_json TEXT NOT NULL DEFAULT '[]',        -- 变式:题目这样变,哪一步跟着变
  figures_json  TEXT NOT NULL DEFAULT '[]',        -- 数学图(内联 SVG,按母题真实区域算出)
  trigger       TEXT NOT NULL DEFAULT '',          -- 讲解:识别信号
  steps_json    TEXT NOT NULL DEFAULT '[]',        -- 讲解:通用打法
  pitfalls_json TEXT NOT NULL DEFAULT '[]',        -- 讲解:常见坑
  curated       INTEGER NOT NULL DEFAULT 0         -- 1=已归纳带讲解 0=直通(待归纳)
);

CREATE TABLE IF NOT EXISTS attempts(
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id INTEGER NOT NULL,
  result      TEXT NOT NULL,                        -- correct | wrong | fuzzy
  created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_a_q ON attempts(question_id, id);

CREATE TABLE IF NOT EXISTS type_progress(
  type_name  TEXT PRIMARY KEY,
  status     TEXT NOT NULL DEFAULT 'learning',      -- learning | mastered(够了)
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_explain(
  cache_key  TEXT PRIMARY KEY,                       -- T:<题型名> 或 Q:<题id>
  content    TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    return conn


def init_db(conn) -> None:
    conn.executescript(SCHEMA)
    cols = {r[1] for r in conn.execute('PRAGMA table_info(questions)')}
    if 'plain' not in cols:
        conn.execute("ALTER TABLE questions ADD COLUMN plain TEXT NOT NULL DEFAULT ''")
    tcols = {r[1] for r in conn.execute('PRAGMA table_info(types)')}
    for col, ddl in [('intuition', "intuition TEXT NOT NULL DEFAULT ''"),
                     ('example_src', "example_src TEXT NOT NULL DEFAULT ''"),
                     ('example_qid', 'example_qid INTEGER'),
                     ('example_stem', "example_stem TEXT NOT NULL DEFAULT ''"),
                     ('example_steps_json', "example_steps_json TEXT NOT NULL DEFAULT '[]'"),
                     ('variants_json', "variants_json TEXT NOT NULL DEFAULT '[]'"),
                     ('figures_json', "figures_json TEXT NOT NULL DEFAULT '[]'")]:
        if col not in tcols:
            conn.execute('ALTER TABLE types ADD COLUMN ' + ddl)
    conn.commit()

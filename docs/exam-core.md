# 数学主站：以真题为核心

2026-09-29 最新需求：用已抽取的题目文本建立真题与880的具体联系，提供题目与参考答案。解析由用户自行问AI，系统不生成或展示解析。继续使用302主站，题间保持停用。

## 学习流程

从2020—2026年真题开始，作答、核对答案、练相关880题，再返回原题。补练区分同法练习与变式，说明具体对应的方法和小问；不以同章节代替逐题联系。没有足够贴近的练习时明确显示空列表。

题目用文字和LaTeX显示，保留选项、小问和6幅必要题图。原有925道题保持ID，追加4道未编号题，共929道。原始文件保存在content/workbooks，源文件不改写。

“核对答案”只显示参考结果及必要的疑点说明。证明题注明结论见题干，不展示证明过程。答案不确定时停用自动判分。主观题仍由用户核对自评。

## 本次内容范围

- 全部155道核心真题均已检查匹配结果。
- 301条去重后的关联，142道真题有匹配，共涉及226道880练习；13道暂未找到合适匹配。
- 511道880已有可展示的参考答案，其中475道无现有核对疑点；其余带说明。尚未收录的418道明确提示缺失，不使用未经核对的生成稿填充。
- 参考答案复用先前已经完成的核对结果。本次没有调用模型生成答案或解析，也没有新增在线AI功能。
- 已停止原解析生成、复核进程，并禁用三个解析脚本的命令行入口。旧资料保留，不再作为页面讲解或交付要求。

关联复用已有逐对审核结果，并在content/manual-relations.json记录本次补充、修正、弱关联剔除和小问合并。旧模型审核不等于人工全量校对。来源真题和目标题均带内容指纹，题目改变后旧联系不再显示。

## 作答保存

study_sessions区分套卷和补练上下文；study_items存当前答案、演算和自评；study_history保留完成时的快照。revision防止旧页面覆盖新内容，mutation使重试幂等。本机只暂存未同步内容，服务器确认后显示“已保存到服务器”。

旧浏览器的math302-paper-choices-v1自动迁移，只填充空白服务器记录，冲突保留两份。照片和笔记沿用独立接口；用户主动删除照片后历史引用可能失效。内容更新不删除作答、笔记、照片和历史。

## 发布与验证

先用SQLite online backup备份生产库，再进行增量导入。禁止用开发库替换生产库。

```bash
backend/.venv/bin/python scripts/import_workbook.py --apply
backend/.venv/bin/python scripts/publish_exam_links.py --apply
backend/.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
npm --prefix frontend test
node scripts/check_content.cjs
MATH_PYTHON=backend/.venv/bin/python node scripts/test_exam_core.cjs
```

publish_exam_links只更新关联与参考答案，不发布解析。打包时从离线核对结果读取，部署时仅依赖content/relations.json、relation-sources.json和reference-answers.json。内容更新整体事务提交，源或目标指纹失配即停止，不修改学习记录。

公式检查覆盖929道原始题目、参考答案和关联理由。浏览器测试使用独立临时数据库和8304端口，验证跨浏览器恢复、冲突处理、断网续存、重做历史、答案展示、补练返回路径及手机布局。

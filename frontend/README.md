# 数学前端

静态页面直接由项目的前端代理提供。题目笔记保存在后端 SQLite 中，浏览器仅保留未提交的文字草稿。

每道真题和 880 习题的“笔记”旁都有“草稿纸”。支持本机多图上传、手机扫码拍照、放大查看和删除，图片按题目追加保存。手机上传后，打开的电脑弹窗会自动更新。

Markdown、公式和二维码使用本项目自己的依赖，构建产物及许可证保存在 `vendor/`，运行时无需访问外部 CDN。

更新依赖、`markdown.mjs` 或 `qrcode.mjs` 后运行：

```bash
npm ci
npm run build
npm test
```

其余前端文件是直接加载的 JavaScript 和 CSS，无需打包。

后端图片校验依赖 Pillow，部署时在项目根目录运行 `backend/.venv/bin/python -m pip install -r backend/requirements.txt`，并重启数学后端及前端代理。草稿纸原图保存在 `backend/data/drafts/`，备份时需与 `backend/data/study.db` 一起保存。

新增草稿接口如下，原有笔记接口保持不变。`/api/paper`、`/api/type`、`/api/practice` 返回的题目增加 `draft_count`。

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/api/questions/{id}/drafts` | 返回题目信息及按上传顺序排列的 `drafts` |
| POST | `/api/questions/{id}/drafts` | 追加一张图片，返回图片记录 |
| GET / HEAD | `/api/draft-images/{id}` | 查看原图 |
| DELETE | `/api/draft-images/{id}` | 删除一张图片，可安全重试 |
| POST | `/api/questions/{id}/draft-token` | 返回手机上传路径 `path` 和过期时间 `expires_at`（Unix 秒） |
| GET / POST | `/api/draft-upload/{token}` | 手机上传页及单张图片上传 |

上传 JSON 包含 `image_base64`（可带 data URL 前缀）和 `client_id`（16–80 位字母、数字、下划线或连字符）。单张最多 9 MB，支持 JPG、PNG、WebP、GIF。一次上传的重试必须沿用同一个 `client_id`，以免重复保存。

只有手机上传路径免登录，其凭据为绑定题目的随机链接，10 分钟有效，一次成功上传后失效；原请求可以在有效期内重试。它不能读取原有图片、笔记或签发新链接。其他接口沿用前端代理的访问密码验证。

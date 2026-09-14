# 数学前端

静态页面直接由项目的前端代理提供。题目笔记保存在后端 SQLite 中，浏览器仅保留未提交的草稿。

Markdown 和公式库使用本项目自己的依赖，构建产物及许可证保存在 `vendor/`，运行时无需访问外部 CDN。

更新依赖或 `markdown.mjs` 后运行：

```bash
npm ci
npm run build
npm test
```

其余前端文件是直接加载的 JavaScript 和 CSS，无需打包。

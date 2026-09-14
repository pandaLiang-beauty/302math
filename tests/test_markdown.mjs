import assert from 'node:assert/strict';
import test from 'node:test';
import { render } from '../frontend/markdown.mjs';

test('math notes support triple and double highlights with nested Markdown', () => {
  assert.match(render('===**重点**===，==易错点=='), /<mark><strong>重点<\/strong><\/mark>，<mark>易错点<\/mark>/);
  assert.match(render('**===重点===**'), /<strong><mark>重点<\/mark><\/strong>/);
  assert.doesNotMatch(render('===未匹配=='), /<mark>/);
});

test('formulas preserve TeX and render integral and subscript notation', () => {
  const html = render('# 解法\n\n$$\\int_0^1 x^2\\,dx=\\frac13$$\n\n$x_1+y_2$');
  assert.match(html, /<h1>解法<\/h1>/);
  assert.match(html, /class="katex-display"/);
  assert.match(html, /class="katex"/);
  assert.doesNotMatch(html, /<em>/);
});

test('lists, tables, code and existing plain-text newlines render correctly', () => {
  const html = render('第一步\n第二步\n\n- [x] 化简\n\n| 方法 | 结论 |\n| --- | --- |\n| 代换 | 正确 |\n\n```js\na === b\n```');
  assert.match(html, /第一步<br>\n第二步/);
  assert.match(html, /type="checkbox"/); assert.match(html, /<table>/);
  assert.match(html, /a === b/); assert.doesNotMatch(html, /<mark>/);
});

test('HTML and script URLs in notes stay inert and escaped highlight/code stay literal', () => {
  const html = render('<img src=x onerror=alert(1)>\n\n[x](javascript:alert(1))\n\n$\\href{javascript:alert(1)}{x}$\n\n`===代码===`\n\n\\=\\=\\=原文\\=\\=\\=');
  assert.doesNotMatch(html, /<img|href="javascript:|<mark>/);
  assert.match(html, /&lt;img/);
});

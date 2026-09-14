import { build } from 'esbuild';
import { cp, mkdir } from 'node:fs/promises';

await mkdir('vendor/katex', { recursive: true });
await build({ entryPoints: ['markdown.mjs'], outfile: 'vendor/markdown.js', bundle: true,
  format: 'iife', globalName: 'MathMarkdown', minify: true, legalComments: 'linked', target: 'es2022' });
await cp('node_modules/katex/dist/katex.min.css', 'vendor/katex/katex.min.css');
await cp('node_modules/katex/dist/fonts', 'vendor/katex/fonts', { recursive: true });
for (const name of ['katex', 'markdown-it', 'markdown-it-task-lists', '@mdit/plugin-tex']) {
  await cp('node_modules/' + name + '/LICENSE', 'vendor/' + name.replaceAll('/', '-') + '-LICENSE');
}
console.log('Built local Markdown and math assets.');

import MarkdownIt from 'markdown-it';
import taskLists from 'markdown-it-task-lists';
import { tex } from '@mdit/plugin-tex';
import katex from 'katex';
import renderMathInElement from 'katex/contrib/auto-render';

function highlights(md) {
  const markers = new Set([0xE102, 0xE103]);
  md.inline.ruler.before('emphasis', 'study_highlight', (state, silent) => {
    if (silent || state.src[state.pos] !== '=') return false;
    const run = state.scanDelims(state.pos, true);
    if (run.length !== 2 && run.length !== 3) return false;
    const token = state.push('text', '', 0);
    token.content = '='.repeat(run.length);
    state.delimiters.push({ marker: 0xE100 + run.length, length: 0, token: state.tokens.length - 1,
      end: -1, open: run.can_open, close: run.can_close });
    state.pos += run.length;
    return true;
  });
  md.inline.ruler2.before('emphasis', 'study_highlight', state => {
    const groups = [state.delimiters, ...state.tokens_meta.flatMap(meta => meta?.delimiters ? [meta.delimiters] : [])];
    for (const delimiters of groups) for (const opening of delimiters) {
      if (!markers.has(opening.marker) || opening.end < 0) continue;
      const closing = delimiters[opening.end];
      for (const [position, nesting] of [[opening.token, 1], [closing.token, -1]]) {
        Object.assign(state.tokens[position], { type: nesting === 1 ? 'mark_open' : 'mark_close', tag: 'mark', nesting, content: '' });
      }
    }
  });
}

const parser = new MarkdownIt({ html: false, breaks: true, linkify: true })
  .use(highlights).use(taskLists).use(tex, { delimiters: 'all', mathFence: true,
    render: (formula, displayMode) => katex.renderToString(formula, { displayMode, throwOnError: false, trust: false, strict: 'ignore' }) });

export function render(source = '') { return parser.render(String(source || '')); }
export function renderMath(element, options) {
  renderMathInElement(element, { ...options, trust: false, ignoredClasses: ['note-markdown', 'note-editor'] });
}

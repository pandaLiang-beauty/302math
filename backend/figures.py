# -*- coding: utf-8 -*-
"""把「画区域」这一步真的画出来:按真实区域采样,生成内联 SVG 数学图。

不是插画,是坐标图——坐标轴 + 边界曲线 + 阴影区域 + θ 角标 + 分界线 + 切片箭头。
在 Python 里算好路径存进库,前端直接 innerHTML,零依赖、可缩放。
"""
import math

C_AX = '#8a919a'          # 坐标轴
C_MAIN = '#2f6feb'        # 主边界
C_ALT = '#1a7f37'         # 次边界 / 新次序
C_BAD = '#cf222e'         # 错的次序 / 坑
C_DASH = '#9aa3ad'        # 辅助线
FILL = 'rgba(47,111,235,.14)'
FILL2 = 'rgba(26,127,55,.15)'
FILL3 = 'rgba(178,80,0,.13)'


# ---------- 采样器:给区域/曲线算点列 ----------
def curve(f, x1, x2, n=90):
    """y=f(x) 上的点列。"""
    return [(x1 + (x2 - x1) * i / n, f(x1 + (x2 - x1) * i / n)) for i in range(n + 1)]


def param(fx, fy, t1, t2, n=120):
    """参数曲线 (fx(t), fy(t))。"""
    return [(fx(t1 + (t2 - t1) * i / n), fy(t1 + (t2 - t1) * i / n)) for i in range(n + 1)]


def polar(fr, a1, a2, n=120):
    """极坐标曲线 r=fr(θ),θ 用弧度。"""
    return [(fr(a) * math.cos(a), fr(a) * math.sin(a))
            for a in (a1 + (a2 - a1) * i / n for i in range(n + 1))]


def vslice(lo, hi, x1, x2, n=90):
    """竖切区域 lo(x)≤y≤hi(x) 的闭合边界。"""
    return curve(lo, x1, x2, n) + curve(hi, x2, x1, n)


def polar_region(r_in, r_out, a1, a2, n=120):
    """极坐标区域 r_in(θ)≤r≤r_out(θ) 的闭合边界。"""
    return polar(r_out, a1, a2, n) + polar(r_in, a2, a1, n)


# ---------- 图元 ----------
def axes(xlab='x', ylab='y', ticks=()):
    return {'k': 'axes', 'xlab': xlab, 'ylab': ylab, 'ticks': list(ticks)}


def shade(pts, fill=FILL, label=''):
    return {'k': 'shade', 'pts': pts, 'fill': fill, 'label': label}


def line(pts, color=C_MAIN, dash=False, lw=1.6, label='', lat=None):
    return {'k': 'line', 'pts': pts, 'color': color, 'dash': dash, 'lw': lw,
            'label': label, 'lat': lat}


def seg(p1, p2, **kw):
    return line([p1, p2], **kw)


def sector(r, a1, a2, label='', color=C_BAD):
    return {'k': 'sector', 'r': r, 'a1': a1, 'a2': a2, 'label': label, 'color': color}


def ray(a, r1, r2, label='', color=C_BAD):
    """从 r1 到 r2 沿角度 a 的箭头,表示"沿这条射线 r 从…到…"。"""
    return {'k': 'ray', 'a': a, 'r1': r1, 'r2': r2, 'label': label, 'color': color}


def arrow(p1, p2, color=C_ALT, label='', dash=False):
    return {'k': 'arrow', 'p1': p1, 'p2': p2, 'color': color, 'label': label, 'dash': dash}


def text(at, s, color='#1f2328', size=12.5, anchor='middle', weight='400'):
    return {'k': 'text', 'at': at, 's': s, 'color': color, 'size': size,
            'anchor': anchor, 'weight': weight}


def dot(at, label='', color=C_MAIN):
    return {'k': 'dot', 'at': at, 'label': label, 'color': color}


def grid(x1, x2, y1, y2, n):
    return {'k': 'grid', 'box': (x1, x2, y1, y2), 'n': n}


# ---------- 渲染 ----------
def _esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def fig(xr, yr, items, w=330, caption='', pad=26):
    """生成一张 SVG。xr/yr 是数学坐标范围,自动等比映射(不变形)。"""
    x1, x2 = xr
    y1, y2 = yr
    span = max(x2 - x1, y2 - y1)
    inner = w - 2 * pad
    k = inner / span                      # 每单位数学长度的像素
    h = int(round((y2 - y1) * k + 2 * pad))

    def X(x):
        return pad + (x - x1) * k

    def Y(y):
        return h - pad - (y - y1) * k

    def P(pts):
        return ' '.join('%.2f,%.2f' % (X(a), Y(b)) for a, b in pts)

    o = ['<svg class="mfig" viewBox="0 0 %d %d" width="%d" height="%d" '
         'xmlns="http://www.w3.org/2000/svg" role="img">' % (w, h, w, h),
         '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
         'markerHeight="6" orient="auto-start-reverse">'
         '<path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>']
    for it in items:
        kk = it['k']
        if kk == 'grid':
            gx1, gx2, gy1, gy2, n = it['box'] + (it['n'],)
            for i in range(n + 1):
                gx = gx1 + (gx2 - gx1) * i / n
                gy = gy1 + (gy2 - gy1) * i / n
                o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#dfe3e8" '
                         'stroke-width=".7"/>' % (X(gx), Y(gy1), X(gx), Y(gy2)))
                o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#dfe3e8" '
                         'stroke-width=".7"/>' % (X(gx1), Y(gy), X(gx2), Y(gy)))
        elif kk == 'axes':
            o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.1" '
                     'marker-end="url(#ah)"/>' % (X(x1), Y(0), X(x2), Y(0), C_AX))
            o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.1" '
                     'marker-end="url(#ah)"/>' % (X(0), Y(y1), X(0), Y(y2), C_AX))
            o.append('<text x="%.2f" y="%.2f" font-size="12" fill="%s" font-style="italic">%s</text>'
                     % (X(x2) - 2, Y(0) + 15, C_AX, _esc(it['xlab'])))
            o.append('<text x="%.2f" y="%.2f" font-size="12" fill="%s" font-style="italic">%s</text>'
                     % (X(0) - 14, Y(y2) + 10, C_AX, _esc(it['ylab'])))
            for (tx, ty, lb) in it['ticks']:
                o.append('<text x="%.2f" y="%.2f" font-size="11" fill="%s" text-anchor="middle">%s</text>'
                         % (X(tx), Y(ty), C_AX, _esc(lb)))
        elif kk == 'shade':
            o.append('<polygon points="%s" fill="%s" stroke="none"/>' % (P(it['pts']), it['fill']))
        elif kk == 'line':
            o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f"%s '
                     'stroke-linejoin="round"/>'
                     % (P(it['pts']), it['color'], it['lw'],
                        ' stroke-dasharray="5 4"' if it['dash'] else ''))
            if it['label']:
                ax, ay = it['lat'] or it['pts'][len(it['pts']) // 2]
                o.append('<text x="%.2f" y="%.2f" font-size="11.5" fill="%s" text-anchor="middle">%s</text>'
                         % (X(ax), Y(ay), it['color'], _esc(it['label'])))
        elif kk == 'sector':
            r, a1, a2 = it['r'], it['a1'], it['a2']
            o.append('<path d="M %.2f %.2f L %.2f %.2f A %.2f %.2f 0 0 0 %.2f %.2f Z" '
                     'fill="none" stroke="%s" stroke-width="1.3"/>'
                     % (X(0), Y(0), X(r * math.cos(a1)), Y(r * math.sin(a1)), r * k, r * k,
                        X(r * math.cos(a2)), Y(r * math.sin(a2)), it['color']))
            if it['label']:
                am = (a1 + a2) / 2
                o.append('<text x="%.2f" y="%.2f" font-size="12" fill="%s" text-anchor="middle" '
                         'font-weight="600">%s</text>'
                         % (X(r * 1.5 * math.cos(am)), Y(r * 1.5 * math.sin(am)) + 4,
                            it['color'], _esc(it['label'])))
        elif kk == 'ray':
            a, r1, r2 = it['a'], it['r1'], it['r2']
            o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.5" '
                     'marker-end="url(#ah)"/>'
                     % (X(r1 * math.cos(a)), Y(r1 * math.sin(a)), X(r2 * math.cos(a)),
                        Y(r2 * math.sin(a)), it['color']))
            if it['label']:
                rm = (r1 + r2) / 2
                o.append('<text x="%.2f" y="%.2f" font-size="11.5" fill="%s" text-anchor="middle">%s</text>'
                         % (X(rm * math.cos(a)), Y(rm * math.sin(a)) - 5, it['color'], _esc(it['label'])))
        elif kk == 'arrow':
            (ax1, ay1), (ax2, ay2) = it['p1'], it['p2']
            o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="1.5"%s '
                     'marker-end="url(#ah)"/>'
                     % (X(ax1), Y(ay1), X(ax2), Y(ay2), it['color'],
                        ' stroke-dasharray="4 3"' if it['dash'] else ''))
            if it['label']:
                o.append('<text x="%.2f" y="%.2f" font-size="11.5" fill="%s" text-anchor="middle">%s</text>'
                         % (X((ax1 + ax2) / 2), Y((ay1 + ay2) / 2) - 5, it['color'], _esc(it['label'])))
        elif kk == 'text':
            o.append('<text x="%.2f" y="%.2f" font-size="%.1f" fill="%s" text-anchor="%s" '
                     'font-weight="%s">%s</text>'
                     % (X(it['at'][0]), Y(it['at'][1]), it['size'], it['color'],
                        it['anchor'], it['weight'], _esc(it['s'])))
        elif kk == 'dot':
            o.append('<circle cx="%.2f" cy="%.2f" r="3" fill="%s"/>'
                     % (X(it['at'][0]), Y(it['at'][1]), it['color']))
            if it['label']:
                o.append('<text x="%.2f" y="%.2f" font-size="11" fill="%s" text-anchor="start">%s</text>'
                         % (X(it['at'][0]) + 6, Y(it['at'][1]) - 5, it['color'], _esc(it['label'])))
    o.append('</svg>')
    svg = ''.join(o)
    if caption:
        return '<figure class="mfigw">%s<figcaption>%s</figcaption></figure>' % (svg, _esc(caption))
    return '<figure class="mfigw">%s</figure>' % svg

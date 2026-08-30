# -*- coding: utf-8 -*-
"""「重积分的计算」12 个题型的数学图:每张都画母题的真实区域。
每个套路的第一步都是"画区域",这些图就是那一步。"""
import math as M
import figures as F

pi = M.pi
FIGS = {}


def _c(cx, cy, r):
    return F.param(lambda t: cx + r * M.cos(t), lambda t: cy + r * M.sin(t), 0, 2 * pi)


# ---- T1 极坐标·单一边界(2020#19:1≤x≤2, 0≤y≤x)----
FIGS['极坐标·单一边界'] = [F.fig(
    (-0.3, 2.6), (-0.35, 2.35), [
        F.axes(ticks=[(1, -0.16, '1'), (2, -0.16, '2')]),
        F.shade([(1, 0), (2, 0), (2, 2), (1, 1)]),
        F.seg((1, 0), (1, 1), label='x=1 → r=secθ', lat=(0.62, 1.15)),
        F.seg((2, 0), (2, 2), label='x=2 → r=2secθ', lat=(2.0, 2.15)),
        F.seg((0, 0), (2.25, 2.25), color=F.C_DASH, dash=True, lw=1.2,
              label='y=x', lat=(0.55, 0.72)),
        F.sector(0.5, 0, pi / 4, label='θ∈[0,π/4]'),
        F.ray(0.5, 1 / M.cos(0.5), 2 / M.cos(0.5), label='r'),
        F.text((1.55, 0.45), 'D', size=15, weight='700'),
    ], caption='θ 被 x 轴与 y=x 夹住;沿任一射线,r 从 secθ 走到 2secθ——一段,不分叉')]

# ---- T2 极坐标·分段边界(2025#20:两圆 x²+y²≤4x 与 ≤4y)----
FIGS['极坐标·分段边界'] = [F.fig(
    (-0.5, 4.6), (-0.5, 4.6), [
        F.axes(),
        F.shade(F.polar(lambda a: 4 * M.sin(a), 0, pi / 4)
                + F.polar(lambda a: 4 * M.cos(a), pi / 4, pi / 2)),
        F.line(F.polar(lambda a: 4 * M.cos(a), 0, pi / 2), color=F.C_DASH, dash=True, lw=1.1,
               label='x²+y²=4x  (r=4cosθ)', lat=(3.05, 2.35)),
        F.line(F.polar(lambda a: 4 * M.sin(a), 0, pi / 2), color=F.C_ALT, dash=True, lw=1.1,
               label='x²+y²=4y  (r=4sinθ)', lat=(1.28, 4.25)),
        F.seg((0, 0), (3.2, 3.2), color=F.C_BAD, dash=True, lw=1.3,
              label='θ=π/4 分界', lat=(2.55, 3.0)),
        F.ray(0.45, 0, 4 * M.sin(0.45), label='r≤4sinθ', color=F.C_ALT),
        F.ray(1.12, 0, 4 * M.cos(1.12), label='r≤4cosθ'),
        F.dot((2, 2), label='(2,2)'),
        F.text((1.15, 1.0), 'D', size=15, weight='700'),
    ], caption='取交集 → r 上限取两者中较小的那个;π/4 两侧换人,必须分段')]

# ---- T3 直角坐标·选序(2026#20:单位正方形)----
FIGS['直角坐标·选序计算'] = [F.fig(
    (-0.3, 1.5), (-0.3, 1.5), [
        F.axes(ticks=[(1, -0.14, '1')]),
        F.shade([(0, 0), (1, 0), (1, 1), (0, 1)]),
        F.line([(1, 0), (1, 1), (0, 1)]),
        F.arrow((0.58, 0.02), (0.58, 0.98), label='先积 y'),
        F.text((0.58, -0.2), 'x 固定', color=F.C_ALT, size=11.5),
        F.text((0.26, 0.45), 'D', size=15, weight='700'),
    ], caption='被积含 y·(1+x²+y²)^(−3/2):对 y 是凑微分 → 先积 y,再积 x')]

# ---- T4 对称性化简(2014#16:第一象限 1≤r≤2 四分圆环)----
FIGS['对称性化简'] = [F.fig(
    (-0.35, 2.4), (-0.35, 2.4), [
        F.axes(ticks=[(1, -0.16, '1'), (2, -0.16, '2')]),
        F.shade(F.polar_region(lambda a: 1, lambda a: 2, 0, pi / 2)),
        F.line(F.polar(lambda a: 2, 0, pi / 2), label='r=2', lat=(1.62, 1.62)),
        F.line(F.polar(lambda a: 1, 0, pi / 2), label='r=1', lat=(0.62, 0.62)),
        F.seg((0, 0), (2.3, 2.3), color=F.C_BAD, dash=True, lw=1.3,
              label='y=x 对称轴', lat=(2.0, 2.22)),
        F.arrow((1.72, 0.62), (0.62, 1.72), color=F.C_BAD, dash=True, label='x↔y'),
        F.text((1.35, 0.32), 'D', size=15, weight='700'),
    ], caption='D 关于 y=x 对称 → 把 x/(x+y) 换成 y/(x+y) 后相加,分母被消掉')]

# ---- T5 累次积分换序(880-7:0≤x≤y≤1)----
FIGS['累次积分换序'] = [F.fig(
    (-0.3, 1.5), (-0.3, 1.55), [
        F.axes(ticks=[(1, -0.14, '1')]),
        F.shade([(0, 0), (1, 1), (0, 1)]),
        F.seg((0, 0), (1.15, 1.15), label='y=x', lat=(1.02, 0.86)),
        F.seg((0, 1), (1, 1), label='y=1', lat=(0.62, 1.12)),
        F.arrow((0.32, 0.34), (0.32, 0.97), color=F.C_BAD, dash=True,
                label='原序:先积 y ✗ e^(−y²) 积不出'),
        F.arrow((0.02, 0.72), (0.70, 0.72), color=F.C_ALT, label='换序:先积 x ✓'),
        F.text((0.2, 0.55), 'D', size=15, weight='700'),
    ], caption='同一片三角形,横着切就能积:∫₀¹e^(−y²)(∫₀^y x²dx)dy')]

# ---- T6 累次积分化极坐标(2026#17:y≥|x| 且 r≤√2)----
_R2 = M.sqrt(2)
FIGS['累次积分化极坐标'] = [F.fig(
    (-1.75, 1.75), (-0.35, 1.8), [
        F.axes(),
        F.shade(F.polar_region(lambda a: 0, lambda a: _R2, pi / 4, 3 * pi / 4)),
        F.line(F.polar(lambda a: _R2, pi / 4, 3 * pi / 4), label='x²+y²=2  (r=√2)',
               lat=(0.0, 1.62)),
        F.seg((0, 0), (1.2, 1.2), color=F.C_DASH, dash=True, lw=1.2,
              label='y=x', lat=(1.35, 1.1)),
        F.seg((0, 0), (-1.2, 1.2), color=F.C_DASH, dash=True, lw=1.2,
              label='y=−x', lat=(-1.38, 1.1)),
        F.sector(0.42, pi / 4, 3 * pi / 4, label='π/4 ≤ θ ≤ 3π/4'),
        F.text((0, 0.72), 'D', size=15, weight='700'),
    ], caption='下界 y=|x| 是两条 45° 射线,上界是圆 → 极坐标里变量彻底分离')]

# ---- T7 绝对值/分段(2008#17:正方形被 xy=1 切开)----
_hy = F.curve(lambda x: 1.0 / x, 0.5, 2, 80)
FIGS['绝对值与分段被积函数'] = [F.fig(
    (-0.3, 2.45), (-0.3, 2.45), [
        F.axes(ticks=[(0.5, -0.15, '½'), (2, -0.15, '2')]),
        F.shade([(0, 0), (2, 0), (2, 0.5)] + list(reversed(_hy)) + [(0.5, 2), (0, 2)]),
        F.shade(_hy + [(2, 2), (0.5, 2)], fill=F.FILL3),
        F.line(_hy, color=F.C_BAD, lw=1.8, label='xy=1 变脸线', lat=(1.5, 0.85)),
        F.line([(2, 0), (2, 2), (0, 2)], color=F.C_DASH, lw=1.2),
        F.text((0.62, 0.42), 'max=1', size=12, weight='700'),
        F.text((1.4, 1.62), 'max=xy', size=12, weight='700', color='#8a5000'),
    ], caption='令 xy=1(两个候选相等)解出变脸线,把区域切成两块,各自去掉 max')]

# ---- T8 一般换元:两张图(2024#17)----
_b1 = F.curve(lambda x: 1 / (3 * x), 1 / 3.0, 1, 60)          # xy=1/3
_b2 = F.curve(lambda x: x / 3.0, 1, 3, 40)                    # y=x/3
_b3 = F.curve(lambda x: 3 / x, 3, 1, 60)                      # xy=3
_b4 = F.curve(lambda x: 3 * x, 1, 1 / 3.0, 40)                # y=3x
FIGS['一般换元(雅可比)'] = [
    F.fig((-0.3, 3.6), (-0.3, 3.6), [
        F.axes(),
        F.shade(_b1 + _b2 + _b3 + _b4),
        F.line(_b1, label='xy=1/3', lat=(0.42, 0.42)),
        F.line(_b3, label='xy=3', lat=(1.95, 1.95)),
        F.line(_b2, color=F.C_ALT, label='y=x/3', lat=(2.75, 0.72)),
        F.line(_b4, color=F.C_ALT, label='y=3x', lat=(0.78, 2.75)),
        F.dot((1 / 3.0, 1)), F.dot((1, 3)), F.dot((3, 1)), F.dot((1, 1 / 3.0)),
        F.text((1.15, 1.05), 'D', size=15, weight='700'),
    ], caption='xy 平面:四条边界是「同形不同常数」的两组曲线'),
    F.fig((-0.3, 3.6), (-0.3, 3.6), [
        F.axes(xlab='u', ylab='v', ticks=[(1 / 3.0, -0.16, '⅓'), (3, -0.16, '3')]),
        F.shade([(1 / 3.0, 1 / 3.0), (3, 1 / 3.0), (3, 3), (1 / 3.0, 3)], fill=F.FILL2),
        F.line([(1 / 3.0, 1 / 3.0), (3, 1 / 3.0), (3, 3), (1 / 3.0, 3), (1 / 3.0, 1 / 3.0)],
               color=F.C_ALT),
        F.text((1.65, 1.5), 'u,v 平面', size=13, weight='700', color=F.C_ALT),
        F.text((1.65, 0.05), 'u=xy', size=11.5, color=F.C_ALT),
    ], caption='令 u=xy, v=y/x 后变成正方形 [⅓,3]²,代价是 dxdy = dudv/(2v)'),
]

# ---- T9 含参变限(2008#4:圆环 1≤r≤u, 0≤θ≤v)----
_v = 2.0
FIGS['含参变限二重积分'] = [F.fig(
    (-2.6, 2.6), (-0.4, 2.7), [
        F.axes(),
        F.shade(F.polar_region(lambda a: 1, lambda a: 2, 0, _v)),
        F.line(F.polar(lambda a: 2, 0, _v), label='r=u', lat=(1.5, 1.62)),
        F.line(F.polar(lambda a: 1, 0, _v), label='r=1', lat=(0.5, 0.68)),
        F.line(F.polar(lambda a: 2.45, 0, _v), color=F.C_BAD, dash=True, lw=1.2,
               label='u 增大', lat=(1.85, 2.05)),
        F.arrow((2.02, 0.06), (2.42, 0.06), color=F.C_BAD),
        F.seg((0, 0), (2.45 * M.cos(_v), 2.45 * M.sin(_v)), color=F.C_DASH, dash=True, lw=1.2),
        F.sector(0.55, 0, _v, label='θ≤v'),
        F.text((1.15, 0.62), 'D(u,v)', size=13, weight='700'),
    ], caption='参数 u 只落在 r 的上限上 → 先压成 v·∫₁^u f(r²)dr,再对上限求导')]

# ---- T10 含∬的方程(2020#18:上半单位圆盘)----
FIGS['含二重积分的方程'] = [F.fig(
    (-1.5, 1.5), (-0.35, 1.55), [
        F.axes(ticks=[(1, -0.15, '1'), (-1, -0.15, '−1')]),
        F.shade(F.polar_region(lambda a: 0, lambda a: 1, 0, pi)),
        F.line(F.polar(lambda a: 1, 0, pi), label='x²+y²=1', lat=(0.0, 1.18)),
        F.seg((0, -0.2), (0, 1.35), color=F.C_BAD, dash=True, lw=1.3),
        F.text((0.72, 0.68), '∬x = 0', color=F.C_BAD, size=12.5, weight='700'),
        F.text((-0.62, 0.42), 'D 固定 → ∬f 是常数 A', color=F.C_ALT, size=11),
        F.text((0, 0.28), 'D', size=15, weight='700'),
    ], caption='D 固定 ⇒ ∬f 只是个数,设成 A;再靠 y 轴对称让含 A 的项归零')]

# ---- T11 和式极限(2010#6:单位正方形上的 n×n 网格)----
_n = 6
FIGS['和式极限化二重积分'] = [F.fig(
    (-0.32, 1.5), (-0.32, 1.5), [
        F.shade([(0, 0), (1, 0), (1, 1), (0, 1)]),
        F.grid(0, 1, 0, 1, _n),
        F.axes(ticks=[(1, -0.15, '1')]),
        F.line([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], lw=1.4),
        F.dot((4 / 6.0, 3 / 6.0), label='(i/n, j/n)', color=F.C_BAD),
        F.text((0.5, 1.22), '每格面积 = 1/n × 1/n', size=11.5, color=F.C_ALT),
    ], caption='双重和的 1/n² 就是网格面积 → 直接抄成 ∫₀¹∫₀¹ f(x,y)dxdy')]

# ---- T12 比较大小:两张图(2019#5)----
_h = pi / 2
FIGS['二重积分比较大小'] = [
    F.fig((-2.0, 2.0), (-2.0, 2.0), [
        F.axes(),
        F.shade([(_h, 0), (0, _h), (-_h, 0), (0, -_h)]),
        F.line([(_h, 0), (0, _h), (-_h, 0), (0, -_h), (_h, 0)], label='|x|+|y|=π/2',
               lat=(1.05, 1.05)),
        F.line(_c(0, 0, _h), color=F.C_BAD, dash=True, lw=1.1),
        F.dot((_h, 0), label='r=π/2', color=F.C_BAD),
        F.text((0, 0.12), 'D', size=15, weight='700'),
    ], caption='区域完全相同 → 不用算,只需知道 r 的范围:0 ≤ r ≤ π/2(顶点处最大)'),
    F.fig((-0.3, 1.95), (-0.3, 1.95), [
        F.axes(xlab='r', ylab='', ticks=[(_h, -0.16, 'π/2')]),
        F.line(F.curve(lambda x: x, 0, _h), label='r', lat=(1.42, 1.62)),
        F.line(F.curve(M.sin, 0, _h), color=F.C_ALT, label='sin r', lat=(1.05, 1.12)),
        F.line(F.curve(lambda x: 1 - M.cos(x), 0, _h), color='#b25000',
               label='1−cos r', lat=(1.18, 0.42)),
        F.seg((_h, 0), (_h, 1.62), color=F.C_DASH, dash=True, lw=1.1),
        F.dot((_h, 1)),
    ], caption='在 (0, π/2) 上恒有 1−cos r < sin r < r ⇒ I₃ < I₂ < I₁'),
]




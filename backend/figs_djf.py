# -*- coding: utf-8 -*-
"""「定积分的应用」4 个题型的数学图(母题的真实图形)。"""
import math as M
import figures as F

pi = M.pi
FIGS = {}

# ---- 平面图形面积(2012#12:y=4/x, y=x, y=4x 第一象限)----
FIGS['平面图形面积'] = [F.fig(
    (-0.35, 2.9), (-0.5, 4.8), [
        F.axes(ticks=[(1, -0.28, '1'), (2, -0.28, '2')]),
        F.shade(F.curve(lambda x: x, 0, 2) + F.curve(lambda x: 4 / x, 2, 1)
                + F.curve(lambda x: 4 * x, 1, 0)),
        F.line(F.curve(lambda x: 4 / x, 0.88, 2.85), label='y=4/x', lat=(2.42, 1.95)),
        F.line(F.curve(lambda x: x, 0, 2.55), color=F.C_ALT, label='y=x', lat=(2.32, 2.62)),
        F.line(F.curve(lambda x: 4 * x, 0, 1.16), color=F.C_ALT, label='y=4x', lat=(0.72, 4.35)),
        F.seg((1, 0), (1, 4), color=F.C_BAD, dash=True, lw=1.2,
              label='x=1 分段', lat=(1.42, 3.42)),
        F.dot((1, 4), label='(1,4)'), F.dot((2, 2), label='(2,2)'),
        F.text((1.02, 1.5), 'S', size=15, weight='700'),
    ], caption='交点必须解出来:x=1 处上边界从 y=4x 换成 y=4/x → 必须分两段')]

# ---- 旋转体体积(2011#12:y=√(x²−1), x=2, x 轴)----
_S3 = M.sqrt(3)
FIGS['旋转体体积'] = [F.fig(
    (-0.35, 2.7), (-0.4, 2.3), [
        F.axes(ticks=[(1, -0.2, '1'), (2, -0.2, '2')]),
        F.shade(F.curve(lambda x: M.sqrt(max(x * x - 1, 0)), 1, 2) + [(2, 0), (1, 0)]),
        F.line(F.curve(lambda x: M.sqrt(max(x * x - 1, 0)), 1, 2.35),
               label='y=√(x²−1)', lat=(1.62, 1.62)),
        F.seg((2, 0), (2, _S3), color=F.C_DASH, dash=True, lw=1.2, label='x=2', lat=(2.28, 0.9)),
        F.seg((1.62, 0), (1.62, M.sqrt(1.62 ** 2 - 1)), color=F.C_BAD, lw=2.2),
        F.text((1.62, -0.28), 'dx', color=F.C_BAD, size=11.5),
        F.text((0.98, 0.72), 'R=y(x)', color=F.C_BAD, size=11.5, anchor='end'),
        F.dot((1, 0)), F.dot((2, _S3)),
    ], caption='切片垂直于转轴 → 圆盘法:每片体积 πy²dx,V=π∫₁²(x²−1)dx = 4π/3')]

# ---- 弧长(2011#9:y=∫₀ˣ tan t dt, 0≤x≤π/4)----
_y = lambda x: -M.log(M.cos(x))
_x0, _dx = 0.46, 0.20
_y0 = _y(_x0)
_dy = M.tan(_x0) * _dx
FIGS['弧长'] = [F.fig(
    (-0.12, 1.02), (-0.14, 0.62), [
        F.axes(ticks=[(pi / 4, -0.075, 'π/4')]),
        F.line(F.curve(_y, 0, pi / 4), lw=2.2, label='y=∫₀ˣ tan t dt', lat=(0.3, 0.33)),
        F.seg((_x0, _y0), (_x0 + _dx, _y0), color=F.C_ALT, lw=1.5),
        F.seg((_x0 + _dx, _y0), (_x0 + _dx, _y0 + _dy), color=F.C_ALT, lw=1.5),
        F.seg((_x0, _y0), (_x0 + _dx, _y0 + _dy), color=F.C_BAD, lw=2),
        F.text((_x0 + _dx / 2, _y0 - 0.045), 'dx', color=F.C_ALT, size=11.5),
        F.text((_x0 + _dx + 0.055, _y0 + _dy / 2), 'dy', color=F.C_ALT, size=11.5),
        F.text((_x0 + 0.015, _y0 + _dy + 0.035), 'ds', color=F.C_BAD, size=12, weight='700',
               anchor='start'),
        F.seg((pi / 4, 0), (pi / 4, _y(pi / 4)), color=F.C_DASH, dash=True, lw=1.1),
    ], caption='ds=√(dx²+dy²)=√(1+y′²)dx;y 由变限积分给出 ⇒ y′=tan x 直接由牛顿-莱布尼茨读出')]

# ---- 物理/其他应用(2014#13:细棒 [0,1],ρ(x)=−x²+2x+1,求质心)----
_rho = lambda x: -x * x + 2 * x + 1
FIGS['物理/其他应用'] = [F.fig(
    (-0.18, 1.35), (-0.5, 2.5), [
        F.axes(ticks=[(1, -0.36, '1')]),
        F.shade(F.curve(_rho, 0, 1) + [(1, 0), (0, 0)]),
        F.line(F.curve(_rho, 0, 1.12), label='ρ(x)=−x²+2x+1', lat=(0.62, 2.28)),
        F.seg((0, -0.22), (1, -0.22), color='#57606a', lw=5),
        F.text((-0.05, -0.22), '棒', size=11.5, color='#57606a', anchor='end'),
        F.seg((0.62, 0), (0.62, _rho(0.62)), color=F.C_BAD, lw=2.2),
        F.text((0.62, _rho(0.62) + 0.14), 'dm=ρ(x)dx', color=F.C_BAD, size=11.5),
        F.dot((0.55, -0.22), label='x̄=11/20', color=F.C_ALT),
    ], caption='元素法:先写一个微元的贡献 dm=ρdx,再 x̄ = ∫xρdx / ∫ρdx = (11/12)/(5/3) = 11/20')]


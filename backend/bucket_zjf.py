# -*- coding: utf-8 -*-
"""知识点桶「重积分的计算」→ 12 个方法级题型(逐题人工归类 + 讲解)。

归类不走正则猜:真题按 年#题号、880 按题号(463–540)人工钉死,
因为方法级精度只能逐题读出来。判据同前:一个通用方法概括不了就拆成两个题型。
"""
import re

POINT = '重积分的计算'
SUBJECT, CHAPTER = '高等数学', '多元函数积分学'

T1 = '极坐标·单一边界'
T2 = '极坐标·分段边界'
T3 = '直角坐标·选序计算'
T4 = '对称性化简'
T5 = '累次积分换序'
T6 = '累次积分化极坐标'
T7 = '绝对值与分段被积函数'
T8 = '一般换元(雅可比)'
T9 = '含参变限二重积分'
T10 = '含二重积分的方程'
T11 = '和式极限化二重积分'
T12 = '二重积分比较大小'

ORDER = [T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12]

# ---- 数二越界 / 归错桶 ----
RE_TRIPLE = r'∭|dxdydz|三重积分'                      # 三重积分:数二不考 → 删
RE_MOVE_DJF = r'的面积|旋转体的体积'                    # 求面积/旋转体体积 → 其实属「定积分的应用」


def is_triple(stem):
    return bool(re.search(RE_TRIPLE, stem or ''))


def is_misfiled(stem):
    s = stem or ''
    return bool(re.search(RE_MOVE_DJF, s)) and not re.search(r'二重积分|∬', s)


# ---- 真题:年#题号 → 题型。值为 str,或 [(正则, 题型), ...] 用题干消歧(同号多题) ----
MAP_REAL = {
    '2008#4': T9, '2008#6': T9, '2008#11': T4, '2008#17': T7, '2008#18': T7,
    '2009#17': T1, '2009#19': T1,
    '2010#6': T11, '2010#16': T4, '2010#20': T3,
    '2011#13': T1,
    '2011#19': [(r'f′\(x\+y\)|Dt|f\(t\)dxdy', T9), ('', T3)],
    '2011#21': T3,
    '2012#6': T4, '2012#16': T3, '2012#18': T1,
    '2013#3': T12, '2013#17': T3,
    '2014#16': T4, '2014#17': T4,
    '2015#3': T2, '2015#16': T4, '2015#18': T4,
    '2016#3': T12, '2016#12': T3, '2016#15': T1, '2016#18': T1,
    '2017#16': T3, '2017#20': T1,
    '2018#6': T4, '2018#16': T3, '2018#17': T3,
    '2019#5': T12, '2019#18': T1,
    '2020#18': T10, '2020#19': T1,
    '2021#21': T1,
    '2022#14': T3, '2022#18': T2, '2022#19': T2,
    '2023#19': T7,
    '2024#17': [(r'第一象限|xy=', T8), ('', T2)],
    '2025#19': T4, '2025#20': T2,
    '2026#7': T4, '2026#17': T6, '2026#20': T3,
}

# ---- 李林880:做题本题号(二重积分章 = 463–540)→ 题型 ----
MAP_880 = {
    463: T12, 464: T4, 465: T4, 466: T5, 467: T6, 468: T6, 469: T5, 470: T5,
    471: T5, 472: T9, 473: T4, 474: T4, 475: T4, 476: T1, 477: T2, 478: T8,
    479: T4, 480: T3, 481: T4, 482: T9, 483: T3, 484: T2, 485: T8, 486: T2,
    487: T7, 488: T7, 489: T7, 490: T2, 491: T7, 492: T7, 493: T7, 494: T7,
    495: T7, 496: T1, 497: T3, 498: T12, 499: T12, 500: T11, 501: T6, 502: T6,
    503: T10, 504: T9, 505: T7, 506: T3, 507: T5, 508: T5, 509: T5, 510: T1,
    511: T7, 512: T7, 513: T4, 514: T2, 515: T8, 516: T4, 517: T1, 518: T4,
    519: T8, 520: T6, 521: T9, 522: T9, 523: T3, 524: T1, 525: T3, 526: T9,
    527: T10, 528: T10, 529: T9, 530: T10, 531: T1, 532: T10, 533: T4,
    534: T8, 535: T9, 536: T3, 537: T7, 538: T8, 539: T1, 540: T4,
}


def pick_real(year, number, stem=''):
    v = MAP_REAL.get('%s#%s' % (year, number))
    if v is None:
        return ''
    if isinstance(v, str):
        return v
    for pat, name in v:
        if not pat or re.search(pat, stem or ''):
            return name
    return ''


def pick_880(num):
    try:
        return MAP_880.get(int(num), '')
    except (TypeError, ValueError):
        return ''


JIANGJIE = {}
JIANGJIE[T1] = {
    'intuition': r"圆的边界在直角坐标里是 $y=\pm\sqrt{1-x^2}$ 这种带根号的丑东西,换成极坐标就一句 $r=1$。所以看到圆、扇形、环,或者被积函数里成团出现 $x^2+y^2$,就别在直角坐标里硬扛——换到极坐标,丑边界立刻变干净。",
    'trigger': r"区域边界是圆/圆弧/扇形/环,或由 $r=r(\theta)$ 型曲线(心形线、双纽线、玫瑰线)围成;或被积函数含 $\sqrt{x^2+y^2}$、$x^2+y^2$。且整个区域能用**一个** $\theta$ 区间配**一段** $r$ 上下限盖住。",
    'example_src': r"2020 真题 #19",
    'example_stem': r"设区域 $D$ 由直线 $x=1$、$x=2$、$y=x$ 及 $x$ 轴围成,计算 $\displaystyle\iint_D \frac{\sqrt{x^2+y^2}}{x}\,dxdy$。",
    'example_steps': [
        r"**定 $\theta$ 范围**:区域夹在 $x$ 轴($\theta=0$)和 $y=x$($\theta=\frac{\pi}{4}$)之间,所以 $0\le\theta\le\frac{\pi}{4}$。",
        r"**定 $r$ 上下限**:把两条边界化成 $r=r(\theta)$。$x=1\Rightarrow r\cos\theta=1\Rightarrow r=\sec\theta$;$x=2\Rightarrow r=2\sec\theta$。于是 $\sec\theta\le r\le 2\sec\theta$。",
        r"**换被积 + 别忘 $r$**:$\dfrac{\sqrt{x^2+y^2}}{x}=\dfrac{r}{r\cos\theta}=\sec\theta$,面积元 $dxdy=r\,drd\theta$,所以 $I=\displaystyle\int_0^{\pi/4}\!\!\sec\theta\int_{\sec\theta}^{2\sec\theta} r\,dr\,d\theta$。",
        r"**先积 $r$**:$\displaystyle\int_{\sec\theta}^{2\sec\theta}r\,dr=\frac{4\sec^2\theta-\sec^2\theta}{2}=\frac{3}{2}\sec^2\theta$,于是 $I=\dfrac{3}{2}\displaystyle\int_0^{\pi/4}\sec^3\theta\,d\theta$。",
        r"**收尾**:$\displaystyle\int\sec^3\theta\,d\theta=\frac{1}{2}\big(\sec\theta\tan\theta+\ln|\sec\theta+\tan\theta|\big)$,代入 $0\to\frac{\pi}{4}$ 得 $\frac{1}{2}(\sqrt2+\ln(1+\sqrt2))$。故 $I=\dfrac{3}{4}\big(\sqrt2+\ln(1+\sqrt2)\big)$。",
    ],
    'steps': [
        r"**画区域**,看它被哪两条射线夹住 → 定出 $\theta$ 的上下限(这一步定了,后面才不会乱)。",
        r"把每条边界曲线**化成 $r=r(\theta)$**:$x=a\Rightarrow r=a\sec\theta$;$y=b\Rightarrow r=b\csc\theta$;$x^2+y^2=2ax\Rightarrow r=2a\cos\theta$(偏心圆);$x^2+y^2=R^2\Rightarrow r=R$。",
        r"写成 $\displaystyle\int_{\theta_1}^{\theta_2}\!\!d\theta\int_{r_{\text{内}}(\theta)}^{r_{\text{外}}(\theta)} f(r\cos\theta,r\sin\theta)\,r\,dr$,**面积元的 $r$ 一定要写**。",
        r"先积 $r$(通常是幂函数,很快),再积 $\theta$。",
    ],
    'variants': [
        r"**偏心圆**:$x^2+y^2\le 2x$ → $r=2\cos\theta$,$\theta\in[-\frac{\pi}{2},\frac{\pi}{2}]$(2017#20、2012#18 的心形线同理)。",
        r"**环形/两圆之间**:$2\le r\le 2(1+\cos\theta)$(2016#15),$r$ 的内外限都是 $\theta$ 的函数,照写就行。",
        r"**极坐标方程给定的怪曲线**:双纽线 $(x^2+y^2)^2=x^2-y^2\Rightarrow r^2=\cos2\theta$(2021#21)、玫瑰线 $(x^2+y^2)^3\le y^4\Rightarrow r\le\sin^2\theta$(2019#18)。套路一模一样。",
        r"**先平移再极坐标**:$(x-1)^2+(y-1)^2\le2$ 先令 $u=x-1,v=y-1$ 化成圆心在原点(2009#17)。",
    ],
    'pitfalls': [
        r"**漏掉面积元的 $r$**——最高频失分点,$dxdy=r\,drd\theta$。",
        r"$\theta$ 范围凭感觉写。**先画图**:区域被哪两条过原点的射线夹住,就是 $\theta_1,\theta_2$。",
        r"原点不在区域内时,$r$ 的下限不是 0(本题下限是 $\sec\theta$,不是 0)。",
    ],
}
JIANGJIE[T2] = {
    'intuition': r"还是极坐标,但区域是**两条曲线相交**围出来的。这时候从原点朝不同方向射出去,先撞到的边界不是同一条——所以 $r$ 的上限在某个 $\theta_0$ 处**换人**了。必须先求交点定出 $\theta_0$,把 $\theta$ 切成两段分别写。",
    'trigger': r"两个圆(或圆与直线、圆与曲线)的**公共部分/相交区域**;或区域虽是一片,但沿 $\theta$ 扫过去时 $r$ 的上界(或下界)中途换了另一条曲线。信号词:两个不等式同时成立、$D_1\cap D_2$。",
    'example_src': r"2025 真题 #20",
    'example_stem': r"已知平面有界区域 $D=\{(x,y)\mid x^2+y^2\le 4x,\ x^2+y^2\le 4y\}$,计算 $\displaystyle\iint_D (x-y)^2dxdy$。",
    'example_steps': [
        r"**两条边界化极坐标**:$x^2+y^2\le4x\Rightarrow r\le4\cos\theta$;$x^2+y^2\le4y\Rightarrow r\le4\sin\theta$。区域是两圆公共部分,位于第一象限,$\theta\in[0,\frac{\pi}{2}]$。",
        r"**求分界角**:$4\cos\theta=4\sin\theta\Rightarrow\theta=\frac{\pi}{4}$。当 $\theta<\frac{\pi}{4}$ 时 $\sin\theta<\cos\theta$,**小的那个才是上限** → $r\le4\sin\theta$;当 $\theta>\frac{\pi}{4}$ 时 $r\le4\cos\theta$。",
        r"**先用对称性省一半**:$D$ 关于 $y=x$ 对称,$(x-y)^2$ 在交换 $x\leftrightarrow y$ 下不变,所以 $I=2\displaystyle\iint_{D\cap\{\theta\le\pi/4\}}(x-y)^2dxdy$。",
        r"**代入积分**:$(x-y)^2=r^2(\cos\theta-\sin\theta)^2=r^2(1-\sin2\theta)$,故 $I=2\displaystyle\int_0^{\pi/4}\!(1-\sin2\theta)\int_0^{4\sin\theta} r^3\,dr\,d\theta=2\int_0^{\pi/4}(1-\sin2\theta)\cdot 64\sin^4\theta\,d\theta$。",
        r"**收尾**:拆成 $128\displaystyle\int_0^{\pi/4}\sin^4\theta\,d\theta-128\int_0^{\pi/4}\sin^4\theta\sin2\theta\,d\theta$,前者用降幂公式、后者令 $u=\sin\theta$ 凑微分,分别积出后相减。",
    ],
    'steps': [
        r"两条边界**都**化成 $r=r_1(\theta)$、$r=r_2(\theta)$。",
        r"**解 $r_1(\theta)=r_2(\theta)$ 求分界角 $\theta_0$**——这一步是本题型的命门。",
        r"在每段 $\theta$ 上判断谁是真正的上限:求**公共部分**取**较小者**,求**并集/外侧**取较大者。",
        r"分段写成两个累次积分相加;若区域关于某条线对称、被积也对称,先用对称性只算一段再乘 2。",
    ],
    'variants': [
        r"**圆与直线切出的分段**:$1\le x^2+y^2\le 2x,y\ge0$(880-28),内限 $r=1$、外限 $r=2\cos\theta$,还要解出 $\theta$ 的可行范围。",
        r"**圆弧 + 直线段拼的区域**:$y-2\le x\le\sqrt{4-y^2}$(2022#18),一段由直线定 $r$,一段由圆定 $r$。",
        r"**选择题只要形式**:2015#3 只问「写成极坐标累次积分是哪个」,分界角照样得求。",
        r"**上限被 $|y|\le1$ 截断**:2024#17,$\theta\le\frac{\pi}{4}$ 时上限 $\sec\theta$,$\theta>\frac{\pi}{4}$ 时上限 $\csc\theta$。",
    ],
    'pitfalls': [
        r"**求交集时取了较大的那个 $r$**——公共部分永远取 $\min$。",
        r"忘了求分界角,一路用同一个上限积到底,答案必错。",
        r"分段后两段的 $\theta$ 区间写重叠或漏缝。",
    ],
}
JIANGJIE[T3] = {
    'intuition': r"最朴素的一招:把二重积分拆成「先积一个、再积另一个」的两层一元积分。关键**只有一件事——先积谁**。选对了一步到底,选错了内层原函数根本写不出来。所以不是随便选序,是**看被积函数点名让你先积谁**。",
    'trigger': r"边界是直线、抛物线这类非圆的一般曲线,极坐标反而更麻烦;区域用 $a\le x\le b,\ \varphi_1(x)\le y\le\varphi_2(x)$ 就能写清。也包括题目直接给出累次积分让你算出来(含 $(r,\theta)$ 形式的,把 $r,\theta$ 当两个普通变量一样处理)。",
    'example_src': r"2026 真题 #20",
    'example_stem': r"设平面区域 $D=\{(x,y)\mid 0\le x\le1,\ 0\le y\le1\}$,计算 $\displaystyle\iint_D \frac{y}{(1+x^2+y^2)^{3/2}}dxdy$。",
    'example_steps': [
        r"**看被积函数选序**:分子有个 $y$,而 $\frac{d}{dy}(1+x^2+y^2)^{-1/2}=-y(1+x^2+y^2)^{-3/2}$——**先积 $y$** 就是凑微分,一步出来。反过来先积 $x$ 则无从下手。",
        r"**先积 $y$**:$\displaystyle\int_0^1\frac{y\,dy}{(1+x^2+y^2)^{3/2}}=\Big[-\frac{1}{\sqrt{1+x^2+y^2}}\Big]_0^1=\frac{1}{\sqrt{1+x^2}}-\frac{1}{\sqrt{2+x^2}}$。",
        r"**再积 $x$**:用 $\displaystyle\int\frac{dx}{\sqrt{x^2+a^2}}=\ln\big(x+\sqrt{x^2+a^2}\big)+C$,得 $I=\big[\ln(x+\sqrt{1+x^2})\big]_0^1-\big[\ln(x+\sqrt{2+x^2})\big]_0^1$。",
        r"**代入**:$=\ln(1+\sqrt2)-\big[\ln(1+\sqrt3)-\ln\sqrt2\big]=\ln\dfrac{\sqrt2(1+\sqrt2)}{1+\sqrt3}=\ln\dfrac{\sqrt2+2}{1+\sqrt3}$。",
    ],
    'steps': [
        r"**画区域**,写出两种切法的限:竖切 $a\le x\le b,\varphi_1(x)\le y\le\varphi_2(x)$;横切 $c\le y\le d,\psi_1(y)\le x\le\psi_2(y)$。",
        r"**看被积函数决定先积谁**:哪个变量积起来能凑微分、能出初等原函数,就先积它。$e^{-y^2}$、$\frac{\sin y}{y}$ 这类出现时,**绝对不能先积它**。",
        r"内层积分把另一个变量当常数,积完得到一个一元函数;外层再积一次。",
        r"若区域被折线/交点切成几块(先积那个变量的上限中途换人),就**分块相加**。",
    ],
    'variants': [
        r"**被积逼你选序**:$\displaystyle\iint_D x^2e^{-y^2}$,$D:|x|\le y\le1$(2016#12)——$e^{-y^2}$ 积不出,必须先积 $x$。",
        r"**区域逼你分块**:$D$ 由 $x=3y,y=3x,x+y=8$ 围成(2013#17),先积 $y$ 时上限在交点处换人,切成两块。",
        r"**参数方程边界**:摆线 $x=t-\sin t$ 围的区域(2018#17、880-73),照样竖切,只是外层那个一元积分要用参数代换。",
        r"**$(r,\theta)$ 形式的累次积分**:$\displaystyle\iint_D r^2\sin\theta\sqrt{1-r^2\cos^2\theta}\,drd\theta$(2010#20)——把 $r,\theta$ 当普通两变量,一样是选序、先积能积的那个。",
    ],
    'pitfalls': [
        r"**不看被积函数就按 $x$ 在前的习惯写**,结果内层原函数写不出来,卡死。",
        r"换成横切后**上下限忘了跟着换成 $y$ 的函数**。",
        r"区域该分块却没分,上限用了一条曲线通到底。",
    ],
}
JIANGJIE[T4] = {
    'intuition': r"这一招不算积分,是**先划掉一部分再算**。两种划法:①区域左右(上下)对称、被积对那个变量是奇函数 → 整项直接是 0,连算都不用算;②区域关于 $y=x$ 对称 → 把 $x$ 和 $y$ 换个名字积分值不变,于是可以把两个丑积分加起来变一个漂亮的。数二真题里这招出现的频率极高,常常是「不用它就做不出来」。",
    'trigger': r"看两样东西:**区域的对称性**(关于 $x$ 轴/$y$ 轴/原点/直线 $y=x$)和**被积函数的奇偶性或轮换性**。被积函数是多项式展开后有奇次项、或形如 $\frac{x}{x+y}$、$\frac{f(x)}{f(x)+f(y)}$ 时,几乎必用。",
    'example_src': r"2014 真题 #16",
    'example_stem': r"计算区域 $D=\{(x,y)\mid 1\le x^2+y^2\le4,\ x\ge0,\ y\ge0\}$ 上的二重积分 $\displaystyle\iint_D\frac{x\sin(\pi\sqrt{x^2+y^2})}{x+y}\,d\sigma$。",
    'example_steps': [
        r"**认出轮换对称**:$D$ 是第一象限的四分之一圆环,关于直线 $y=x$ 对称。所以把被积里的 $x$ 与 $y$ 互换,积分值不变:$I=\displaystyle\iint_D\frac{y\sin(\pi\sqrt{x^2+y^2})}{x+y}d\sigma$。",
        r"**两式相加**:$2I=\displaystyle\iint_D\frac{(x+y)\sin(\pi\sqrt{x^2+y^2})}{x+y}d\sigma=\iint_D\sin\big(\pi\sqrt{x^2+y^2}\big)d\sigma$。分母被消掉了——这就是这招的全部价值。",
        r"**剩下的用极坐标**:$2I=\displaystyle\int_0^{\pi/2}\!\!d\theta\int_1^2\sin(\pi r)\cdot r\,dr=\frac{\pi}{2}\int_1^2 r\sin(\pi r)\,dr$。",
        r"**算内层**:$\displaystyle\int r\sin(\pi r)dr=-\frac{r\cos(\pi r)}{\pi}+\frac{\sin(\pi r)}{\pi^2}$,代 $1\to2$ 得 $-\frac{2}{\pi}-\frac{1}{\pi}=-\frac{3}{\pi}$。",
        r"**收尾**:$2I=\dfrac{\pi}{2}\cdot\Big(-\dfrac{3}{\pi}\Big)=-\dfrac{3}{2}$,所以 $I=-\dfrac{3}{4}$。",
    ],
    'steps': [
        r"**先判区域对称于什么**:关于 $y$ 轴?$x$ 轴?原点?直线 $y=x$?",
        r"**再把被积函数按项拆开**,逐项看:关于 $x$ 是奇函数且 $D$ 关于 $y$ 轴对称 → 该项 $=0$;是偶函数 → 该项 $=2\times$ 半区域。",
        r"若 $D$ 关于 $y=x$ 对称,写出 $x\leftrightarrow y$ 互换后的 $I$,与原式**相加**(有时相减),把分母或丑结构消掉。",
        r"化简完剩下的那个干净积分,再按极坐标或选序算出。",
    ],
    'variants': [
        r"**奇项归零**:$\displaystyle\iint_{x^2+y^2\le1}(x^2-y)$(2008#11)、$\displaystyle\iint_{x^2+y^2\le2x}(2x+3y)$(880-19),$-y$、$3y$ 直接 0。",
        r"**展开后逐项判**:$\displaystyle\iint(x+y)^3$(2010#16) 展成四项,对 $y$ 奇的两项消掉。",
        r"**分母消去型**:$\displaystyle\iint_D\frac{af(x)+bf(y)}{f(x)+f(y)}$(880-11)、$\displaystyle\iint_D\frac{(x+y)^2}{x^2+y^2}$,都是 $x\leftrightarrow y$ 相加。",
        r"**用来证不等式**:$\displaystyle\iint_D xf(x)f(y)[f(x)-f(y)]\le0$(880-70),把 $x\leftrightarrow y$ 相加后配成完全平方判号。",
    ],
    'pitfalls': [
        r"**只看被积函数不看区域**——区域不对称,奇函数也不为 0。",
        r"关于 $y=x$ 互换时**积分区域也要真的不变**才行(第一象限的四分圆可以,一般三角形不行)。",
        r"逐项判时漏了某一项,或把 $2\times$ 半区域的 2 忘了。",
    ],
}
JIANGJIE[T5] = {
    'intuition': r"题目已经把累次积分写好递到你手上了,但里层那个积分**根本积不出来**($e^{-y^2}$、$\sin(1-x)^2$、$\frac{\sin y}{y}$ 都没有初等原函数)。这不是让你硬算,是在提示你:**这个顺序是错的**。把它还原成一片区域,换另一头先积,立刻能积。注意——你不是在「翻限」,你是在**重新看图**。",
    'trigger': r"题面直接给 $\displaystyle\int_a^b\!dx\int_{\varphi_1(x)}^{\varphi_2(x)}f\,dy$ 这种累次积分(不是给区域),而且内层被积函数明显积不出来;或者两个累次积分相加、限看着很别扭。",
    'example_src': r"李林880 · 二重积分 · 基础 (1)",
    'example_stem': r"计算 $\displaystyle I=\int_0^1 x^2\,dx\int_x^1 e^{-y^2}\,dy$。",
    'example_steps': [
        r"**先看内层**:$\displaystyle\int e^{-y^2}dy$ 没有初等原函数 → 确定要换序。",
        r"**还原区域**(关键一步,一定画图):$0\le x\le1$,$x\le y\le1$,即 $D:\ 0\le x\le y\le1$ —— 单位正方形里 $y=x$ 上方那个三角形。",
        r"**按另一头重写限**:先积 $x$ 时,$y$ 从 0 到 1,$x$ 从 0 到 $y$。于是 $I=\displaystyle\int_0^1 e^{-y^2}\Big(\int_0^y x^2dx\Big)dy=\int_0^1 e^{-y^2}\cdot\frac{y^3}{3}\,dy$。",
        r"**现在能积了**:令 $u=y^2$,$du=2y\,dy$,则 $y^3dy=\frac{u}{2}du$,得 $I=\dfrac{1}{6}\displaystyle\int_0^1 ue^{-u}du$。",
        r"**收尾**:$\displaystyle\int_0^1ue^{-u}du=\big[-ue^{-u}\big]_0^1+\int_0^1e^{-u}du=-\frac{1}{e}+1-\frac{1}{e}=1-\frac{2}{e}$,所以 $I=\dfrac{1}{6}\Big(1-\dfrac{2}{e}\Big)$。",
    ],
    'steps': [
        r"**判断该不该换**:内层被积函数对内层变量是否可积?积不出就换。",
        r"**由限还原区域并画出来**——不要试图在纸上直接「翻转不等式」,画图最快最不会错。",
        r"**读图重写限**:新外层变量的整体范围 = 图形在那个轴上的投影;新内层的上下限 = 沿该方向穿进穿出的两条边界。",
        r"换完后先积原来积不出的那一层(现在它成了被乘的常数或能凑微分),再积外层。",
    ],
    'variants': [
        r"**两段拼一片**:$\displaystyle\int_0^2\!dx\!\int_0^{x^2/2}\!+\int_2^{2\sqrt2}\!dx\!\int_0^{\sqrt{8-x^2}}$(880-4),先把两块拼成一片再换序。",
        r"**内层限是曲线**:$\displaystyle\int_1^2\!dx\!\int_{\sqrt x}^{x}\sin\frac{\pi x}{2y}dy+\int_2^4\!dx\!\int_{\sqrt x}^{2}\cdots$(880-8)。",
        r"**换完还要凑微分**:$\displaystyle\int_0^1\!dy\!\int_0^{y^2}y\sin(1-x)^2dx$(880-44)。",
        r"**$(r,\theta)$ 平面上换序**:$\displaystyle\int_0^{2\pi}\!d\theta\!\int_{\theta/2}^{\pi}\theta^2e^{r^2}dr$(880-45)——把 $r,\theta$ 当普通两变量,同一套还原重写。",
    ],
    'pitfalls': [
        r"**不画图硬翻限**——这是本题型唯一的失分来源。",
        r"新外层变量的范围写成了原来那个变量的范围。",
        r"两段累次积分对应的是同一片区域,却分别换序,没有先合并。",
    ],
}
JIANGJIE[T6] = {
    'intuition': r"和「换序」是同一个动作,只是换的不是次序而是**坐标系**。题目给你一串直角坐标的累次积分,你看见限里有 $\sqrt{2-x^2}$、$|x|$ 这种圆和射线的痕迹,或者被积函数里成团的 $x^2+y^2$ —— 那就是在说「我本来是极坐标的题,被写成直角坐标折磨你」。还原成区域,换成极坐标写,立刻化开。",
    'trigger': r"题面给的是累次积分而非区域,且**限里出现 $\sqrt{R^2-x^2}$、$|x|$、$\sqrt{2x-x^2}$** 等圆弧/射线,或被积含 $\sqrt{x^2+y^2}$、$\sin(x^2+y^2)$、$e^{-(x^2+y^2)}$。反向题(给极坐标累次积分要化回直角坐标)是同一题型,倒着走一遍。",
    'example_src': r"2026 真题 #17",
    'example_stem': r"计算 $\displaystyle I=\int_{-1}^{1}dx\int_{|x|}^{\sqrt{2-x^2}} y\sin\sqrt{x^2+y^2}\;dy$。",
    'example_steps': [
        r"**还原区域**:下界 $y=|x|$ 是两条 $45^\circ$ 射线,上界 $y=\sqrt{2-x^2}$ 是圆 $x^2+y^2=2$ 的上半。所以 $D$ 是圆 $r=\sqrt2$ 内、夹在两条射线上方的那块扇形。",
        r"**读出极坐标限**:$y\ge|x|$ 即 $\frac{\pi}{4}\le\theta\le\frac{3\pi}{4}$;$r$ 从 0 到 $\sqrt2$。",
        r"**换被积 + 面积元**:$y\sin\sqrt{x^2+y^2}=r\sin\theta\cdot\sin r$,再乘 $r\,drd\theta$,得 $I=\displaystyle\int_{\pi/4}^{3\pi/4}\!\!\sin\theta\,d\theta\int_0^{\sqrt2} r^2\sin r\,dr$ —— 变量彻底分离了。",
        r"**算 $\theta$ 那半**:$\displaystyle\int_{\pi/4}^{3\pi/4}\sin\theta\,d\theta=\big[-\cos\theta\big]_{\pi/4}^{3\pi/4}=\frac{\sqrt2}{2}+\frac{\sqrt2}{2}=\sqrt2$。",
        r"**算 $r$ 那半**(两次分部):$\displaystyle\int r^2\sin r\,dr=-r^2\cos r+2r\sin r+2\cos r$,代 $0\to\sqrt2$ 得 $2\sqrt2\sin\sqrt2-2$。",
        r"**收尾**:$I=\sqrt2\big(2\sqrt2\sin\sqrt2-2\big)=4\sin\sqrt2-2\sqrt2$。",
    ],
    'steps': [
        r"**由限还原区域并画图**(和换序同一步,别省)。",
        r"把边界翻译成 $\theta$ 的范围和 $r=r(\theta)$:直线 $y=kx\to\theta=\arctan k$;圆 $x^2+y^2=R^2\to r=R$;$x^2+y^2=2ax\to r=2a\cos\theta$。",
        r"被积函数按 $x=r\cos\theta,\ y=r\sin\theta$ 代换,**乘上 $r$**,写成 $\displaystyle\int d\theta\int f\cdot r\,dr$。",
        r"若要求的只是「化成哪个形式」(选择/填空),写到这步就结束;要求算出的,再分别积。",
    ],
    'variants': [
        r"**只要形式的选择题**:$D:x^2+y^2\le x$,问 $\displaystyle\iint_D f$ 的极坐标累次形式(880-5)。",
        r"**反向**:把 $\displaystyle\int_{\pi/4}^{\pi/2}\!d\theta\!\int_0^{2\sin\theta}f\,r\,dr$ 化回直角坐标(880-6、880-39)——还原区域再竖切/横切。",
        r"**换完要算出**:$\displaystyle\int\!dx\!\int_{|x|}^{\sqrt{\pi-x^2}}e^{-(x^2+y^2)}\sin(x^2+y^2)dy$(880-57),和母题同构。",
    ],
    'pitfalls': [
        r"**又忘了 $r$**:$dxdy=r\,drd\theta$。",
        r"$y\ge|x|$ 误读成 $\theta\in[0,\frac{\pi}{4}]$——画图确认是**上方**那块($\frac{\pi}{4}$ 到 $\frac{3\pi}{4}$)。",
        r"反向化回直角坐标时,忘了先把 $r=2\sin\theta$ 还原成圆 $x^2+(y-1)^2=1$。",
    ],
}
JIANGJIE[T7] = {
    'intuition': r"被积函数里有 $|\cdot|$、$\max$、$\min$、$[\ \cdot\ ]$ 或分段定义——这些东西**不能直接积**。但它们「变脸」的位置是一条明确的曲线(让 $|\cdot|$ 里面等于 0、让 $\max$ 的两个候选相等)。用这条曲线把区域切开,在每一块上它就是个普通函数了。所以这类题的全部难度**不在积分,在切区域**。",
    'trigger': r"被积函数含 $|f(x,y)|$、$\max\{\cdot,\cdot\}$、$\min$、$\mathrm{sgn}$、取整 $[\cdot]$,或题目直接给一个分段定义的 $f(x,y)$。",
    'example_src': r"2008 真题 #17",
    'example_stem': r"计算 $\displaystyle\iint_D\max(xy,1)\,dxdy$,其中 $D=\{(x,y)\mid 0\le x\le2,\ 0\le y\le2\}$。",
    'example_steps': [
        r"**找变脸曲线**:$\max(xy,1)$ 在 $xy=1$ 两侧换人。双曲线 $xy=1$ 穿过正方形 $[0,2]^2$,把它切成两块:$D_1:xy<1$(靠原点那侧,取值 1)、$D_2:xy\ge1$(取值 $xy$)。",
        r"**拆成两个积分**:$I=\displaystyle\iint_{D_1}1\,dxdy+\iint_{D_2}xy\,dxdy=S(D_1)+\iint_{D_2}xy\,dxdy$ —— 第一块直接是面积,不用积。",
        r"**算 $D_2$ 的范围**:$xy\ge1$ 且 $x,y\le2$ 要求 $x\ge\frac12$,此时 $y$ 从 $\frac1x$ 到 2。于是 $S(D_2)=\displaystyle\int_{1/2}^{2}\Big(2-\frac1x\Big)dx=\big[2x-\ln x\big]_{1/2}^{2}=3-2\ln2$。",
        r"**第一块面积**:$S(D_1)=4-S(D_2)=4-(3-2\ln2)=1+2\ln2$。",
        r"**算 $D_2$ 上的积分**:$\displaystyle\int_{1/2}^{2}x\Big[\frac{y^2}{2}\Big]_{1/x}^{2}dx=\int_{1/2}^{2}\Big(2x-\frac{1}{2x}\Big)dx=\Big[x^2-\frac12\ln x\Big]_{1/2}^{2}=\frac{15}{4}-\ln2$。",
        r"**合并**:$I=(1+2\ln2)+\Big(\dfrac{15}{4}-\ln2\Big)=\dfrac{19}{4}+\ln2$。",
    ],
    'steps': [
        r"**令内部为 0(或令两个候选相等)解出变脸曲线**:$|g|\to g=0$;$\max\{a,b\}\to a=b$;取整 $\to$ 各条整数等值线。",
        r"**在图上画出这条曲线**,看它把 $D$ 切成哪几块,并判断每块上取哪个表达式(代一个具体点验证最快)。",
        r"**逐块积分再相加**;哪块的被积函数是常数,就直接用面积代替积分。",
        r"若某块用极坐标更顺(圆域 + $|r-1|$ 型),就在那块上换极坐标。",
    ],
    'variants': [
        r"**极坐标 + 绝对值**:$\displaystyle\iint_{x^2+y^2\le9}|x^2+y^2-4|$(880-26),分界圆 $r=2$,答案 $\frac{41\pi}{2}$;$\displaystyle\iint_{(x-1)^2+y^2\le1}\big|\sqrt{x^2+y^2}-1\big|$(2023#19)。",
        r"**$\max$ 型**:$\max\{2x-x^2,(1-y)^2\}$(880-30)、$\max\{y+1,\frac{2}{1+x}\}$(880-49)。",
        r"**取整/符号**:$\displaystyle\iint[1+x+y]$(880-29)、$\displaystyle\iint\mathrm{sgn}(x^2-y^2+2)$(880-31)。",
        r"**题目直接给分段 $f$**:880-32、880-33,先看清每段的定义域再和 $D$ 求交。",
    ],
    'pitfalls': [
        r"**变脸曲线画错或漏了一段**——一切错误的根源。",
        r"判断哪块取哪个表达式时**凭感觉**:代一个具体点(如原点)进去验,一秒确认。",
        r"常数块忘了可以直接用面积,反而去积分,费时又易错。",
    ],
}
JIANGJIE[T8] = {
    'intuition': r"极坐标只是换元里最常用的**一种**。当区域的四条边界长得像 $xy=c$、$\frac{y}{x}=c$、$x+y=c$ 时,极坐标不管用,但只要**让边界表达式本身当新变量**($u=xy$、$v=\frac{y}{x}$),区域立刻变成一个矩形——最好积的形状。代价是要乘上雅可比行列式。",
    'trigger': r"区域由**两组「同一形式、不同常数」的曲线**夹成:$xy=a$ 与 $xy=b$、$y=k_1x$ 与 $y=k_2x$、$x+y=a$ 与 $x+y=b$、$|\ln x|+|\ln y|=1$ 等;或被积函数整体是 $g(x+y)$、$e^{x/(x+y)}$ 这种「只认某个组合」的形式。",
    'example_src': r"2024 真题 #17",
    'example_stem': r"设平面有界区域 $D$ 位于第一象限,由曲线 $xy=\frac13$、$xy=3$ 与直线 $y=\frac13x$、$y=3x$ 围成,计算 $\displaystyle\iint_D(1+x-y)\,dxdy$。",
    'example_steps': [
        r"**让边界当新变量**:令 $u=xy,\ v=\dfrac{y}{x}$。四条边界直接变成 $u=\frac13,u=3,v=\frac13,v=3$ —— 区域成了正方形 $[\frac13,3]^2$。",
        r"**反解并算雅可比**:$x=\sqrt{u/v},\ y=\sqrt{uv}$,算得 $\dfrac{\partial(x,y)}{\partial(u,v)}=\dfrac{1}{2v}$,故 $dxdy=\dfrac{du\,dv}{2v}$。",
        r"**换被积**:$x-y=\sqrt{u}\Big(\dfrac{1}{\sqrt v}-\sqrt v\Big)$,于是 $I=\displaystyle\iint_{[1/3,3]^2}\Big[1+\sqrt u\Big(\frac{1}{\sqrt v}-\sqrt v\Big)\Big]\frac{du\,dv}{2v}$。",
        r"**第二项自动为 0**:它对 $v$ 的部分是 $\displaystyle\int_{1/3}^{3}\big(v^{-3/2}-v^{-1/2}\big)dv=\frac{4}{\sqrt3}-\frac{4}{\sqrt3}=0$。(也可由 $v\to\frac1v$ 的对称性一眼看出。)",
        r"**只剩第一项**:$I=\displaystyle\int_{1/3}^{3}\!\!du\int_{1/3}^{3}\frac{dv}{2v}=\frac12\Big(3-\frac13\Big)\big[\ln v\big]_{1/3}^{3}=\frac12\cdot\frac83\cdot\ln 9=\dfrac{8}{3}\ln 3$。",
    ],
    'steps': [
        r"**认出边界的共同形式**,把那个表达式设成新变量($u,v$ 各一个),使区域变成矩形。",
        r"**反解出 $x=x(u,v),y=y(u,v)$**,算雅可比 $J=\dfrac{\partial(x,y)}{\partial(u,v)}$,则 $dxdy=|J|\,dudv$。(反解太难时,算 $\dfrac{\partial(u,v)}{\partial(x,y)}$ 再取倒数。)",
        r"被积函数也用 $u,v$ 重写,在矩形上积分(常常变量可分离,两个一元积分相乘)。",
        r"新区域上若有对称性($v\to\frac1v$ 之类),顺手用掉。",
    ],
    'variants': [
        r"**只换一个组合**:$u=x+y$,如 $\displaystyle\iint_D e^{x/(x+y)}$(880-16)、$\displaystyle\iint_D\frac{xe^{(x+y)^2}}{x+y}$(880-23)、$\displaystyle\iint_{|x|+|y|\le1}f(x+y)$ 的证明(880-71)。",
        r"**$u=x+y,\ v=x-y$**:$(x+y)^3=xy$ 围的区域(880-52)、$e^{(x+y)^2}(\sin^2x+\cos^2y)$(880-56)。",
        r"**取对数换元**:$|\ln x|+|\ln y|=1$ 围的区域,令 $u=\ln x,v=\ln y$(880-75),此时 $dxdy=e^{u+v}dudv$。",
    ],
    'pitfalls': [
        r"**忘乘雅可比**,或把 $\dfrac{\partial(u,v)}{\partial(x,y)}$ 直接当成 $|J|$(应取倒数)。",
        r"新区域的范围写错:必须是每条老边界一一对应到 $u$ 或 $v$ 的一个常数值。",
        r"$|J|$ 的绝对值忘了取,得出负的面积元。",
    ],
}
JIANGJIE[T9] = {
    'intuition': r"这类题的二重积分**不是要你算出一个数**,而是一个含参数 $t$(或 $u$)的函数 $F(t)$,接下来要对它求导、或求 $t\to0$ 的极限。诀窍只有一句:**先用极坐标把二重积分压成一个一元的变限积分**,之后它就退化成一元微积分的老套路(变限积分求导 / 洛必达 / 等价无穷小)。",
    'trigger': r"区域或积分限里带参数($D_t$、$x^2+y^2\le t^2$、上限是 $u$),要求 $\dfrac{\partial F}{\partial u}$、$F'(t)$、或 $\lim\limits_{t\to0^+}\dfrac{1}{t^k}\displaystyle\iint_{D_t}f$。",
    'example_src': r"2008 真题 #4",
    'example_stem': r"设 $F(u,v)=\displaystyle\iint_{D_{uv}}\frac{f(x^2+y^2)}{\sqrt{x^2+y^2}}dxdy$,其中 $D_{uv}$ 为圆环域 $1\le x^2+y^2\le u^2$,$0\le\theta\le v$,求 $\dfrac{\partial F}{\partial u}$。",
    'example_steps': [
        r"**换极坐标**:$D_{uv}$ 就是 $1\le r\le u$、$0\le\theta\le v$ —— 参数正好落在积分限上,这是本题型的标准长相。",
        r"**压成一元**:$F=\displaystyle\int_0^v\!\!d\theta\int_1^u\frac{f(r^2)}{r}\cdot r\,dr=\int_0^v d\theta\cdot\int_1^u f(r^2)\,dr=v\int_1^u f(r^2)\,dr$。注意面积元的 $r$ 恰好把分母消掉了。",
        r"**变限积分求导**:$\theta$ 那半与 $u$ 无关,当常数;对上限 $u$ 求导直接取被积函数在 $u$ 处的值。",
        r"**得答案**:$\dfrac{\partial F}{\partial u}=v\,f(u^2)$。",
    ],
    'steps': [
        r"**先换极坐标**,让参数 $t$ 只出现在 $r$(或 $\theta$)的积分限上。",
        r"**把能分离的先积掉**,把二重积分压成形如 $C\cdot\displaystyle\int_{a}^{t}g(r)dr$ 的一元变限积分。",
        r"**求导**用变限积分求导公式;**求极限**用洛必达(分子分母同时对 $t$ 求导)或等价无穷小。",
        r"若被积是抽象的 $f$,别急着积——保留成 $\displaystyle\int_0^t f(r)\cdot r\,dr$ 的形式再洛必达。",
    ],
    'variants': [
        r"**求极限型**:$\lim\limits_{t\to0^+}\dfrac{1}{t^2}\displaystyle\iint_{D_t}(\sin x+\cos y)$(880-41)、$\lim\limits_{t\to0^+}\dfrac{1}{t^2}\displaystyle\iint_{[0,t]^2}e^{(x+y)^2}\cos(x+y)^2$(880-20)——分母的 $t^k$ 提示你用洛必达几次。",
        r"**变限二重积分求高阶导**:$f(t)=\displaystyle\int_0^t\!dx\!\int_x^t e^{-(x-y)^2}dy$,求 $f''(1)$(880-10)——先对 $t$ 求一次导,注意 $t$ 同时出现在**两层**限里。",
        r"**含抽象 $f$ 的极限**:$D:x^2+y^2\le2tx,y\ge0$(880-72)、880-63,极坐标后配等价无穷小。",
        r"**二重积分等式反求函数**:$\displaystyle\iint_{D_t}f'(x+y)=\iint_{D_t}f(t)$ 求 $f(x)$(2011#19)——两边都压成一元后变成微分方程。",
    ],
    'pitfalls': [
        r"**参数同时出现在多处**(如既在上限又在被积里)却只对一处求导。",
        r"极坐标后忘了 $r$,导致压出来的一元被积函数少一个 $r$ 因子。",
        r"洛必达前没检查是否真的是 $\frac00$;或求极限时次数 $k$ 与实际阶数不符还硬洛。",
    ],
}
JIANGJIE[T10] = {
    'intuition': r"式子里的 $\displaystyle\iint_D f$ 看着吓人,其实**它是个数**——$D$ 是固定区域,积完就是一个常数,和 $x,y$ 无关了。所以把它整体设成 $A$,方程立刻变成普通的代数式;再把这个式子代回 $\displaystyle\iint_D$ 去积一遍,就得到关于 $A$ 的一元方程,解出 $A$ 即可。**认出「它只是个常数」是全部关键。**",
    'trigger': r"被求的函数**自己出现在自己的二重积分里**:$f(x,y)=g(x,y)+\displaystyle\iint_D f$;或 $F(t)=\displaystyle\iint_{D_t}[\cdots F\cdots]$(此时 $D_t$ 带参数,积出来是 $t$ 的函数,要先化成一元后当积分方程/微分方程解)。",
    'example_src': r"2020 真题 #18",
    'example_stem': r"设 $D=\{(x,y)\mid x^2+y^2\le1,\ y\ge0\}$,连续函数 $f(x,y)$ 满足 $f(x,y)=y\sqrt{1-x^2}+x\displaystyle\iint_D f(x,y)dxdy$,求 $\displaystyle\iint_D xf(x,y)dxdy$。",
    'example_steps': [
        r"**设常数**:令 $A=\displaystyle\iint_D f\,dxdy$(一个数),则 $f(x,y)=y\sqrt{1-x^2}+Ax$。",
        r"**代回自身求 $A$**:$A=\displaystyle\iint_D y\sqrt{1-x^2}\,dxdy+A\iint_D x\,dxdy$。而 $D$ 是上半圆盘,关于 $y$ 轴对称、$x$ 是奇函数 → $\displaystyle\iint_D x=0$,含 $A$ 的项消失。",
        r"**算剩下那个积分**:$\displaystyle\iint_D y\sqrt{1-x^2}=\int_{-1}^{1}\!\sqrt{1-x^2}\Big[\frac{y^2}{2}\Big]_0^{\sqrt{1-x^2}}dx=\frac12\int_{-1}^{1}(1-x^2)^{3/2}dx=\frac12\cdot\frac{3\pi}{8}=\frac{3\pi}{16}$。所以 $A=\dfrac{3\pi}{16}$。",
        r"**回答真正问的东西**:$\displaystyle\iint_D xf=\iint_D xy\sqrt{1-x^2}+A\iint_D x^2$。第一项对 $x$ 是奇函数 → 为 0。",
        r"**算 $\displaystyle\iint_D x^2$**:上半圆盘是整圆盘的一半,$\displaystyle\iint_{x^2+y^2\le1}x^2=\int_0^{2\pi}\!\cos^2\theta\,d\theta\int_0^1 r^3dr=\pi\cdot\frac14=\frac{\pi}{4}$,故 $\displaystyle\iint_D x^2=\frac{\pi}{8}$。",
        r"**收尾**:$\displaystyle\iint_D xf=\frac{3\pi}{16}\cdot\frac{\pi}{8}=\frac{3\pi^2}{128}$。",
    ],
    'steps': [
        r"**把整个 $\displaystyle\iint_D(\cdots)$ 设成字母 $A$**(区域固定时它就是常数)。",
        r"用 $A$ 写出 $f$ 的显式表达式。",
        r"**把这个表达式代回定义 $A$ 的那个积分**,算出各项(此处大量用对称性让含 $A$ 的项归零),得到关于 $A$ 的一元方程并解出。",
        r"回头算题目**真正问的**那个量——别停在求出 $A$ 就交卷。",
    ],
    'variants': [
        r"**基础同构题**:$f(x,y)=xy+\displaystyle\iint_D f$,$D$ 为三角形(880-40)——同一套设常数。",
        r"**区域带参数 → 变一元方程**:$f(t)=2\displaystyle\iint_{x^2+y^2\le t^2}(x^2+y^2)f(\sqrt{x^2+y^2})+t^4$(880-65),先极坐标压成 $\displaystyle\int_0^t$ 再两边求导变微分方程。",
        r"**求 $F(t)$ 表达式**:880-64、880-67、880-69,都是「压成一元 → 求导 → 解微分方程 → 用连续性定初值」。",
    ],
    'pitfalls': [
        r"**把 $\displaystyle\iint_D f$ 当成还含 $x,y$ 的东西**——只要 $D$ 固定,它就是常数。",
        r"$D$ 带参数 $t$ 时反过来当常数——此时它是 $t$ 的函数,必须先化一元再求导。",
        r"解出 $A$ 就收工,忘了题目问的是另一个积分。",
    ],
}
JIANGJIE[T11] = {
    'intuition': r"一元里 $\lim\frac1n\sum f(\frac in)=\int_0^1 f$;二重就是它的双胞胎:$\lim\frac{1}{n^2}\sum_i\sum_j f(\frac in,\frac jn)=\displaystyle\int_0^1\!\!\int_0^1 f$。所以看到**双重求和 + $n\to\infty$**,唯一的动作是把式子硬凑成 $\dfrac{1}{n^2}\cdot f\big(\frac in,\frac jn\big)$ 的样子,然后照抄成单位正方形上的二重积分。",
    'trigger': r"$\lim\limits_{n\to\infty}\displaystyle\sum_{i=1}^n\sum_{j=1}^n(\cdots)$ 形式的双重和式极限。",
    'example_src': r"2010 真题 #6",
    'example_stem': r"求 $\displaystyle\lim_{n\to\infty}\sum_{i=1}^{n}\sum_{j=1}^{n}\frac{n}{(n+i)(n^2+j^2)}$。",
    'example_steps': [
        r"**目标是凑出 $\frac{1}{n^2}$**:分子 $n$、分母有 $n$ 和 $n^2$,总共 $n^{-2}$ 的量级。把分母按 $n$ 提出来:$(n+i)=n(1+\frac in)$,$(n^2+j^2)=n^2\big(1+(\frac jn)^2\big)$。",
        r"**整理**:通项 $=\dfrac{n}{n\big(1+\frac in\big)\cdot n^2\big(1+(\frac jn)^2\big)}=\dfrac{1}{n^2}\cdot\dfrac{1}{\big(1+\frac in\big)\big(1+(\frac jn)^2\big)}$ —— 正好凑成标准形。",
        r"**照抄成二重积分**:$\displaystyle\iint_{[0,1]^2}\frac{dxdy}{(1+x)(1+y^2)}$,其中 $x\leftrightarrow\frac in,\ y\leftrightarrow\frac jn$。",
        r"**变量分离,两个一元积分相乘**:$\displaystyle\int_0^1\frac{dx}{1+x}\cdot\int_0^1\frac{dy}{1+y^2}=\ln2\cdot\frac{\pi}{4}$。",
        r"**答案**:$\dfrac{\pi\ln2}{4}$。",
    ],
    'steps': [
        r"数一数通项里 $n$ 的净次数,**把它凑成 $\dfrac{1}{n^2}\times(\cdots)$**。",
        r"把括号里剩下的部分**全部写成 $\frac in$ 和 $\frac jn$ 的函数**——凑不出来就说明凑法错了,回上一步。",
        r"直接替换成 $\displaystyle\int_0^1\!\!\int_0^1 f(x,y)\,dxdy$。",
        r"能分离就分离成两个一元积分相乘,这类题的被积函数几乎总能分离。",
    ],
    'variants': [
        r"**同构题**:$\lim\limits_{n\to\infty}\displaystyle\sum_{i=1}^n\sum_{j=1}^n\frac{1}{\big(1+\frac in\big)(n^2+j^2)}$(880-38)——已经半凑好了,再补一个 $n^2$ 即可。",
    ],
    'pitfalls': [
        r"**凑成了 $\frac1n$ 而不是 $\frac{1}{n^2}$**:二重要的是 $\frac{1}{n^2}$(两个方向各 $\frac1n$)。",
        r"$\frac in$ 与 $\frac jn$ 混用成同一个变量。",
        r"上下限想当然写成 $[0,1]$ 之外的区间——$i,j$ 从 1 到 $n$ 时对应的就是 $[0,1]$。",
    ],
}
JIANGJIE[T12] = {
    'intuition': r"选择题里给你三四个二重积分让你排大小,**绝对不是让你把它们都算出来**。区域相同时,只比**被积函数在这片区域上谁大**;被积函数相同时,只比**区域谁包住谁**(前提是被积非负)。把两个被积函数一减、判个号,题就完了。",
    'trigger': r"选择题/判断题,几个 $I_1,I_2,I_3$ 只差被积函数(或只差积分区域),问大小关系或正负号。",
    'example_src': r"2019 真题 #5",
    'example_stem': r"设 $D=\{(x,y)\mid|x|+|y|\le\frac{\pi}{2}\}$,$I_1=\displaystyle\iint_D\sqrt{x^2+y^2}$,$I_2=\displaystyle\iint_D\sin\sqrt{x^2+y^2}$,$I_3=\displaystyle\iint_D(1-\cos\sqrt{x^2+y^2})$,比较大小。",
    'example_steps': [
        r"**统一记号**:三个被积函数都只依赖 $r=\sqrt{x^2+y^2}$,分别是 $r$、$\sin r$、$1-\cos r$。区域完全相同 → 只需在 $D$ 上比较这三个函数。",
        r"**定出 $r$ 的范围**:$D$ 是正方形(顶点在 $(\pm\frac{\pi}{2},0),(0,\pm\frac{\pi}{2})$),$r$ 最大在顶点处 $=\frac{\pi}{2}$。所以 $0\le r\le\frac{\pi}{2}$。",
        r"**比 $\sin r$ 与 $r$**:$0<r$ 时恒有 $\sin r<r$。",
        r"**比 $1-\cos r$ 与 $\sin r$**:$1-\cos r<\sin r\iff 2\sin^2\frac r2<2\sin\frac r2\cos\frac r2\iff\tan\frac r2<1\iff r<\frac{\pi}{2}$ —— 在区域内部成立。",
        r"**结论**:$1-\cos r<\sin r<r$ 在 $D$ 上(除边界点)处处成立,故 $I_3<I_2<I_1$。",
    ],
    'steps': [
        r"**先看变的是被积函数还是区域**,这决定了用哪条判据。",
        r"被积函数不同、区域相同 → **把两个被积函数相减判号**,或找出它们共同变量($r$)的取值范围再比较基本不等式。",
        r"区域不同、被积相同 → 被积非负时,**区域大的积分大**;注意先判被积函数的符号。",
        r"若被积函数含奇次项而区域对称,先用对称性把它归零,常常直接得出「等于 0」这种选项。",
    ],
    'variants': [
        r"**只差区域**:$J_i=\displaystyle\iint_{D_i}\sqrt[3]{x-y}$,三个 $D_i$ 层层包含(2016#3)。",
        r"**用对称性定号**:$I_k=\displaystyle\iint_{D_k}(y-x)$,$D_k$ 是单位圆的第 $k$ 象限部分(2013#3)。",
        r"**同款换函数**:$\cos\sqrt{x^2+y^2}$ vs $\cos(x^2+y^2)$ vs $\cos(x^2+y^2)^2$,$D:r\le1$(880-36)——比的是 $r,r^2,r^4$ 在 $[0,1]$ 上的大小再套 $\cos$ 的单调性。",
    ],
    'pitfalls': [
        r"**动手去算积分**——这类题算出来就输了(费时且常算不出)。",
        r"区域比较时忘了**被积函数必须非负**才有「区域大则积分大」。",
        r"$r$ 的取值范围搞错(本题最大是顶点的 $\frac{\pi}{2}$,不是边中点的距离)。",
    ],
}


for _n in ORDER:
    JIANGJIE.setdefault(_n, {})
    JIANGJIE[_n].update({'subject': SUBJECT, 'chapter': CHAPTER, 'point': POINT})

import figs_zjf as _G                                   # noqa: E402  数学图(内联 SVG)
for _n in ORDER:
    JIANGJIE[_n]['figures'] = _G.FIGS.get(_n, [])

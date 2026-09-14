"""Reviewed links from math II exam topics to the local Li Lin 880 workbook.

Numbers are the stable workbook IDs produced by build_880.py, not database IDs.
The existing method classifications remain separate: these sets identify useful
exercises for a knowledge point, and do not assert that every exercise has the
same solution method. Unlisted exercises remain available in their book chapter.
"""
from dataclasses import dataclass


FOCUS_YEARS = tuple(range(2020, 2027))


@dataclass(frozen=True)
class Chapter:
    key: str
    name: str
    book_chapter: str
    subject: str
    aliases: tuple[str, ...] = ()


CHAPTERS = (
    Chapter('limits', '函数、极限、连续', '函数极限连续', '高等数学'),
    Chapter('derivatives', '一元函数微分学', '一元函数微分学及其应用', '高等数学'),
    Chapter('integrals', '一元函数积分学', '一元函数积分学及其应用', '高等数学'),
    Chapter('multivariable', '多元函数微分学', '多元函数微分学及其应用', '高等数学'),
    Chapter('double-integrals', '二重积分', '二重积分', '高等数学', ('多元函数积分学',)),
    Chapter('ode', '常微分方程', '微分方程及其应用', '高等数学'),
    Chapter('determinants', '行列式', '行列式', '线性代数'),
    Chapter('matrices', '矩阵', '矩阵', '线性代数'),
    Chapter('vectors', '向量', '向量', '线性代数'),
    Chapter('linear-systems', '线性方程组', '线性方程组', '线性代数'),
    Chapter('eigenvalues', '特征值与相似对角化', '相似矩阵', '线性代数', ('矩阵的特征值与特征向量',)),
    Chapter('quadratic-forms', '二次型', '二次型', '线性代数'),
)
CHAPTER_BY_KEY = {chapter.key: chapter for chapter in CHAPTERS}
CHAPTER_ALIASES = {
    name: chapter.key for chapter in CHAPTERS
    for name in (chapter.name, chapter.book_chapter, *chapter.aliases)
}


@dataclass(frozen=True)
class Topic:
    key: str
    chapter: str
    name: str
    numbers: tuple[int, ...]
    aliases: tuple[str, ...] = ()


# Read against the stored workbook questions. Existing derivative, integral
# application and double-integral method groups supply their reviewed IDs.
TOPICS = (
    Topic('function-properties', 'limits', '函数的性质',
          (1, 2, 3, 14, 20, 41, 43, 54)),
    Topic('function-limits', 'limits', '函数极限的计算',
          (6, 17, 18, 19, 21, 25, 26, 45, 47, 51, 52, 53, 55, 56, 61, 62, 63, 64, 67, 71)),
    Topic('infinitesimals', 'limits', '无穷小量的比较',
          (7, 8, 27, 28, 29, 36, 44, 46, 66)),
    Topic('sequence-limits', 'limits', '数列极限与敛散性',
          (10, 11, 22, 33, 34, 35, 37, 38, 39, 48, 49, 50, 57, 58, 59, 65, 68, 69, 70, 72, 73, 74, 75, 76, 77),
          ('数列敛散性的判定',)),
    Topic('continuity', 'limits', '连续性与间断点',
          (12, 13, 16, 23, 24, 30, 31, 32, 42, 60), ('函数的连续性',)),

    Topic('derivative-definition', 'derivatives', '导数定义与可导性',
          (79, 80, 84, 90, 95, 163, 184, 201), ('导数概念与杂项',)),
    Topic('piecewise-derivative', 'derivatives', '分段函数的可导性',
          (78, 82, 83, 87, 91, 94, 160, 161, 165, 166, 183)),
    Topic('derivative-limit', 'derivatives', '用定义/极限求导数值(抽象函数)',
          (103, 106, 139, 140, 162, 171, 172, 173, 190, 203)),
    Topic('derivative-calculation', 'derivatives', '求导与微分计算',
          (115, 116, 129, 130, 131, 135, 186, 213), ('导数与微分',)),
    Topic('higher-derivatives', 'derivatives', '求具体高阶导数值',
          (92, 120, 159, 185, 198, 207, 208)),
    Topic('parametric-derivative', 'derivatives', '参数方程求导',
          (127, 133, 152, 153, 196)),
    Topic('implicit-derivative', 'derivatives', '隐函数求导', (105, 132)),
    Topic('inverse-derivative', 'derivatives', '反函数求导', (192, 195)),
    Topic('tangent-normal', 'derivatives', '隐式曲线的切线与法线',
          (112, 113, 118, 134, 216, 220)),
    Topic('tangent-parameters', 'derivatives', '两曲线相切求参数', (96, 214)),
    Topic('curvature', 'derivatives', '曲率与曲率半径',
          (121, 123, 126, 154, 178, 197, 215), ('曲率',)),
    Topic('related-rates', 'derivatives', '相关变化率', (137, 138, 202)),
    Topic('monotonicity', 'derivatives', '函数的单调性、极值与最值',
          (97, 98, 128, 150, 151, 155, 158, 167, 168, 170, 174, 175, 177, 182, 187, 188, 189, 200, 210, 211)),
    Topic('convexity', 'derivatives', '凹凸性、拐点与渐近线',
          (85, 86, 89, 99, 100, 101, 107, 111, 119, 124, 156, 157, 180, 181, 191, 217, 218),
          ('曲线的凹凸性、拐点及渐近线',)),
    Topic('mean-value-theorem', 'derivatives', '微分中值定理',
          (141, 142, 143, 144, 145, 146, 147, 148, 149, 204, 206, 217, 218, 219, 221)),
    Topic('taylor', 'derivatives', '泰勒公式', (109, 110, 117, 205, 212)),

    Topic('indefinite-integrals', 'integrals', '不定积分的计算',
          (223, 224, 228, 241, 264, 265, 266, 267, 285, 315, 331, 332, 353)),
    Topic('definite-integrals', 'integrals', '定积分的计算',
          (232, 252, 268, 269, 270, 271, 274, 297, 319, 320, 322, 323, 324, 329, 330, 334, 348, 350, 351, 352, 360)),
    Topic('integral-properties', 'integrals', '定积分的性质与不等式',
          (225, 230, 231, 233, 234, 276, 277, 288, 289, 290, 291, 292, 293, 294, 295, 355, 356, 357, 383, 386, 387, 388, 389),
          ('定积分的概念、性质及几何意义',)),
    Topic('riemann-sums', 'integrals', '定积分定义与和式极限',
          (229, 262, 307, 328, 344, 345, 346, 347)),
    Topic('variable-integrals', 'integrals', '变限积分',
          (226, 227, 235, 243, 244, 245, 246, 248, 273, 275, 278, 286, 287, 299, 300, 301, 308, 317, 337, 342, 343, 361)),
    Topic('improper-integrals', 'integrals', '反常积分的计算与敛散性',
          (238, 239, 240, 272, 296, 302, 303, 304, 305, 306, 326, 349)),
    Topic('area', 'integrals', '平面图形面积', (254, 258, 280, 298, 310, 358, 375, 378, 380)),
    Topic('volume', 'integrals', '旋转体体积',
          (255, 259, 281, 283, 362, 364, 365, 366, 368, 369, 370, 371, 372, 376, 377, 381, 384)),
    Topic('arc-length', 'integrals', '弧长', (256, 257, 282, 284, 312, 313, 363)),
    Topic('physical-integrals', 'integrals', '定积分的物理应用',
          (253, 261, 263, 321, 373, 374, 382), ('物理/其他应用',)),

    Topic('partial-derivatives', 'multivariable', '偏导数的概念与计算',
          (390, 391, 392, 393, 394, 398, 403, 407, 408, 416, 425, 426, 427, 430, 431, 433, 436, 437, 441, 454, 456, 460, 461, 462)),
    Topic('total-differential', 'multivariable', '全微分的概念与计算',
          (402, 409, 411, 413, 414, 430, 432, 435, 452, 453, 454, 455)),
    Topic('implicit-partials', 'multivariable', '隐函数的偏导数计算',
          (395, 404, 405, 406, 409, 412, 417, 434, 440, 442, 458)),
    Topic('multivariable-extrema', 'multivariable', '多元函数的极值问题',
          (396, 397, 415, 421, 422, 423, 424, 428, 429, 445, 447, 448, 449, 450, 451, 452, 453, 457, 459, 460, 462)),

    Topic('double-comparison', 'double-integrals', '二重积分比较大小', (463, 498, 499)),
    Topic('double-symmetry', 'double-integrals', '对称性化简',
          (464, 465, 473, 474, 475, 479, 481, 513, 516, 518, 533, 540)),
    Topic('double-order', 'double-integrals', '累次积分换序',
          (466, 469, 470, 471, 507, 508, 509), ('交换积分次序与坐标系之间的转化',)),
    Topic('double-polar-conversion', 'double-integrals', '累次积分化极坐标', (467, 468, 501, 502, 520)),
    Topic('double-variable', 'double-integrals', '含参变限二重积分',
          (472, 482, 504, 521, 522, 526, 529, 535)),
    Topic('double-polar', 'double-integrals', '极坐标·单一边界',
          (476, 496, 510, 517, 524, 531, 539)),
    Topic('double-polar-split', 'double-integrals', '极坐标·分段边界', (477, 484, 486, 490, 514)),
    Topic('double-substitution', 'double-integrals', '一般换元(雅可比)', (478, 485, 515, 519, 534, 538)),
    Topic('double-cartesian', 'double-integrals', '直角坐标·选序计算',
          (480, 483, 497, 506, 523, 525, 536), ('重积分的计算',)),
    Topic('double-piecewise', 'double-integrals', '绝对值与分段被积函数',
          (487, 488, 489, 491, 492, 493, 494, 495, 505, 511, 512, 537)),
    Topic('double-sums', 'double-integrals', '和式极限化二重积分', (500,)),
    Topic('double-equations', 'double-integrals', '含二重积分的方程', (503, 527, 528, 530, 532)),

    Topic('ode-separable', 'ode', '可分离变量与齐次微分方程',
          (541, 549, 550, 578, 598, 601), ('可分离变量的微分方程与齐次方程',)),
    Topic('ode-first-order', 'ode', '一阶线性微分方程',
          (542, 547, 548, 559, 566, 567, 574, 579, 582, 586, 596, 597, 603, 607),
          ('一阶非齐次线性微分方程',)),
    Topic('ode-constant', 'ode', '常系数线性微分方程',
          (543, 546, 552, 553, 556, 558, 560, 568, 569, 573, 576, 580, 581, 583, 584, 590, 594, 595),
          ('常系数齐次线性微分方程', '常系数非齐次线性微分方程')),
    Topic('ode-structure', 'ode', '线性微分方程的解的结构', (544, 545, 555, 571, 572)),
    Topic('ode-substitution', 'ode', '微分方程的换元与降阶',
          (554, 557, 563, 575, 577, 587, 588, 589, 605, 606, 608, 616), ('其他方程',)),
    Topic('ode-geometry', 'ode', '微分方程的几何应用',
          (564, 565, 604, 605, 606, 608, 609, 610, 611), ('由切线几何条件反求曲线',)),
    Topic('ode-physics', 'ode', '微分方程的物理应用', (612, 613, 614)),

    Topic('determinant-calculation', 'determinants', '行列式的计算与性质',
          (618, 619, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 633, 634, 635, 636, 640, 641, 643, 645, 648, 649, 650, 651),
          ('行列式·未拆分',)),
    Topic('cofactors', 'determinants', '余子式与代数余子式', (617, 620, 632, 637, 638, 647, 655)),
    Topic('matrix-operations', 'matrices', '矩阵的运算与变换',
          (656, 660, 667, 668, 674, 677, 687, 688, 689, 690, 693, 696, 697, 706, 708, 710, 711)),
    Topic('matrix-inverse', 'matrices', '伴随矩阵与可逆矩阵',
          (657, 658, 668, 670, 671, 672, 673, 674, 676, 678, 679, 681, 683, 684, 685, 692, 696, 697, 698, 699, 703, 707)),
    Topic('matrix-rank', 'matrices', '矩阵的秩', (659, 661, 662, 669, 691, 692, 694, 695, 702)),
    Topic('vector-dependence', 'vectors', '向量组的线性相关性',
          (712, 713, 714, 715, 717, 718, 719, 727, 729, 730, 732, 740, 742, 743, 744)),
    Topic('vector-representation', 'vectors', '向量组之间的线性表示',
          (712, 715, 721, 722, 723, 724, 725, 731, 732, 734, 735, 736, 738, 739, 741)),
    Topic('vector-basis', 'vectors', '极大无关组与向量组的秩', (722, 724, 726, 728, 737, 745)),
    Topic('linear-solutions', 'linear-systems', '线性方程组的解与基础解系',
          (747, 750, 752, 756, 762, 763, 765, 766, 768, 769, 770, 771, 774, 783, 787, 788, 789, 793),
          ('线性方程组·未拆分',)),
    Topic('linear-parameters', 'linear-systems', '线性方程组的有解判定与参数讨论',
          (751, 753, 755, 760, 761, 764, 772, 773, 775, 780, 781, 782, 793, 799, 800)),
    Topic('linear-common', 'linear-systems', '同解与公共解',
          (748, 749, 757, 758, 765, 766, 767, 776, 777, 795, 796, 797)),
    Topic('eigenvalues', 'eigenvalues', '特征值与特征向量',
          (801, 805, 808, 809, 811, 812, 815, 819, 822, 823, 826, 829, 832, 833, 834, 837, 838, 839, 840, 842, 844, 845, 849)),
    Topic('diagonalization', 'eigenvalues', '相似矩阵与对角化',
          (802, 803, 804, 807, 810, 813, 814, 815, 816, 817, 818, 819, 820, 821, 824, 827, 828, 830, 831, 835, 836, 841, 842, 846, 847, 848, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862),
          ('矩阵的特征值与特征向量·未拆分',)),
    Topic('quadratic-standard', 'quadratic-forms', '二次型的标准形与正交变换',
          (863, 864, 870, 874, 875, 876, 879, 880, 883, 892, 902, 903, 909, 910, 912, 913, 914, 916, 918, 919, 920, 921, 922, 925)),
    Topic('quadratic-inertia', 'quadratic-forms', '二次型的规范形与惯性指数',
          (867, 868, 872, 879, 884, 885, 887, 891, 893, 894, 895, 896, 898, 899, 900, 902, 904, 919),
          ('二次型·未拆分',)),
    Topic('quadratic-congruence', 'quadratic-forms', '合同变换与二次型',
          (865, 866, 868, 871, 882, 885, 886, 888, 891, 898, 908, 913, 914, 917, 923, 924)),
    Topic('quadratic-positive', 'quadratic-forms', '正定二次型与最值',
          (869, 873, 877, 890, 897, 901, 905, 906, 907, 914, 915, 917, 918)),
)
TOPIC_BY_KEY = {topic.key: topic for topic in TOPICS}
TOPIC_ALIASES = {name: topic.key for topic in TOPICS for name in (topic.name, *topic.aliases)}

# Source tags occasionally misidentify the topic (e.g. 2023 #20 is a double
# integral, and 2024 #11 / 2026 #13 are curvature). These links are reviewed
# against each original stem, keyed by paper/year/number rather than mutable IDs.
# A multi-part exam question may offer more than one relevant knowledge point.
EXAM_TOPICS = {
    (2020, 6): ('monotonicity', 'mean-value-theorem'),
    (2020, 7): ('matrix-inverse', 'linear-solutions'),
    (2020, 8): ('diagonalization',),
    (2020, 14): ('determinant-calculation',),
    (2020, 20): ('mean-value-theorem', 'variable-integrals'),
    (2020, 21): ('ode-geometry',),
    (2020, 22): ('quadratic-congruence', 'quadratic-inertia'),
    (2020, 23): ('diagonalization', 'matrix-inverse'),
    (2021, 3): ('related-rates', 'partial-derivatives'),
    (2021, 8): ('quadratic-inertia',),
    (2021, 14): ('double-variable',),
    (2021, 16): ('determinant-calculation',),
    (2021, 19): ('arc-length',),
    (2021, 20): ('ode-first-order', 'tangent-normal'),
    (2021, 22): ('diagonalization',),
    (2022, 6): ('sequence-limits',),
    (2022, 7): ('integral-properties',),
    (2022, 9): ('linear-parameters',),
    (2022, 10): ('vector-representation',),
    (2022, 18): ('ode-first-order', 'arc-length'),
    (2022, 20): ('multivariable-extrema', 'partial-derivatives'),
    (2022, 21): ('integral-properties', 'convexity'),
    (2022, 22): ('quadratic-standard', 'quadratic-positive'),
    (2023, 7): ('monotonicity', 'convexity'),
    (2023, 9): ('quadratic-inertia',),
    (2023, 13): ('implicit-partials',),
    (2023, 16): ('determinant-calculation',),
    (2023, 17): ('ode-geometry',),
    (2023, 19): ('volume', 'area'),
    (2023, 20): ('double-polar', 'double-substitution'),
    (2023, 22): ('diagonalization', 'matrix-operations'),
    (2024, 8): ('matrix-operations', 'matrix-inverse'),
    (2024, 9): ('matrix-inverse', 'matrix-rank'),
    (2024, 10): ('diagonalization',),
    (2024, 11): ('curvature',),
    (2024, 13): ('ode-substitution',),
    (2024, 18): ('ode-substitution',),
    (2024, 19): ('volume', 'monotonicity'),
    (2024, 21): ('mean-value-theorem', 'integral-properties'),
    (2024, 22): ('quadratic-standard', 'linear-common'),
    (2025, 1): ('implicit-partials',),
    (2025, 2): ('monotonicity', 'convexity', 'variable-integrals'),
    (2025, 8): ('eigenvalues', 'quadratic-inertia'),
    (2025, 13): ('riemann-sums',),
    (2025, 15): ('ode-separable',),
    (2025, 16): ('linear-solutions', 'vector-dependence'),
    (2025, 19): ('total-differential', 'multivariable-extrema'),
    (2025, 21): ('mean-value-theorem', 'convexity'),
    (2025, 22): ('quadratic-congruence', 'quadratic-standard'),
    (2026, 3): ('implicit-partials',),
    (2026, 6): ('inverse-derivative', 'variable-integrals'),
    (2026, 9): ('matrix-operations', 'linear-parameters'),
    (2026, 13): ('curvature',),
    (2026, 14): ('partial-derivatives', 'total-differential'),
    (2026, 15): ('definite-integrals', 'integral-properties'),
    (2026, 16): ('quadratic-inertia', 'matrix-rank'),
    (2026, 20): ('volume', 'convexity'),
    (2026, 21): ('ode-substitution',),
    (2026, 22): ('vector-basis', 'matrix-operations'),
}


def source_topics(question):
    if question['paper'] == 'math2':
        explicit = EXAM_TOPICS.get((question['year'], question['number']))
        if explicit:
            return [TOPIC_BY_KEY[key] for key in explicit]
    for name in (question['type_name'], question['point']):
        if name in TOPIC_ALIASES:
            return [TOPIC_BY_KEY[TOPIC_ALIASES[name]]]
    return []


def source_chapter(question):
    topics = source_topics(question)
    return topics[0].chapter if topics else CHAPTER_ALIASES.get(question['chapter'])

# 李林880·数学二·线性代数题目全文（LaTeX版）

来源：【A4留白版】李林880数二线代篇做题本(1).pdf。
提取范围：原PDF第2–130页，共311道主问题；子问与选项保留在所属题目中。第1页目录用于恢复章节结构。
正文采用UTF-8文本，公式采用LaTeX。保留原章节、难度、题型、题号及来源页码，并增加Q001–Q311作为唯一编号。原文两道未编号的题标为“原文未编号”。
页眉页脚、宣传文字及做题留白不纳入题目。矩阵中原有的空白位置仍保留为空白；没有补写答案或缺失条件。原文疑点见文末校对说明。

| 章节 | 主问题数 |
|---|---:|
| 第七章行列式 | 39 |
| 第八章矩阵 | 56 |
| 第九章向量 | 37 |
| 第十章线性方程组 | 54 |
| 第十一章相似矩阵 | 62 |
| 第十二章二次型 | 63 |

## 第七章行列式

### 基础题 · 选择题

#### Q001｜原题(1)｜PDF第2页

设行列式

$$
D=\begin{vmatrix}3 & 0 & 4 & 0 \\
2 & 2 & 2 & 2 \\
0 & -7 & 0 & 0 \\
5 & 3 & -2 & 2\end{vmatrix},
$$

则$D$的第$4$行各元素的余子式之和$M_{41}+M_{42}+M_{43}+M_{44}=()$.

A.$-28$

B.$28$

C.$14$

D.$-14$

#### Q002｜原题(2)｜PDF第2页

设$\alpha_{1},\alpha_{2},\alpha_{3},\beta_{1},\beta_{2}$均是$4$维列向量，且$4$阶行列式$\left|\alpha_{1},\alpha_{2},\alpha_{3},\beta_{1}\right|=a,\left|\alpha_{1},\alpha_{2},\beta_{2},\alpha_{3}\right|=b$，则行列式$\left|\alpha_{3},\alpha_{2},\alpha_{1},\beta_{1}+\beta_{2}\right|=()$.

A.$a+b$

B.$a-b$

C.$b-a$

D.$-(a+b)$

#### Q003｜原题(3)｜PDF第2页

设$\beta_{1},\beta_{2},\alpha_{1},\alpha_{2},\alpha_{3}$均是$4$维列向量,且$\left|A\right|=\left|\beta_{1},\alpha_{1},\alpha_{2},\alpha_{3}\right|=1,\left|B\right|=\left|\beta_{2},\alpha_{1},3\alpha_{2},\alpha_{3}\right|=3$,则$\left|A+B\right|= ()$.

A.$15$

B.$16$

C.$31$

D.$32$

#### Q004｜原题(4)｜PDF第3页

设$3$阶矩阵$A=(a_{ij})_{3\times 3}$满足$A^{T}=kA^{*}(k>0)$,若$a_{11}=a_{12}=a_{13}=c>0$,则$c=()$.

A.$\frac{\sqrt{3}}{3k}$

B.$\frac{\sqrt{3}k^{2}}{3}$

C.$\sqrt{3}k^{2}$

D.$\frac{\sqrt{3}}{k^{2}}$

### 基础题 · 填空题

#### Q005｜原题(1)｜PDF第3页

行列式

$$
\begin{vmatrix}k & 0 & -1 & 1 \\
0 & k & 1 & -1 \\
-1 & 1 & k & 0 \\
1 & -1 & 0 & k\end{vmatrix}=\underline{\qquad\qquad}.
$$

#### Q006｜原题(2)｜PDF第3页

若

$$
\begin{vmatrix}\lambda -a & -1 & -1 \\
-1 & \lambda -a & 1 \\
-1 & 1 & \lambda -a\end{vmatrix}=0,
$$

则$\lambda =\underline{\qquad\qquad}$.

#### Q007｜原题(3)｜PDF第4页

行列式

$$
D_{4}=\begin{vmatrix}1 & 0 & 0 & 1 \\
0 & 2 & 0 & 1 \\
0 & 0 & 3 & 1 \\
1 & 1 & 1 & 4\end{vmatrix}=\underline{\qquad\qquad}.
$$

#### Q008｜原题(4)｜PDF第4页

行列式

$$
D_{4}=\begin{vmatrix}0 & 1 & 2 & 0 \\
1 & 0 & 0 & 2 \\
0 & 3 & 4 & 0 \\
3 & 0 & 0 & 4\end{vmatrix}=\underline{\qquad\qquad}.
$$

#### Q009｜原题(5)｜PDF第4页

行列式

$$
D_{4}=\begin{vmatrix}a & -1 & 0 & 0 \\
0 & a & -1 & 0 \\
0 & 0 & a & -1 \\
4 & 3 & 2 & a+1\end{vmatrix}=\underline{\qquad\qquad}.
$$

#### Q010｜原题(6)｜PDF第5页

设

$$
f(x)=\begin{vmatrix}x & -2x & 1 & 2 \\
1 & x & 1 & -1 \\
3 & 2 & 3x & 1 \\
1 & 1 & 1 & x\end{vmatrix}
$$

，则$x^{3}$的系数为$\underline{\qquad\qquad}$.

#### Q011｜原题(7)｜PDF第5页

设$A$是$n$阶方阵,且$AA^{T}=E,\left|A\right|<0$，则$\left|A+E\right|=\underline{\qquad\qquad}$.

#### Q012｜原题(8)｜PDF第5页

设$A$是$n$阶方阵,$E$是$n$阶单位矩阵,且$A^{2}=A,A\ne E$,则$\left|A\right|=\underline{\qquad\qquad}$.

#### Q013｜原题(9)｜PDF第6页

设$A,B$均为$n$阶方阵,且$\left|A\right|=\left|B\right|=\left|A^{-1}+B\right|=2$,则$\left|A+B^{-1}\right|=\underline{\qquad\qquad}$.

#### Q014｜原题(10)｜PDF第6页

设$\left|A\right|=2,\left|B\right|=-2$，其中$A$，$B$均为$n$阶方阵，则$\left|A^{-1}B^{*}-A^{*}B^{-1}\right|=\underline{\qquad\qquad}$.

#### Q015｜原题(11)｜PDF第6页

设$3$阶方阵$A=(\alpha_{1},\alpha_{2},\alpha_{3}),B=(3\alpha_{1}-\alpha_{2},3\alpha_{2}-2\alpha_{1},2\alpha_{3}-\alpha_{1}-2\alpha_{2})$，且$\left|B\right|=14$，则$\left|A\right|=\underline{\qquad\qquad}$.

#### Q016｜原题(12)｜PDF第7页

设$A=(a_{ij})_{n\times n}$为$n$阶方阵,$\left|A\right|=1$,且$A$的每列元素之和均为$k(k\ne 0)$,则$A$的代数余子式之和$A_{11}+A_{12}+\cdots +A_{1n}=\underline{\qquad\qquad}$.

### 基础题 · 解答题

#### Q017｜原题(1)｜PDF第7页

计算$n$阶行列式

$$
D_{n}=\begin{vmatrix}b & a & a & \cdots  & a \\
a & b & a & \cdots  & a \\
\vdots  & \vdots  & \vdots  &  & \vdots  \\
a & a & a & \cdots  & b\end{vmatrix}.
$$

#### Q018｜原题(2)｜PDF第8页

证明:

$$
D_{n}=\begin{vmatrix}x & -1 & 0 & \cdots  & 0 & 0 \\
0 & x & -1 & \cdots  & 0 & 0 \\
\vdots  & \vdots  & \vdots  &  & \vdots  & \vdots  \\
0 & 0 & 0 & \cdots  & x & -1 \\
a_{n} & a_{n-1} & a_{n-2} & \cdots  & a_{2} & x+a_{1}\end{vmatrix}=x^{n}+\sum_{i=1}^{n}a_{i}x^{n-i}.
$$

#### Q019｜原题(3)｜PDF第8页

计算$n$阶行列式

$$
D_{n}=\begin{vmatrix}2 & -1 & 0 & \cdots  & 0 & 0 \\
-1 & 2 & -1 & \cdots  & 0 & 0 \\
0 & -1 & 2 & \cdots  & 0 & 0 \\
\vdots  & \vdots  & \vdots  &  & \vdots  & \vdots  \\
0 & 0 & 0 & \cdots  & 2 & -1 \\
0 & 0 & 0 & \cdots  & -1 & 2\end{vmatrix}.
$$

#### Q020｜原题(4)｜PDF第9页

计算$n$阶行列式

$$
D_{n}=\begin{vmatrix}a_{1} & b_{1} & 0 & \cdots  & 0 & 0 \\
0 & a_{2} & b_{2} & \cdots  & 0 & 0 \\
\vdots  & \vdots  & \vdots  &  & \vdots  & \vdots  \\
0 & 0 & 0 & \cdots  & a_{n-1} & b_{n-1} \\
b_{n} & 0 & 0 & \cdots  & 0 & a_{n}\end{vmatrix}+\begin{vmatrix}a_{1} & 0 & 0 & \cdots  & 0 & b_{n} \\
b_{1} & a_{2} & 0 & \cdots  & 0 & 0 \\
0 & b_{2} & a_{3} & \cdots  & 0 & 0 \\
\vdots  & \vdots  & \vdots  &  & \vdots  & \vdots  \\
0 & 0 & 0 & \cdots  & a_{n-1} & 0 \\
0 & 0 & 0 & \cdots  & b_{n-1} & a_{n}\end{vmatrix},
$$

其中$a_{i},b_{i}$均不为$0$.

### 综合题 · 选择题

#### Q021｜原题(1)｜PDF第9页

设$A$是$3$阶可逆矩阵，$A^{-1}$的特征值为$3,2,1$，则$\left|A\right|$的代数余子式之和$A_{11}+A_{22}+A_{33}=()$.

A.$\frac{1}{6}$

B.$\frac{1}{3}$

C.$\frac{1}{2}$

D.$1$

#### Q022｜原题(2)｜PDF第10页

$$
\left|A\right|=\begin{vmatrix}0 & 0 & 0 & 1 \\
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0\end{vmatrix}
$$

的所有代数余子式$A_{ij}$之和$\sum_{i=1}^{4}\sum_{j=1}^{4}A_{ij}=()$.

A.$4$

B.$-4$

C.$1$

D.$-1$

#### Q023｜原题(3)｜PDF第10页

设$A$是$3$阶方阵，$A^{*}$是$A$的伴随矩阵，$\left|A\right|=\frac{1}{2}$，则$\left|(2A)^{-1}-2A^{*}\right|=()$.

A.$\frac{1}{2}$

B.$-\frac{1}{2}$

C.$-\frac{1}{4}$

D.$\frac{1}{4}$

#### Q024｜原题(4)｜PDF第10页

设

$$
f(x)=\begin{vmatrix}1 & x & x^{2} & x^{3} \\
1 & 2 & 4 & 8 \\
1 & -1 & 1 & -1 \\
1 & 1 & 1 & 1\end{vmatrix}
$$

，则曲线$y=f(x)$在$(-1,2)$内存在水平切线的条数为$()$。

A.$1$

B.$2$

C.$3$

D.$4$

### 综合题 · 填空题

#### Q025｜原题(1)｜PDF第11页

设$A,B$均为$n$阶方阵,

$$
\left|A\right|=6,\left|B\right|=1,C=\begin{pmatrix}A & 3A^{*} \\
(\frac{B}{2})^{-1} & O\end{pmatrix}
$$

，则$\left|C\right|=\underline{\qquad\qquad}$.

#### Q026｜原题(2)｜PDF第11页

设$A$是$m\times n$矩阵，$B$是$n\times m$矩阵，当$m>n$时，$\left|AB\right|=\underline{\qquad\qquad}$.

#### Q027｜原题(3)｜PDF第11页

设$A,B$均为$3$阶方阵,满足$A^{2}B-A-B=E$，若

$$
A=\begin{pmatrix}1 & 0 & 1 \\
0 & 2 & 0 \\
-2 & 0 & 1\end{pmatrix}
$$

，则$\left|B\right|=\underline{\qquad\qquad}$.

#### Q028｜原题(4)｜PDF第12页

设$A$是$3$阶方阵,且满足$\left|A-E\right|=\left|A+2E\right|=\left|2A+3E\right|=0$，则$\left|2A^{*}-3E\right|=\underline{\qquad\qquad}$.

#### Q029｜原题(5)｜PDF第12页

设$A$是$3$阶方阵,$\alpha_{1},\alpha_{2},\alpha_{3}$线性无关,且$A\alpha_{1}=\alpha_{1}+\alpha_{2},A\alpha_{2}=\alpha_{2}+\alpha_{3},A\alpha_{3}=\alpha_{3}+\alpha_{1}$,则$\left|A\right|=\underline{\qquad\qquad}$.

#### Q030｜原题(6)｜PDF第12页

设$\alpha,\beta,\alpha_{1},\alpha_{2},\alpha_{3}$均为$4$维列向量,$A=(\alpha,\alpha_{1},\alpha_{2},\alpha_{3}),B=(\beta,\alpha_{1},\alpha_{2},\alpha_{3})$,且$\left|A\right|=2,\left|B\right|=1$,则$\left|A^{-1}+B^{-1}\right|=\underline{\qquad\qquad}$.

#### Q031｜原题(7)｜PDF第13页

设$n$阶行列式

$$
\left|A\right|=\begin{vmatrix}0 & 1 & 0 & \cdots  & 0 \\
0 & 0 & 2 & \cdots  & 0 \\
\vdots  & \vdots  & \vdots  &  & \vdots  \\
0 & 0 & 0 & \cdots  & n-1 \\
n & 0 & 0 & \cdots  & 0\end{vmatrix}
$$

，则$\left|A\right|$的第$k$行元素的代数余子式之和$A_{k1}+A_{k2}+\cdots +A_{kn}=\underline{\qquad\qquad}$.

### 综合题 · 解答题

#### Q032｜原题(1)｜PDF第13页

计算$n$阶行列式

$$
D_{n}=\begin{vmatrix}b-a_{1}^{2} & -a_{1}a_{2} & \cdots  & -a_{1}a_{n} \\
-a_{2}a_{1} & b-a_{2}^{2} & \cdots  & -a_{2}a_{n} \\
\vdots  & \vdots  &  & \vdots  \\
-a_{n}a_{1} & -a_{n}a_{2} & \cdots  & b-a_{n}^{2}\end{vmatrix}.
$$

#### Q033｜原题(2)｜PDF第13页

计算$n$阶行列式

$$
D_{n}=\begin{vmatrix}a+b_{1} & a & \cdots  & a \\
a & a+b_{2} & \cdots  & a \\
\vdots  & \vdots  &  & \vdots  \\
a & a & \cdots  & a+b_{n}\end{vmatrix}(b_{i}\ne 0).
$$

#### Q034｜原题(3)｜PDF第14页

计算$n$阶行列式

$$
D_{n}=\begin{vmatrix}a_{0} & -1 & 0 & \cdots  & 0 & 0 \\
a_{1} & x & -1 & \cdots  & 0 & 0 \\
a_{2} & 0 & x & \cdots  & 0 & 0 \\
\vdots  & \vdots  & \vdots  &  & \vdots  & \vdots  \\
a_{n-2} & 0 & 0 & \cdots  & x & -1 \\
a_{n-1} & 0 & 0 & \cdots  & 0 & x\end{vmatrix}.
$$

#### Q035｜原题(4)｜PDF第14页

计算

$$
D_{n}=\begin{vmatrix}a & b & 0 & \cdots  & 0 & 0 \\
c & a & b & \cdots  & 0 & 0 \\
0 & c & a & \cdots  & 0 & 0 \\
\vdots  & \vdots  & \vdots  &  & \vdots  & \vdots  \\
0 & 0 & 0 & \cdots  & a & b \\
0 & 0 & 0 & \cdots  & c & a\end{vmatrix}(a^{2}-4bc\ge 0).
$$

### 拓展题 · 解答题

#### Q036｜原题(1)｜PDF第15页

设矩阵$A$为$3$阶非零实矩阵,$A^{T}=A^{*}$,且$\left|E+A\right|=\left|E-A\right|=0$,计算行列式$\left|A^{2}-A-3E\right|$.

#### Q037｜原题(2)｜PDF第15页

设$A$为$3$阶非零实矩阵，且$A^{T}=kA^{*}(k$为非零常数$)$.

(I)证明:$A$是可逆矩阵;

(II)求行列式$\left|A^{-1}\right|+\left|(A^{*})^{-1}\right|$.

#### Q038｜原题(3)｜PDF第15页

设$3$阶矩阵$A$的特征值为$1,-1,2$，计算行列式

$$
\left|\left|A\right|\cdot \begin{pmatrix}O & A^{*} \\
-2E & A\end{pmatrix}\right|.
$$

#### Q039｜原题(4)｜PDF第16页

设行列式

$$
\left|A\right|=\begin{vmatrix}2 & 2 & 2 & 2 \\
1 & a_{1} & a_{2} & a_{3} \\
1 & b_{1} & b_{2} & b_{3} \\
1 & c_{1} & c_{2} & c_{3}\end{vmatrix}=1,A_{ij}
$$

是$\left|A\right|$中元素$a_{ij}$的代数余子式，求$\sum_{i=1}^{4}\sum_{j=1}^{4}A_{ij}$.

## 第八章矩阵

### 基础题 · 选择题

#### Q040｜原题(1)｜PDF第17页

设

$$
A=(a_{ij})_{3\times 3},B=\begin{pmatrix}a_{21} & a_{22}+a_{23} & a_{23} \\
a_{31} & a_{32}+a_{33} & a_{33} \\
a_{11} & a_{12}+a_{13} & a_{13}\end{pmatrix},P=\begin{pmatrix}0 & 1 & 0 \\
0 & 0 & 1 \\
1 & 0 & 0\end{pmatrix},Q=\begin{pmatrix}1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 1 & 1\end{pmatrix}
$$

，则$B=()$.

A.$AQP$

B.$PAQ$

C.$QAP$

D.$APQ$

#### Q041｜原题(2)｜PDF第17页

设$A$是$n(n\ge 3)$阶可逆方阵，下列结论正确的是$()$.

①$(A^{*})^{-1}=(A^{-1})^{*}$；②$(kA)^{*}=k^{n-1}A^{*}(k\ne 0)$；

③$(A^{*})^{T}=(A^{T})^{*}$；④$(A^{*})^{*}=\left|A\right|^{n-2}A$.

A.①②

B.②③

C.③④

D.①②③④

#### Q042｜原题(3)｜PDF第17页

设

$$
A=\begin{pmatrix}1 & 0 & 1 \\
2 & 1 & 0 \\
-3 & 2 & -5\end{pmatrix}
$$

，则行列式$\left|[(E-A)^{*}]^{-1}\right|=()$.

A.$\frac{1}{4}$

B.$-\frac{1}{4}$

C.$\frac{1}{16}$

D.$-\frac{1}{16}$

#### Q043｜原题(4)｜PDF第18页

设矩阵

$$
A=\begin{pmatrix}1 & 1 & 1 \\
0 & 1 & 0 \\
2 & k & 3 \\
k-1 & 5 & 1\end{pmatrix}
$$

与

$$
B=\begin{pmatrix}1 & 1 & 1 \\
0 & 1 & -1 \\
2 & 3 & k \\
3 & 5 & 1\end{pmatrix}
$$

等价,则$()$.

A.$k=1$

B.$k\ne 1$

C.$k=-1$

D.$k\ne -1$

#### Q044｜原题(5)｜PDF第18页

设

$$
A=\begin{pmatrix}a_{1} & a_{2} & a_{3} \\
b_{1} & b_{2} & b_{3} \\
c_{1} & c_{2} & c_{3}\end{pmatrix},B=\begin{pmatrix}b_{1} & b_{3} & b_{2} \\
a_{1} & a_{3} & a_{2} \\
c_{1}+a_{1} & c_{3}+a_{3} & c_{2}+a_{2}\end{pmatrix},
$$

则$()$.

A.$\left|A\right|=-\left|B\right|$

B.$2\left|A\right|=\left|B\right|$

C.$\left|A\right|=2\left|B\right|$

D.$\left|A\right|=\left|B\right|$

#### Q045｜原题(6)｜PDF第18页

设

$$
A=\begin{pmatrix}1 & 0 & -1 \\
2 & a & 1 \\
1 & 2 & 1\end{pmatrix},B
$$

是$3$阶矩阵,且$r(B)=2,r(AB)=1,A^{*}$与$B^{*}$分别是$A$与$B$的伴随矩阵,则正确的是$()$.

A.

$$
r[\begin{pmatrix}A^{*} & O \\
A & B\end{pmatrix}]=3
$$

B.

$$
r[\begin{pmatrix}A & O \\
O & B^{*}\end{pmatrix}]=3
$$

C.

$$
r[\begin{pmatrix}A^{*} & B \\
O & A\end{pmatrix}]=3
$$

D.

$$
r[\begin{pmatrix}A & B^{*} \\
O & B\end{pmatrix}]=3
$$

#### Q046｜原题(7)｜PDF第19页

设$A,B$分别为$m\times n,n\times s$矩阵，且$AB=C$，则正确的是$()$.

A.若$r(C)=m$，则$r(A)\le m$

B.若$r(C)=s$，则$r(B)\le s$

C.若$r(A)=n$,则$r(B)\le r(C)$

D.若$r(A)=n$,则$r(B)=r(C)$

### 基础题 · 填空题

#### Q047｜原题(1)｜PDF第19页

设$\alpha =(1,2,3)^{T},\beta =(1,\frac{1}{2},\frac{1}{3})^{T},A=\alpha \beta^{T}$,则$A^{n}=\underline{\qquad\qquad}$.

#### Q048｜原题(2)｜PDF第19页

设$\alpha =(2,-1,3)^{T},\beta =(1,2,0)^{T},A=\alpha \beta^{T},E$是$3$阶单位矩阵，则$(A+E)^{n}=\underline{\qquad\qquad}$.

#### Q049｜原题(3)｜PDF第20页

设

$$
A=\begin{pmatrix}1 & 0 & 1 \\
0 & 2 & 0 \\
1 & 0 & 1\end{pmatrix},
$$

则$A^{n}=\underline{\qquad\qquad}$.

#### Q050｜原题(4)｜PDF第20页

设

$$
A=\begin{pmatrix}1 & 1 & 1 \\
0 & 1 & 1 \\
0 & 0 & -1\end{pmatrix},
$$

则$A^{18}=\underline{\qquad\qquad}$.

#### Q051｜原题(5)｜PDF第20页

设

$$
B=\begin{pmatrix}0 & -1 & 0 \\
1 & 0 & 0 \\
0 & 0 & 1\end{pmatrix},A=P^{-1}BP,
$$

则$A^{4}-2B^{2}=\underline{\qquad\qquad}$.

#### Q052｜原题(6)｜PDF第21页

设$A$是$n$阶方阵,且$\left|A\right|=2$,将$A$的第$i$行与第$j$行互换得到$B$,则行列式$\left|B^{-1}B^{*}B^{T}\right|=\underline{\qquad\qquad}$.

#### Q053｜原题(7)｜PDF第21页

设

$$
A=\begin{pmatrix}1 & 2 & 3 & 4 \\
2 & 3 & 4 & 5 \\
3 & 4 & 5 & 6 \\
4 & 5 & 6 & 7\end{pmatrix},
$$

则$r(A)=\underline{\qquad\qquad}$.

#### Q054｜原题(8)｜PDF第21页

若$A^{n}=O,n$为正整数，则$(E-A)^{-1}=\underline{\qquad\qquad}$.

#### Q055｜原题(9)｜PDF第22页

若$A^{n}=E,n$为正整数，则$(A^{*})^{n}=\underline{\qquad\qquad}$.

#### Q056｜原题(10)｜PDF第22页

设方阵$A$满足$A^{2}-3A-2E=O$，则$A^{-1}=\underline{\qquad\qquad}$.

#### Q057｜原题(11)｜PDF第22页

设方阵$A$满足$A^{2}=A$，则$(A+E)^{-1}=\underline{\qquad\qquad}$.

#### Q058｜原题(12)｜PDF第23页

设$A$是$n$阶可逆矩阵，将$A$的第$i$行和第$j$行交换得$B$，则行列式$\left|AB^{-1}\right|=\underline{\qquad\qquad}$.

#### Q059｜原题(13)｜PDF第23页

设$\alpha =(k,0,\cdots,0,k)^{T}(k\ne 0)$，且$A=E-\alpha \alpha^{T},A^{-1}=E+\frac{1}{k}\alpha \alpha^{T}$，则$k=\underline{\qquad\qquad}$.

#### Q060｜原题(14)｜PDF第23页

设$\alpha,\beta,\gamma$均为$3$维列向量，$A=(\alpha,\beta,\gamma),\left|A\right|=1,B=(\alpha +\beta,\beta +\gamma,\beta +2\gamma)$，则$\left|(A^{-1}+B^{-1})^{*}\right|=\underline{\qquad\qquad}$.

### 基础题 · 解答题

#### Q061｜原题(1)｜PDF第24页

设

$$
A=\begin{pmatrix}2 & -1 & 3 \\
a & 1 & b \\
4 & c & 6\end{pmatrix},
$$

且$BA=O,B$是$3$阶方阵,$r(B)>1$,求$A^{n}$.

#### Q062｜原题(2)｜PDF第24页

设$\alpha,\beta$是$n$维列向量，且$\alpha^{T}\beta =2$，证明:$A=E+\alpha \beta^{T}$可逆，并求$A^{-1}$.

#### Q063｜原题(3)｜PDF第24页

设

$$
A^{-1}=\begin{pmatrix}1 & 1 & 1 \\
1 & 2 & 1 \\
1 & 1 & 3\end{pmatrix},
$$

求$(A^{*})^{-1}$.

#### Q064｜原题(4)｜PDF第25页

设

$$
A=\begin{pmatrix}2 & 1 & 1 \\
1 & 2 & 1 \\
1 & 1 & 2\end{pmatrix},
$$

证明:$A^{2}=5A-4E$,并求$A^{-1}$.

#### Q065｜原题(5)｜PDF第25页

设方阵$A,B$满足$\left|B\right|\ne 0,(A-E)^{-1}=(B-E)^{T}$,求$A^{-1}($用$B$表示$)$.

#### Q066｜原题(6)｜PDF第25页

设

$$
A=\begin{pmatrix}1 & 0 & 0 \\
2 & 3 & 0 \\
0 & 4 & 5\end{pmatrix},B=(E+A)^{-1}(E-A),
$$

求$[(E+B)^{2}]^{-1}$.

#### Q067｜原题(7)｜PDF第26页

已知方阵$A,B,(A+B)$均可逆,求$(A^{-1}+B^{-1})^{-1}$.

#### Q068｜原题(8)｜PDF第26页

设$A$为$2n+1$阶正交矩阵，且$\left|A\right|=1$，证明:$A-E$不可逆.

#### Q069｜原题(9)｜PDF第26页

设$n$阶方阵$A,B$，满足$A^{2}=E,B^{2}=E$，且$\left|A\right|+\left|B\right|=0$，证明:$A+B$不可逆.

#### Q070｜原题(10)｜PDF第27页

设

$$
A=\begin{pmatrix}1 & 0 & 1 \\
0 & 2 & 0 \\
-1 & 0 & 1\end{pmatrix},AB+E=A^{2}+B,
$$

求$B$.

#### Q071｜原题(11)｜PDF第27页

设

$$
A=\begin{pmatrix}0 & 2 \\
1 & 2\end{pmatrix},
$$

且$(A^{T}B^{-1})^{T}-A(B^{T}A)^{-1}=(E-B^{-1})^{T}$,求$B$.

#### Q072｜原题(12)｜PDF第27页

设

$$
A=\begin{pmatrix}\frac{1}{3} & 0 & 0 \\
0 & \frac{1}{4} & 0 \\
0 & 0 & \frac{1}{7}\end{pmatrix},A^{-1}BA=6A+BA,
$$

求$B$.

#### Q073｜原题(13)｜PDF第28页

设

$$
A=\begin{pmatrix}0 & 1 & 0 \\
1 & 0 & 0 \\
0 & 0 & 1\end{pmatrix},B=\begin{pmatrix}1 & 0 & 0 \\
0 & 0 & 1 \\
0 & 1 & 0\end{pmatrix},C=\begin{pmatrix}1 & -4 & 3 \\
2 & 0 & -1 \\
1 & -2 & 0\end{pmatrix},
$$

满足$AXB=C$,求矩阵$X$.

#### Q074｜原题(14)｜PDF第28页

设矩阵$A$满足

$$
A\begin{pmatrix}1 & 2 \\
0 & 1\end{pmatrix}=\begin{pmatrix}2 & 1 \\
3 & 2\end{pmatrix}A,
$$

求矩阵$A$.

### 综合题 · 选择题

#### Q075｜原题(1)｜PDF第28页

设

$$
A=\begin{pmatrix}1 & 2 & k \\
1 & k+1 & 1 \\
k & 2 & 1\end{pmatrix}
$$

，$B$是$3$阶非零矩阵，且$AB=O$，则$()$.

A.当$k=1$时，$r(B)=1$

B.当$k=-3$时，$r(B)=1$

C.当$k=1$时，$r(B)=2$

D.当$k=-3$时,$r(B)=2$

#### Q076｜原题(2)｜PDF第29页

设

$$
A=\begin{pmatrix}a & b & b \\
b & a & b \\
b & b & a\end{pmatrix}(a,b\text{均不为}0)
$$

，且$r(A^{*})=1$，则必有$()$.

A.$a=b$

B.$a=b$或$a+2b\ne 0$

C.$a+2b=0$

D.$a\ne b$且$a+2b\ne 0$

#### Q077｜原题(3)｜PDF第29页

设

$$
A=\begin{pmatrix}a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}\end{pmatrix},P=\begin{pmatrix}0 & 0 & 1 \\
0 & 1 & 0 \\
1 & 0 & 0\end{pmatrix},
$$

且$P^{n}AP^{m}=A$,则正整数$n,m$可以为$()$.

A.$n=m=4$

B.$n=5,m=4$

C.$n=4,m=5$

D.$n=m=5$

#### Q078｜原题(4)｜PDF第29页

设$A,B$均为$n$阶矩阵，$E$为$n$阶单位矩阵，矩阵

$$
\begin{pmatrix}O & A \\
B & E\end{pmatrix},\begin{pmatrix}A & B \\
O & E\end{pmatrix}
$$

，

$$
\begin{pmatrix}A & AB \\
E & B\end{pmatrix}
$$

的秩分别为$r_{1},r_{2}$,$r_{3}$，则正确的是$()$.

A.$r_{2}\ge r_{1}\ge r_{3}$

B.$r_{3}\ge r_{1}=r_{2}$

C.$r_{1}\ge r_{2}\ge r_{3}$

D.$r_{3}\ge r_{2}\ge r_{1}$

#### Q079｜原题(5)｜PDF第30页

设$n$阶非零实矩阵$A$满足$A^{T}+A=O,B$为$n$阶矩阵,矩阵

$$
\begin{pmatrix}A & E \\
-B & B\end{pmatrix},\begin{pmatrix}A-E & O \\
A & AB\end{pmatrix},
$$

$$
\begin{pmatrix}A+E & O \\
B & A-E\end{pmatrix}
$$

的秩依次为$r_{1},r_{2},r_{3}$,则$()$.

A.$r_{1}\ge r_{2}\ge r_{3}$

B.$r_{3}\ge r_{2}\ge r_{1}$

C.$r_{2}\ge r_{1}\ge r_{3}$

D.$r_{3}\ge r_{1}\ge r_{2}$

#### Q080｜原题(6)｜PDF第30页

下列命题中，正确的是$()$.

①若$A,B,C$均为$n$阶矩阵，且$ABC=E$，则$BCA=CAB$；

②若$A,B$均为$n$阶不可逆矩阵,则$A+B$必不可逆;

③若$A$，$B$均为$n$阶不可逆矩阵，则$AB$必不可逆；

④若$n$阶矩阵$A$，$B$满足$(AB)^{2}=E$，则$(BA)^{2}=E$.

A.①②③

B.①③④

C.②③④

D.①②④

#### Q081｜原题(7)｜PDF第30页

单位矩阵经过若干次互换两行得到的矩阵称为置换矩阵,设$A$为$n$阶置换矩阵,$A^{*}$为$A$的伴随矩阵,则下列说法正确的是$()$.

①$A^{T}$是置换矩阵;②$A^{-1}$是置换矩阵;

③$A^{*}$是置换矩阵;④$A^{-1}-A^{*}=O$.

A.①④

B.②③

C.①②

D.③④

### 综合题 · 填空题

#### Q082｜原题(1)｜PDF第31页

设$A,B$是$n$阶方阵,$\left|A\right|=2,\left|B\right|=3,A^{*},B^{*}$分别是$A,B$的伴随矩阵,

$$
C=\begin{pmatrix}A & O \\
O & B\end{pmatrix},
$$

则$C$的伴随矩阵$C^{*}=\underline{\qquad\qquad}$.

#### Q083｜原题(2)｜PDF第31页

设$A$是$n$阶可逆矩阵，$A$的每行元素之和均为$k$，则$A^{-1}$的每行元素之和均为$\underline{\qquad\qquad}$.

#### Q084｜原题(3)｜PDF第31页

设

$$
A=\begin{pmatrix}1 & -1 & -1 & -1 \\
-1 & 1 & -1 & -1 \\
-1 & -1 & 1 & -1 \\
-1 & -1 & -1 & 1\end{pmatrix},
$$

则$A^{n}(n\ge 1)=\underline{\qquad\qquad}$.

#### Q085｜原题(4)｜PDF第32页

设

$$
A=\begin{pmatrix}0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & 0 & 0\end{pmatrix},
$$

则$(E+A)^{-1}=\underline{\qquad\qquad}$.

#### Q086｜原题(5)｜PDF第32页

设$A,B$均为$n$阶可逆矩阵,且$AB=B^{-1}A^{-1}$,则$r(E+BA)+r(E-BA)=\underline{\qquad\qquad}$.

#### Q087｜原题(6)｜PDF第32页

设$A$是$3$阶非零矩阵,$A^{*}$为$A$的伴随矩阵,若$A^{*}+2A=O$,则$\operatorname{tr}[(A^{2})^{-1}]=\underline{\qquad\qquad}$.

### 综合题 · 解答题

#### Q088｜原题(1)｜PDF第33页

设

$$
A=\begin{pmatrix}0 & 0 & 0 & 1 \\
0 & 0 & 0 & 2 \\
0 & 0 & 0 & 3 \\
3 & 2 & 1 & 0\end{pmatrix},
$$

求$A^{n}(n\ge 1)$.

#### Q089｜原题(2)｜PDF第33页

设

$$
A=\begin{pmatrix}-1 & 1 & 1 & -1 \\
1 & -1 & -1 & 1 \\
1 & -1 & -1 & 1 \\
-1 & 1 & 1 & -1\end{pmatrix},
$$

证明:$A^{2}+4A=O$,并求$(E+A)^{-1}$.

#### Q090｜原题(3)｜PDF第33页

设

$$
A=\begin{pmatrix}0 & 1 & 0 \\
1 & 0 & 0 \\
0 & 1 & 1\end{pmatrix},
$$

证明:$A^{n}=A^{n-2}+A^{2}-E(n\ge 3)$,并计算$A^{100}$.

#### Q091｜原题(4)｜PDF第34页

设

$$
A=\begin{pmatrix}1 & 0 & 0 \\
0 & -2 & 0 \\
0 & 0 & 1\end{pmatrix},
$$

且$A^{*}BA=2BA-8E$,求$B$.

#### Q092｜原题(5)｜PDF第34页

设矩阵$X$满足

$$
\begin{pmatrix}1 & 0 & 1 \\
2 & 1 & -1 \\
-1 & -1 & 2\end{pmatrix}X=\begin{pmatrix}0 & 1 \\
2 & 0 \\
-2 & 1\end{pmatrix},
$$

求$X$.

#### Q093｜原题(6)｜PDF第34页

设分块矩阵

$$
P=\begin{pmatrix}A & C \\
O & B\end{pmatrix}
$$

为正交矩阵,$A,B$分别是$m$阶和$n$阶方阵,证明:$A$与$B$是正交矩阵.

### 拓展题 · 解答题

#### Q094｜原题(1)｜PDF第35页

设

$$
A=\begin{pmatrix}3 & 2 & 2 \\
0 & 1 & 1 \\
0 & 0 & 3\end{pmatrix},B=\begin{pmatrix}1 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & -1\end{pmatrix},
$$

若矩阵$X$满足$AX+2B=BA+2X$,求$X^{2}$.

#### Q095｜原题(2)｜PDF第35页

设列向量$\alpha =(1,2,1)^{T},\beta =(1,\frac{1}{2},0)^{T},\gamma =(0,0,8)^{T},A=\alpha \beta^{T},B=\beta^{T}\alpha$，且$2B^{2}A^{2}x=A^{4}x+B^{4}x+\gamma$,求$x$.

## 第九章向量

### 基础题 · 选择题

#### Q096｜原题(1)｜PDF第36页

若$\alpha_{1},\alpha_{2},\alpha_{3}$线性相关，$\alpha_{2},\alpha_{3},\alpha_{4}$线性无关，则$()$.

A.$\alpha_{1}$可由$\alpha_{2},\alpha_{3}$线性表示

B.$\alpha_{4}$可由$\alpha_{1},\alpha_{2},\alpha_{3}$线性表示

C.$\alpha_{4}$可由$\alpha_{1},\alpha_{3}$线性表示

D.$\alpha_{4}$可由$\alpha_{1},\alpha_{2}$线性表示

#### Q097｜原题(2)｜PDF第36页

向量组$\alpha_{1},\alpha_{2},\cdots,\alpha_{n}$线性无关等价于$()$.

A.存在一组不全为$0$的数,使其线性组合不为$0$

B.存在一个向量不能由其他向量线性表示

C.任何一个向量均不能由其他向量线性表示

D.其中任意两个向量线性无关

#### Q098｜原题(3)｜PDF第36页

设向量组$\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4}$线性无关，则下列向量组线性无关的是$()$.

A.$\alpha_{1}+\alpha_{2},\alpha_{2}+\alpha_{3},\alpha_{3}+\alpha_{4},\alpha_{4}+\alpha_{1}$

B.$\alpha_{1}+\alpha_{2},\alpha_{2}+\alpha_{3},\alpha_{3}+\alpha_{4},\alpha_{4}-\alpha_{1}$

C.$\alpha_{1}+\alpha_{2},\alpha_{2}-\alpha_{3},\alpha_{3}+\alpha_{4},\alpha_{4}-\alpha_{1}$

D.$\alpha_{1}-\alpha_{2},\alpha_{2}-\alpha_{3},\alpha_{3}-\alpha_{4},\alpha_{4}-\alpha_{1}$

#### Q099｜原题(4)｜PDF第37页

设向量组$(I)\beta_{1},\beta_{2},\cdots,\beta_{t}$，$(II)\alpha_{1},\alpha_{2},\cdots,\alpha_{s}$，则下列命题

①若向量组$(I)$可由$(I)$线性表示，且$s<t$，则必有$(I)$线性相关；

②若向量组$(II)$可由$(I)$线性表示，且$s<t$，则必有$(I)$线性相关；

③若向量组$(I)$可由$(II)$线性表示，且$(I)$线性无关，则必有$s\ge t$；

④若向量组$(II)$可由$(I)$线性表示，且$(I)$线性无关，则必有$s\ge t$，正确的是$()$.

A.①④

B.①③

C.②③

D.②④

#### Q100｜原题(5)｜PDF第37页

设$\alpha_{1}=(a_{1},a_{2},a_{3})^{T},\alpha_{2}=(b_{1},b_{2},b_{3})^{T},\alpha_{3}=(c_{1},c_{2},c_{3})^{T}$,其中$a_{i}^{2}+b_{i}^{2}\ne 0(i=1,2,3)$,则三条直线$a_{i}x +b_{i}y+c_{i}=0(i=1,2,3)$恰好仅交于一点的充分必要条件是$()$.

A.$r(\alpha_{1},\alpha_{2},\alpha_{3})=3$

B.$r(\alpha_{1},\alpha_{2},\alpha_{3})=1$

C.$r(\alpha_{1},\alpha_{2},\alpha_{3})=r(\alpha_{1},\alpha_{2})$

D.$r(\alpha_{1},\alpha_{2},\alpha_{3})=r(\alpha_{1},\alpha_{2})=2$

#### Q101｜原题(6)｜PDF第37页

设$\alpha_{1},\alpha_{2},\alpha_{3}$均为$3$维向量,则对任意常数$k$和$\mu$,向量组$\alpha_{1}+k\alpha_{3},\alpha_{2}+\mu \alpha_{3}$线性无关是向量组$\alpha_{1},\alpha_{2},\alpha_{3}$线性无关的$().)$

A.充分必要条件

B.充分非必要条件

C.必要非充分条件

D.既非充分又非必要条件

#### Q102｜原题(7)｜PDF第38页

设

$$
\alpha_{1}=\begin{pmatrix}1 \\
0 \\
0 \\
c_{1}\end{pmatrix},\alpha_{2}=\begin{pmatrix}1 \\
2 \\
0 \\
c_{2}\end{pmatrix},\alpha_{3}=\begin{pmatrix}-1 \\
2 \\
3 \\
c_{3}\end{pmatrix},\alpha_{4}=\begin{pmatrix}-2 \\
1 \\
5 \\
c_{4}\end{pmatrix},
$$

其中$c_{1},c_{2},c_{3},c_{4}$为任意常数,则$()$.

A.$\alpha_{1},\alpha_{2},\alpha_{3}$线性无关

B.$\alpha_{1},\alpha_{2},\alpha_{3}$线性相关

C.$\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4}$线性无关

D.$\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4}$线性相关

#### Q103｜原题(8)｜PDF第38页

设向量组$\alpha_{1},\alpha_{2},\alpha_{1}-2\alpha_{2}+\alpha_{3}$线性无关，则下列向量组线性无关的是$()$.

A.$\alpha_{1}+\alpha_{2},\alpha_{2}+\alpha_{3},\alpha_{3}-\alpha_{1}$

B.$\alpha_{1},\alpha_{2},\alpha_{3}$

C.$\alpha_{1}-\alpha_{2},\alpha_{2}-\alpha_{3},\alpha_{1}-2\alpha_{2}+\alpha_{3}$

D.$\alpha_{1}+\alpha_{2},\alpha_{2}+\alpha_{3},\alpha_{1}+2\alpha_{2}+\alpha_{3}$

### 基础题 · 填空题

#### Q104｜原题(1)｜PDF第38页

已知向量$\alpha_{1}=(1,2,3)^{T},\alpha_{2}=(2,-1,1)^{T},\alpha_{3}=(-2,k,4)^{T}$线性相关，则$k=\underline{\qquad\qquad}$.

#### Q105｜原题(2)｜PDF第39页

设向量组$(I)\alpha_{1}=(1,1,2)^{T},\alpha_{2}=(2,3,3)^{T};(II)\beta_{1}=(2,3,5)^{T},\beta_{2}=(-1,0,1)^{T}$，则既可由$(I)$线性表示，又可由$(II)$线性表示的非零列向量为$\underline{\qquad\qquad}$.

### 基础题 · 解答题

#### Q106｜原题(1)｜PDF第39页

设向量组$\alpha_{1}=(0,4,2)^{T},\alpha_{2}=(1,1,0)^{T},\alpha_{3}=(-2,4,3)^{T},\alpha_{4}=(-1,1,1)^{T}$,求$\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4}$的一个极大线性无关组,并将其余向量用极大线性无关组线性表示.

#### Q107｜原题(2)｜PDF第39页

设$\alpha_{1}=(1,0,2,3)^{T},\alpha_{2}=(1,1,3,5)^{T},\alpha_{3}=(1,-1,a,1)^{T},\beta =(1,b,4,7)^{T}$,问:当$a,b$为何值时,$\beta$不能由$\alpha_{1},\alpha_{2},\alpha_{3}$线性表示?$a,b$为何值时,$\beta$可由$\alpha_{1},\alpha_{2},\alpha_{3}$线性表示?写出表达式.

#### Q108｜原题(3)｜PDF第40页

设向量组$\alpha_{1}=(1,2,-3)^{T},\alpha_{2}=(3,0,1)^{T},\alpha_{3}=(9,6,-7)^{T}$与向量组$\beta_{1}=(0,1,-1)^{T},\beta_{2}=(k,2,1)^{T},\beta_{3} =(\mu,1,0)^{T}$有相同的秩,且$\beta_{3}$可由$\alpha_{1},\alpha_{2},\alpha_{3}$线性表示,求$k,\mu$的值.

#### Q109｜原题(4)｜PDF第40页

设向量组$(I):\alpha_{1}=(1,3,0,5)^{T},\alpha_{2}=(1,2,1,4)^{T},\alpha_{3}=(1,1,2,3)^{T};(II):\beta_{1}=(1,-3,6,-1)^{T},\beta_{2}= (a,0,b,2)^{T}$.若向量组$(I)$与$(II)$等价,求$a,b$的值.

#### Q110｜原题(5)｜PDF第40页

设向量组$(I)\alpha_{1},\alpha_{2},\alpha_{3},(II)\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4},(III)\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{5}$,且$r(I)=r(II)=3,r(III)=4$,证明:向量组$\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{5}-\alpha_{4}$的秩为$4$.

#### Q111｜原题(6)｜PDF第41页

设$A$是$3$阶方阵,$\alpha_{1},\alpha_{2}$为$A$的分别属于特征值$-2,1$的特征向量,且$A\alpha_{3}=\alpha_{2}+\alpha_{3}$,证明:$\alpha_{1},\alpha_{2},\alpha_{3}$线性无关.

#### Q112｜原题(7)｜PDF第41页

设矩阵$A_{5\times 4}$的秩为$2,\alpha_{1}=(1,1,2,3)^{T},\alpha_{2}=(-1,1,4,-1)^{T},\alpha_{3}=(5,-1,-8,9)^{T}$是方程组$Ax=0$的解向量，求$Ax=0$的基础解系，并将其正交单位化.

### 综合题 · 选择题

#### Q113｜原题(1)｜PDF第42页

设$A$是$m\times n$矩阵，$\alpha_{1}$，$\alpha_{2}$，$\cdots,\alpha_{t}$是$n$维列向量，向量组$(I)\alpha_{1},\alpha_{2},\cdots,\alpha_{t}$，$(II)A\alpha_{1},A\alpha_{2},\cdots$,$A\alpha_{t}$，则下列选项正确的是$()$.

A.若(I)线性无关，则$(II)$线性无关

B.若$(II)$线性相关，则$(I)$线性相关

C.若(II)线性无关，则$(I)$线性无关

D.$(I)$与$(II)$具有相同的线性相关性

#### Q114｜原题(2)｜PDF第42页

设三维列向量$\alpha_{1},\alpha_{2},\alpha_{3}$线性相关，$\alpha_{2},\alpha_{3},\alpha_{4}$线性无关，记$(\beta_{1},\beta_{2},\beta_{3})=(\alpha_{1},\alpha_{2},\alpha_{3})A_{3\times 3}$，$(\gamma_{1},\gamma_{2},\gamma_{3})=(\alpha_{2},\alpha_{3},\alpha_{4})B_{3\times 3}$,则$()$

A.存在矩阵$A_{3\times 3}$,使得$\beta_{1},\beta_{2},\beta_{3}$线性无关

B.不存在矩阵$A_{3\times 3}$,使得$\beta_{1},\beta_{2},\beta_{3}$线性相关

C.存在矩阵$B_{3\times 3}$,使得$\gamma_{1},\gamma_{2},\gamma_{3}$线性无关

D.不存在矩阵$B_{3\times 3}$,使得$\gamma_{1},\gamma_{2},\gamma_{3}$线性相关

#### Q115｜原题(3)｜PDF第42页

设向量$\alpha_{1},\alpha_{2},\alpha_{3}$满足$k_{1}\alpha_{1}+k_{2}\alpha_{2}+k_{3}\alpha_{3}=0,k_{1},k_{2},k_{3}$为常数，且$k_{1}k_{3}\ne 0$，则$()$.

A.$\alpha_{1}$与$\alpha_{3}$等价

B.$\alpha_{1},\alpha_{2}$与$\alpha_{1},\alpha_{3}$等价

C.$\alpha_{1},\alpha_{2}$与$\alpha_{2},\alpha_{3}$等价

D.$\alpha_{1},\alpha_{3}$与$\alpha_{2},\alpha_{3}$等价

#### Q116｜原题(4)｜PDF第43页

设$n$维向量组$(I)\alpha_{1},\alpha_{2},\cdots,\alpha_{k}(k<n)$线性无关，则$n$维向量组$(II)\beta_{1},\beta_{2},\cdots,\beta_{k}$也线性无关的充分必要条件是$()$.

A.$\beta_{1},\beta_{2},\cdots,\beta_{k}$可由$\alpha_{1},\alpha_{2},\cdots,\alpha_{k}$线性表示

B.$\alpha_{1},\alpha_{2},\cdots,\alpha_{k}$可由$\beta_{1},\beta_{2},\cdots,\beta_{k}$线性表示

C.向量组$(I)$与向量组$(II)$等价

D.矩阵$(\alpha_{1},\alpha_{2},\cdots,\alpha_{k})$与$(\beta_{1},\beta_{2},\cdots,\beta_{k})$等价

#### Q117｜原题(5)｜PDF第43页

设$4$维列向量$\alpha_{1},\alpha_{2},\alpha_{3}$线性无关，$\beta_{i}(i=1,2,3,4)$为非零列向量，且$\beta_{i}$与$\alpha_{1},\alpha_{2},\alpha_{3}$均正交，则$r(\beta_{1},\beta_{2},\beta_{3},\beta_{4})=()$.

A.$1$

B.$2$

C.$3$

D.$4$

#### Q118｜原题(6)｜PDF第43页

设$A,B$均是$m\times n$矩阵，则$Ax=0$与$Bx=0$同解的充分必要条件是$()$.

A.$A,B$的列向量组等价

B.$A,B$的行向量组等价

C.$A,B$是等价矩阵

D.$A^{T}x=0$与$B^{T}x=0$同解

#### Q119｜原题(7)｜PDF第44页

设$A,B$为$n$阶矩阵，$P,Q$为$n$阶可逆矩阵，下列选项错误的是$()$.

A.若$A=BQ$,则$B$的列向量组与$A$的列向量组等价

B.若$A=PB$,则$B$的行向量组与$A$的行向量组等价

C.若$A=PBQ$,则矩阵$A$与$B$等价

D.若$A=PBQ$,则$B$的行$($列$)$向量组与$A$的行$($列$)$向量组等价

#### Q120｜原题(8)｜PDF第44页

设$A,B$分别为$m\times n$与$n\times s$矩阵,且$r(A)=n$,则下列选项正确的是$()$.

A.$AB$的列向量组与$B$的列向量组等价

B.$AB$的行向量组与$B$的行向量组等价

C.$AB$的列向量组与$A$的列向量组等价

D.$AB$的行向量组与$A$的行向量组等价

### 综合题 · 填空题

#### Q121｜原文未编号｜PDF第44页

设向量组$\alpha_{1}=(1,k+2,3)^{T},\alpha_{2}=(2,-1,1)^{T},\alpha_{3}=(k-1,1,-1)^{T}$线性相关,但任意两个向量线性无关,则$k=\underline{\qquad\qquad}$.

### 综合题 · 解答题

#### Q122｜原题(1)｜PDF第45页

设

$$
A=\begin{pmatrix}1 & 0 & 0 & 0 \\
1 & 2 & 0 & 0 \\
2 & 4 & 3 & -3\end{pmatrix}=(\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4}),B=\begin{pmatrix}1 & 0 & 0 & 0 \\
0 & 2 & 0 & 0 \\
0 & 0 & 3 & 0\end{pmatrix}.
$$

(I)求向量组$\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4}$的一个极大线性无关组;

(II)求可逆矩阵$P_{3\times 3},Q_{4\times 4}$,使得$PAQ=B$.

#### Q123｜原题(2)｜PDF第45页

设向量组$\alpha_{1}=(1,0,1)^{T},\alpha_{2}=(0,1,1)^{T},\alpha_{3}=(1,3,5)^{T}$不能由向量组$\beta_{1}=(1,1,1)^{T},\beta_{2}=(1,2,3)^{T},\beta_{3} =(3,4,a)^{T}$线性表示,求$a$的值,并将$\beta_{1},\beta_{2},\beta_{3}$用$\alpha_{1},\alpha_{2},\alpha_{3}$线性表示.

#### Q124｜原题(3)｜PDF第46页

设$A=(\alpha_{1},\alpha_{2},\alpha_{3})$,其中$\alpha_{1}=(1,0,1)^{T},\alpha_{2}=(1,1,2)^{T},\alpha_{3}=(1,2,a)^{T},B=(\beta_{1},\beta_{2})$,其中$\beta_{1}= (-1,2,1)^{T},\beta_{2}=(1,0,b)^{T}$.问:

(I)当$a,b$为何值时,$\beta_{1},\beta_{2}$不能同时由$\alpha_{1},\alpha_{2},\alpha_{3}$线性表示?

(II)当$a,b$为何值时,$\beta_{1},\beta_{2}$可同时由$\alpha_{1},\alpha_{2},\alpha_{3}$线性表示?并求表达式.

#### Q125｜原题(4)｜PDF第46页

设$n$维向量组$\alpha_{1},\alpha_{2},\cdots,\alpha_{k}(k<n)$线性无关,且$\alpha_{k+1}=\lambda_{1}\alpha_{1}+\lambda_{2}\alpha_{2}+\cdots +\lambda_{k}\alpha_{k},\lambda_{i}\ne 0,i=1,2,\cdots,k$,证明:$\alpha_{1},\alpha_{2},\cdots,\alpha_{k},\alpha_{k+1}$中任何$k$个向量都线性无关.

#### Q126｜原题(5)｜PDF第47页

设$A$是$3$阶方阵,$A$的特征值为$\lambda_{1}=1,\lambda_{2}=2,\lambda_{3}=3$,对应的特征向量分别为$\alpha_{1}=(1,1,1)^{T},\alpha_{2}= (1,2,4)^{T},\alpha_{3}=(1,3,9)^{T}$,另一向量$\beta =(1,1,3)^{T}$.

(I)将$\beta$用$\alpha_{1},\alpha_{2},\alpha_{3}$线性表示;

(II)求$A^{n}\beta (n$为正整数$)$.

#### Q127｜原题(6)｜PDF第47页

设$A$是$m\times n$矩阵,$\alpha_{1}$与$\alpha_{2}$是非齐次线性方程组$Ax=b$的两个不同解.

(I)证明:$\alpha_{1},\alpha_{1}-\alpha_{2}$线性无关;

(II)若$\beta$是$Ax=0$的一个非零解向量,$r(A)=n-1$,证明:$\beta,\alpha_{1},\alpha_{2}$线性相关.

#### Q128｜原题(7)｜PDF第48页

设$\alpha_{1},\alpha_{2},\alpha_{3}$是方程组

$$
\begin{cases}x_{1}-3x_{2}+x_{3}=2, \\
2x_{1}+x_{2}-x_{3}=-1, \\
7x_{1}-2x_{3}=-1\end{cases}
$$

的解向量,证明:$\alpha_{1}-\alpha_{2},\alpha_{1}-\alpha_{3}$线性相关.

#### Q129｜原题(8)｜PDF第48页

设$A$是$3$阶矩阵,$\alpha_{i}(i=1,2,3)$是$3$维非零列向量,且$A\alpha_{i}=i\alpha_{i}(i=1,2,3),\alpha =\alpha_{1}+\alpha_{2}+\alpha_{3}$,证明:$\alpha$,$A\alpha,A^{2}\alpha$线性无关.

#### Q130｜原题(9)｜PDF第49页

设

$$
A=(\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4}),\alpha_{1}=\begin{pmatrix}1 \\
0 \\
0 \\
0\end{pmatrix},\alpha_{2}=\begin{pmatrix}1 \\
1 \\
1 \\
1\end{pmatrix},\alpha_{3}=\begin{pmatrix}0 \\
1 \\
1 \\
1\end{pmatrix},\alpha_{4}=\begin{pmatrix}0 \\
-1 \\
-1 \\
-1\end{pmatrix}.
$$

(I)证明:$\alpha_{1},\alpha_{2}$是$\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4}$的极大线性无关组.

(II)记$G=(\alpha_{1},\alpha_{2})$,求矩阵$H$,使得$A=GH$,并求$A^{8}$.

#### Q131｜原题(10)｜PDF第50页

设$A=(\alpha_{1},\alpha_{2},\alpha_{3})$为$3$阶矩阵，交换$A$的第$1,2$行，再交换$A$的第$2,3$列得$B$，即

$$
B=\begin{pmatrix}0 & -1 & 1 \\
1 & 1 & 1 \\
1 & 1 & -1\end{pmatrix}
$$

(I)求$A$;

(II)记$\beta_{1}=\alpha_{1},\beta_{2}=\alpha_{2}-k\beta_{1},\beta_{3}=\alpha_{3}-l_{1}\beta_{1}-l_{2}\beta_{2}$,若$\beta_{1},\beta_{2},\beta_{3}$两两正交,求$k,l_{1},l_{2}$;

(III)求正交矩阵$Q$及上三角矩阵$T$,使得$A=QT$.

### 拓展题 · 解答题

#### Q132｜原文未编号｜PDF第51页

设$A=(\alpha_{1},\alpha_{2},\alpha_{3}),\alpha_{1}=(0,3,c)^{T},\alpha_{2}=(a,2,1)^{T},\alpha_{3}=(b,1,0)^{T},B=(\beta_{1},\beta_{2},\beta_{3}),\beta_{1}=(1,2,-3)^{T},\beta_{2}= (3,0,1)^{T},\beta_{3}=(9,6,-7)^{T}$,且$r(A)=r(B),\alpha_{2},\alpha_{3}$可由$\beta_{1},\beta_{2},\beta_{3}$线性表示.

(I)求$a,b,c$的值;

(II)若$BX=A$,求矩阵$X$.

## 第十章线性方程组

### 基础题 · 选择题

#### Q133｜原题(1)｜PDF第52页

已知$\eta_{1},\eta_{2}$是非齐次线性方程组$Ax=b$的两个不同解，$\xi_{1},\xi_{2}$是对应齐次线性方程组$Ax=0$的基础解系，$k_{1}$，$k_{2}$为任意常数，则$Ax=b$的通解为$()$.

A.$k_{1}\xi_{1}+k_{2}(\xi_{1}+\xi_{2})+\frac{\eta_{1}-\eta_{2}}{2}$

B.$k_{1}\xi_{1}+k_{2}(\xi_{1}-\xi_{2})+\frac{\eta_{1}+\eta_{2}}{2}$

C.$k_{1}\xi_{1}+k_{2}(\eta_{1}+\eta_{2})+\frac{\eta_{1}-\eta_{2}}{2}$

D.$k_{1}\xi_{1}+k_{2}(\eta_{1}-\eta_{2})+\frac{\eta_{1}+\eta_{2}}{2}$

#### Q134｜原题(2)｜PDF第52页

设$A$是$n(n\ge 3)$阶矩阵，$A^{*}$是$A$的伴随矩阵，线性方程组$AX=0$有两个线性无关的解，则$()$.

A.$AX=0$与$A^{*}X=0$同解

B.$A^{*}X=0$的解均是$AX=0$的解

C.$AX=0$的解均是$A^{*}X=0$的解

D.$AX=0$与$A^{*}X=0$没有非零公共解

#### Q135｜原题(3)｜PDF第52页

设$A$是$n$阶矩阵，对方程组$(I)Ax=0$和$(II)A^{T}Ax=0$，必有$()$.

A.(II)的解是$(I)$的解，$(I)$的解也是$(II)$的解

B.(II)的解是$(I)$的解，但$(I)$的解不是$(II)$的解

C.(I)的解不是$(II)$的解，$(II)$的解也不是$(I)$的解

D.(I)的解是$(II)$的解，但$(II)$的解不是$(I)$的解

#### Q136｜原题(4)｜PDF第53页

设$A$是$n$阶矩阵，若对任意的$n$维列向量$\alpha$，有$A^{*}\alpha =0$，则$Ax=0$的基础解系所含解向量的个数$k$满足$()$.

A.$k=0$

B.$k=1$

C.$k>1$

D.$k=n$

#### Q137｜原题(5)｜PDF第53页

设方程组

$$
\begin{cases}\lambda x_{1}+x_{2}+\lambda^{2}x_{3}=0, \\
x_{1}+\lambda x_{2}+x_{3}=0, \\
x_{1}+x_{2}+\lambda x_{3}=0\end{cases}
$$

的系数矩阵为$A$,若存在$3$阶矩阵$B\ne O$,使得$AB=O$,则必有$()$.

A.$\lambda =-2$且$\left|B\right|=0$

B.$\lambda =-2$且$\left|B\right|\ne 0$

C.$\lambda =1$且$\left|B\right|=0$

D.$\lambda =1$且$\left|B\right|\ne 0$

#### Q138｜原题(6)｜PDF第53页

设

$$
B=\begin{pmatrix}1 & 2 & -1 \\
2 & a & 4 \\
3 & 5 & a\end{pmatrix}(a>0),A
$$

是$3$阶非零矩阵,且$BA^{T}=O,k_{1},k_{2}$为任意常数,则方程组$AX=0$的通解为$()$.

A.

$$
k_{1}\begin{pmatrix}1 \\
0 \\
0\end{pmatrix}
$$

B.

$$
k_{1}\begin{pmatrix}1 \\
2 \\
-1\end{pmatrix}+k_{2}\begin{pmatrix}0 \\
-1 \\
6\end{pmatrix}
$$

C.

$$
k_{1}\begin{pmatrix}1 \\
2 \\
3\end{pmatrix}
$$

D.

$$
k_{1}\begin{pmatrix}1 \\
2 \\
3\end{pmatrix}+k_{2}\begin{pmatrix}0 \\
1 \\
1\end{pmatrix}.
$$

#### Q139｜原题(7)｜PDF第54页

设方程组

$$
\begin{cases}2x_{1}-3x_{2}+x_{3}=b_{1}, \\
x_{1}-2x_{2}+x_{3}=b_{2}, \\
2x_{1}+kx_{2}+3x_{3}=b_{3}\end{cases}
$$

有解,则$()$.

A.当$k\ne -5$时,$(b_{1},b_{2},b_{3})^{T}$为任意非零列向量

B.当$k=-5$时,$(b_{1},b_{2},b_{3})^{T}$为任意列向量

C.当$k=-5$时,$b_{1}+b_{3}=4b_{2}$

D.当$k\ne -5$时,$b_{1}+b_{3}=4b_{2}$

#### Q140｜原题(8)｜PDF第54页

设矩阵$A_{m\times n},B_{n\times m}$，则$()$.

A.当$m>n$时，$AB$必可逆

B.当$m>n$时,必有$\left|AB\right|=0$

C.当$n>m$时,必有$r(AB)<m$

D.当$n>m$时,$ABx=0$必有唯一解

#### Q141｜原题(9)｜PDF第54页

设矩阵$A_{m\times n},B_{n\times m}$满足$AB=E$,其中$E$是单位矩阵,$\alpha$与$\beta$为非零列向量,则下列命题正确的是$()$.

A.方程组$AX=\alpha$有唯一解,方程组$BX=\beta$有唯一解

B.方程组$AX=\alpha$有无穷多解,方程组$BX=\beta$有无穷多解

C.方程组$AX=0$仅有零解,方程组$BX=\beta$有解

D.方程组$AX=\alpha$有解,方程组$BX=0$仅有零解

#### Q142｜原题(10)｜PDF第55页

设$A^{T}=(\alpha_{1},\alpha_{2},\cdots,\alpha_{n-1})$是$n\times (n-1)$矩阵,$r(A^{T})=n-1,\beta_{1},\beta_{2}$是与$\alpha_{1},\alpha_{2},\cdots,\alpha_{n-1}$均正交的$n$维列向量，$\beta_{1}\ne \beta_{2}$，$k$是任意常数，则方程组$AX=0$的通解为$()$.

A.$k\beta_{1}$

B.$k\beta_{2}$

C.$k(\beta_{1}+\beta_{2})$

D.$k(\beta_{1}-\beta_{2})$

#### Q143｜原题(11)｜PDF第55页

设$A$是$m\times s$矩阵，$B$是$s\times n$矩阵，则方程组$ABX=0$与$BX=0$同解的充分必要条件是$()$.

A.$r(A)=s$

B.$r(AB)=r(B)$

C.$r(A)=r(B)$

D.$r(A)=m$

#### Q144｜原题(12)｜PDF第55页

设$A$为$3$阶矩阵,$\alpha_{1}=(1,2,-2)^{T},\alpha_{2}=(2,1,-1)^{T},\alpha_{3}=(1,1,a)^{T}(a\ne -1)$是非齐次线性方程组$AX =b$的三个解,$A^{*}$是$A$的伴随矩阵,则$()$.

A.$AX=0$与$A^{*}X=0$同解

B.$A^{*}X=0$的解均是$AX=0$的解,但二者不同解

C.$AX=0$的解均是$A^{*}X=0$的解,但二者不同解

D.$AX=0$与$A^{*}X=0$没有非零公共解

#### Q145｜原题(13)｜PDF第56页

设有矩阵$A_{n\times s},B_{s\times n}$，且$r(A)=s,r(B)=n,E_{n\times n}$为单位矩阵，则下列齐次线性方程组有非零解的是$()$.

A.

$$
\begin{pmatrix}AB & O \\
E & A\end{pmatrix}X=0
$$

B.

$$
\begin{pmatrix}AB & O \\
E & B\end{pmatrix}X=0
$$

C.

$$
\begin{pmatrix}A & E \\
O & AB\end{pmatrix}X=0
$$

D.

$$
\begin{pmatrix}A & AB \\
E & B\end{pmatrix}X=0
$$

### 基础题 · 填空题

#### Q146｜原题(1)｜PDF第56页

设方程组

$$
\begin{cases}x_{1}+2x_{2}+x_{3}=3, \\
2x_{1}+(k+4)x_{2}-5x_{3}=6, \\
-x_{1}-2x_{2}+kx_{3}=-3,\end{cases}
$$

，则$k=\underline{\qquad\qquad}$.

#### Q147｜原题(2)｜PDF第56页

设

$$
A=\begin{pmatrix}1 & 2 & 1 \\
2 & 3 & a+2 \\
1 & a & -2\end{pmatrix},\beta_{1}=(1,3,4)^{T},\beta_{2}=(0,1,2)^{T},
$$

若方程组$AX=\beta_{1}$有解,且$AX=\beta_{2}$无解,则$a =\underline{\qquad\qquad}$.

#### Q148｜原题(3)｜PDF第57页

设$4$阶方阵$A=(\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4})$，其中$\alpha_{1},\alpha_{2}$线性无关，若$\beta =\alpha_{1}+\alpha_{2}-2\alpha_{3},\beta =\alpha_{1}+2\alpha_{2}+\alpha_{3}-\alpha_{4}$,$\beta =2\alpha_{1}+3\alpha_{2}+2\alpha_{3}+\alpha_{4}$，则方程组$AX=\beta$的通解为$\underline{\qquad\qquad}$.

### 基础题 · 解答题

#### Q149｜原题(1)｜PDF第57页

求方程组

$$
\begin{cases}2x_{1}-x_{2}+4x_{3}-3x_{4}=-4, \\
x_{1}+x_{3}-x_{4}=-3, \\
3x_{1}+x_{2}+x_{3}=1, \\
7x_{1}+7x_{3}-3x_{4}=3\end{cases}
$$

的通解.

#### Q150｜原题(2)｜PDF第57页

设方程组

$$
\begin{cases}2x_{1}+\lambda x_{2}-x_{3}=1, \\
\lambda x_{1}-x_{2}+x_{3}=2, \\
4x_{1}+5x_{2}-5x_{3}=-1,\end{cases}
$$

问:当$\lambda$为何值时,方程组无解、有唯一解、有无穷多解？当有无穷多解时,求其通解.

#### Q151｜原题(3)｜PDF第58页

设有方程组①

$$
\begin{cases}x_{1}+x_{2}=0, \\
x_{2}-x_{4}=0\end{cases}
$$

与方程组②

$$
\begin{cases}x_{1}-x_{2}+x_{3}=0, \\
x_{2}-x_{3}+x_{4}=0.\end{cases}
$$

(I)求方程组①与②的基础解系；

(II)求方程组①与②的非零公共解.

#### Q152｜原题(4)｜PDF第58页

设有方程组

$$
(I)\begin{cases}x_{1}+x_{2}=0, \\
x_{2}-x_{4}=0,\end{cases}(II)Ax=0
$$

，其中$(II)$的基础解系为$\alpha_{1}=(-1,2,2,1)^{T}$,$\alpha_{2}=(0,-1,-1,0)^{T}$,求方程组$(I)$与$(II)$的非零公共解.

#### Q153｜原题(5)｜PDF第59页

设有方程组:

①

$$
\begin{cases}x_{1}-x_{4}=-2, \\
x_{2}-x_{4}=-4, \\
-4x_{2}-x_{3}+6x_{4}=21,\end{cases}
$$

②

$$
\begin{cases}x_{1}+ax_{2}-x_{3}-x_{4}=-1 \\
bx_{2}-x_{3}-2x_{4}=-11, \\
x_{3}-2x_{4}=-c+1.\end{cases}
$$

(I)求方程组①的通解;

(II)当$a,b,c$为何值时,方程组①与②同解?

#### Q154｜原题(6)｜PDF第59页

设$n$阶矩阵$A$满足$\left|A\right|=0,A_{ij}$为$\left|A\right|$的元素$a_{ij}$对应的代数余子式，且$A_{11}\ne 0$，求方程组$A^{*}x=0$的基础解系和通解.

#### Q155｜原题(7)｜PDF第60页

已知$4\times 3$矩阵$A=(\alpha_{1},\alpha_{2},\alpha_{3})$,非齐次线性方程组$Ax=\beta$的通解为$(1,2,-1)^{T}+k(1,-2,3)^{T},k$为任意常数,令$B=(\alpha_{1},\alpha_{2},\alpha_{3},\beta +\alpha_{3})$,求方程组$By=\alpha_{1}-\alpha_{2}$的通解.

#### Q156｜原题(8)｜PDF第60页

设$A$是$5\times 4$矩阵,$r(A)=2$,已知$\alpha_{1},\alpha_{2},\alpha_{3}$是非齐次线性方程组$Ax=b$的三个解向量,且$\alpha_{1}+\alpha_{2} =(4,6,-8,4)^{T},\alpha_{3}=(1,2,-1,1)^{T}$,又$(0,1,-3,0)^{T}$是$Ax=0$的解,求$Ax=b$的通解.

#### Q157｜原题(9)｜PDF第61页

设$A,B$均为$3$阶矩阵,

$$
A=\begin{pmatrix}1 & 0 & 1 \\
2 & a & 0 \\
1 & 1 & -1\end{pmatrix},r(B)=2,r(AB)=1.
$$

求$a$的值,并求方程组$Ax=0$的通解.

### 综合题 · 选择题

#### Q158｜原题(1)｜PDF第61页

设$A$是$m\times n$矩阵,$m<n$,且$A$的行向量组线性无关,$b_{1},b_{2}$分别为$m$维、$n$维非零列向量,则下列选项错误的是$()$.

A.$A^{T}x=0$只有零解

B.$A^{T}Ax=0$必有非零解

C.$Ax=b_{1}$必有无穷多个解

D.$A^{T}x=b_{2}$必有唯一解

#### Q159｜原题(2)｜PDF第62页

设$A$是$m\times n$矩阵，则非齐次线性方程组$Ax=b$有无穷多解的充分必要条件是$()$.

A.$r(A\vdots b)<n$

B.$Ax=0$有非零解

C.$Ax=b$有两个不同解

D.$A$的列向量组线性相关

#### Q160｜原题(3)｜PDF第62页

设$A^{T}=(\alpha_{1},\alpha_{2},\cdots,\alpha_{n-1})$是$n\times (n-1)$矩阵,$r(A^{T})=n-1,\beta_{1},\beta_{2}$是与$\alpha_{1},\alpha_{2},\cdots,\alpha_{n-1}$都正交的两个不同的$n$维列向量，$k$是任意常数，则方程组$Ax=0$的通解为$()$.

A.$k(\beta_{1}-\beta_{2})$

B.$k(\beta_{1}+\beta_{2})$

C.$k\beta_{1}$

D.$k\beta_{2}$

#### Q161｜原题(4)｜PDF第62页

设向量组$\alpha_{1}=(1,1,a)^{T},\alpha_{2}=(1,-2,b)^{T},\alpha_{3}=(-2,1,c)^{T}$的秩为$a$,若$\beta =(1,2,0)^{T}$可由$\alpha_{1},\alpha_{2},\alpha_{3}$线性表示，且表示法不唯一，则$()$.

A.$a=2,b=8,c=-10$

B.$a=2,b=8,c=10$

C.$a=1,b=-8,c=10$

D.$a=1,b=-8,c=-10$

#### Q162｜原题(5)｜PDF第63页

设$n$维实列向量$\alpha$满足$\alpha^{T}\alpha =2,A,B$均为$n$阶矩阵,$E$为$n$阶单位矩阵,且$A(E-2\alpha \alpha^{T})=B$.则$()$.

A.方程组$BX=0$与方程组$(E-2\alpha \alpha^{T})X=0$同解

B.方程组$B^{T}X=0$与方程组$(E-2\alpha \alpha^{T})X=0$同解

C.方程组$BX=0$与方程组$AX=0$同解

D.方程组$B^{T}X=0$与方程组$A^{T}X=0$同解

#### Q163｜原题(6)｜PDF第63页

设$A$为$n$阶矩阵，下列命题正确的是$()$.

①$A^{n}X=0$与$A^{n+1}X=0$同解；②$A^{n+1}X=0$的解不一定是$A^{n}X=0$的解;

③$A^{n}X=0$与$(A^{T})^{n}A^{n}X=0$同解；④$(A^{T})^{n}A^{n}X=0$的解不一定是$A^{n}X=0$的解.

A.①②

B.①③

C.②④

D.③④

#### Q164｜原题(7)｜PDF第63页

设$n$阶非零实矩阵$A$满足$A^{T}+A=O$，$X$为$n$维实列向量，则下列选项正确的是$()$.

A.方程组$AX=X$有无穷多解

B.方程组$AX=-X$有无穷多解

C.方程组$AX=X$只有零解

D.方程组$AX=-X$无解

#### Q165｜原题(8)｜PDF第64页

设$A$是$n$阶实对称矩阵,$B$是$n$阶实矩阵,若对任意$n$维非零列向量$\alpha$,都有$\alpha^{T}(AB+B^{T}A)\alpha >0$,则下列选项正确的是$()$.

A.方程组$ABX=\alpha$有无穷多解

B.方程组$ABX=\alpha$无解

C.方程组$AX=\alpha$有唯一解

D.方程组$AX=\alpha$无解

#### Q166｜原题(9)｜PDF第64页

设$A,B$均为$n$阶矩阵,$\alpha,\beta$均为$n$维列向量.若$\alpha$可由$A$的列向量线性表示，$(\alpha^{T},\beta^{T})$不能由$(A^{T}$，$B^{T})$的行向量线性表示，则下列结论正确的是$()$.

A.$r(B,\beta)=r(B)$

B.$r(B,\beta)=r(B)+1$

C.

$$
r\begin{pmatrix}A^{T} & B^{T} \\
\alpha^{T} & \beta^{T}\end{pmatrix}=r(A^{T},B^{T})+1
$$

D.

$$
[(A,\alpha),B^{T}]=r[(A^{T},B^{T})\begin{pmatrix}A \\
B\end{pmatrix}]
$$

#### Q167｜原题(10)｜PDF第64页

设$f(x)$二阶可导,$f^{\prime\prime}(x)\ne 0,(a,f(a)),(b,f(b)),(c,f(c))$为曲线$y=f(x)$上三个不同的点,则以下方程组$()$.

$$
\begin{cases}x_{1}+ax_{2}+f(a)x_{3}=f(b), \\
x_{1}+bx_{2}+f(b)x_{3}=f(c), \\
x_{1}+cx_{2}+f(c)x_{3}=f(a)\end{cases}
$$

A.有唯一解

B.有无穷多解

C.无解

D.无法确定是否有解

#### Q168｜原题(11)｜PDF第65页

设$A$是$m\times n$矩阵，则非齐次线性方程组$AX=b$有解的充分必要条件是$()$.

A.$r(A)=r(A^{T})=m$

B.$r(A)=r(A^{T})=n$

C.

$$
r(A^{T})=r\begin{pmatrix}A^{T} \\
b^{T}\end{pmatrix}=m
$$

D.$A^{T}X=0$与

$$
\begin{pmatrix}A^{T} \\
b^{T}\end{pmatrix}X=0
$$

同解

### 综合题 · 填空题

#### Q169｜原题(1)｜PDF第65页

设$\alpha_{1},\alpha_{2},\alpha_{3},\beta$均为三维列向量，$A=(\beta -\alpha_{1}-2\alpha_{2}-3\alpha_{3},\alpha_{1},\alpha_{2},\alpha_{3})$，则方程组$Ax=\beta$的一个特解为$\underline{\qquad\qquad}$.

#### Q170｜原题(2)｜PDF第65页

设$A=(a_{ij})_{3\times 3}$为实矩阵，且$A_{ij}=a_{ij}(i,j=1,2,3)$，其中$A_{ij}$为$a_{ij}$的代数余子式，$a_{33}=1$，$\left|A\right|= 1$,则方程组

$$
A\begin{pmatrix}x_{1} \\
x_{2} \\
x_{3}\end{pmatrix}=\begin{pmatrix}0 \\
0 \\
1\end{pmatrix}
$$

的解为$\underline{\qquad\qquad}$.

#### Q171｜原题(3)｜PDF第66页

设$A$是$2$阶矩阵,线性方程组

$$
AX=\begin{pmatrix}3 \\
2\end{pmatrix}
$$

的通解为$k(-2,1)^{T}+(3,-4)^{T}$.若$\beta =(5,-10)^{T}$，则$\beta^{T}A\beta =\underline{\qquad\qquad}$.

#### Q172｜原题(4)｜PDF第66页

设$A$为$3$阶矩阵，$\alpha$为$3$维非零列向量，向量组$\alpha,A\alpha,A^{2}\alpha$线性无关，且$A^{3}\alpha +2A^{2}\alpha -3A\alpha =0$，则$\operatorname{tr}(A)=\underline{\qquad\qquad}$.

### 综合题 · 解答题

#### Q173｜原题(1)｜PDF第66页

设$A$是$m\times n$矩阵，$r(A)=n-2$，非齐次线性方程组$Ax=b$的$3$个解向量$\alpha_{1},\alpha_{2},\alpha_{3}$满足$\alpha_{1}+\alpha_{2} =(1,2,3,4)^{T},\alpha_{2}+2\alpha_{3}=(-2,1,5,3)^{T},2\alpha_{3}+3\alpha_{1}=(11,5,-6,7)^{T}$,求方程组$Ax=b$的通解.

#### Q174｜原题(2)｜PDF第67页

设$A=(\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4})$是$4$阶矩阵,非齐次线性方程组$Ax=\beta$的通解为$(1,2,2,1)^{T}+k(1,-2,4,0)^{T}$,$k$为任意常数,记$B=(\alpha_{3},\alpha_{2},\alpha_{1},\beta -\alpha_{4})$.

(I)证明:$r(B)=2$;

(II)求方程组$Bx=\alpha_{1}-\alpha_{2}$的通解.

#### Q175｜原题(3)｜PDF第67页

设$A$为$3\times 4$矩阵,$r(A)=1$,若向量组$\alpha_{1}=(1,2,0,2)^{T},\alpha_{2}=(-1,-1,1,a)^{T},\alpha_{3}=(1,-1,a,5)^{T},\alpha_{4}= (2,a,-3,-5)^{T}$与方程组$Ax=0$的基础解系等价,求$Ax=0$的通解.

#### Q176｜原题(4)｜PDF第68页

设$A$是$3$阶方阵,$A=(a_{ij})_{3\times 3}$，且$a_{ij}=A_{ij},i,j=1,2,3$，其中$A_{ij}$为$a_{ij}$的代数余子式，$a_{33}\ne 0$，$b =(a_{13},a_{23},a_{33})^{T}$,求非齐次线性方程组$Ax=b$的解.

#### Q177｜原题(5)｜PDF第68页

设

$$
A=\frac{1}{2}\begin{pmatrix}1 & 2a & 1 \\
-1 & \sqrt{2} & 2b \\
\sqrt{2} & 2c & -\sqrt{2}\end{pmatrix}.
$$

(I)若$A$是正交矩阵,求$a,b,c$的值;

(II)当$A$为正交矩阵时,求方程组

$$
Ax=\begin{pmatrix}1 \\
1 \\
1\end{pmatrix}
$$

的解.

#### Q178｜原题(6)｜PDF第69页

设$A$是$3$阶矩阵,向量$\beta =(3,3,3)^{T}$,非齐次线性方程组$Ax=\beta$的通解为$k_{1}(1,2,-2)^{T}+k_{2}(2,1,2)^{T} +(1,1,1)^{T},k_{1},k_{2}$为任意常数.

(I)证明:任意$3$维列向量$\alpha$可由$A$的三个特征向量线性表示;

(II)若$\alpha =(1,2,-1)^{T}$,求$A\alpha$.

#### Q179｜原题(7)｜PDF第69页

设$4$维列向量组$\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4}$,且$\alpha_{1},\alpha_{2},\alpha_{3}$线性无关,$\alpha_{4}=\alpha_{1}+\alpha_{2}+2\alpha_{3}$,$B=(\alpha_{1}-\alpha_{2},\alpha_{2}+\alpha_{3},-\alpha_{1}+k\alpha_{2}+\alpha_{3})$,方程组$Bx=\alpha_{4}$有无穷多解.

(I)求$k$的值;

(II)求方程组的通解.

#### Q180｜原题(8)｜PDF第70页

设

$$
A=\begin{pmatrix}a-3 & -1 & 2 \\
-1 & a-3 & 2 \\
-1 & -1 & a\end{pmatrix},
$$

且$r(E-A)=1$.

(I)求$a$的值;

(II)若非零列向量$\alpha,\beta$满足$(A-E)\alpha =\beta,(A^{2}-E)\alpha =2\beta$,求所有满足题意的$\alpha,\beta$.

#### Q181｜原题(9)｜PDF第70页

设

$$
A=\begin{pmatrix}-1 & 0 & 1 \\
-1 & 1 & a\end{pmatrix},B=\begin{pmatrix}-1 & 1 \\
-1 & 1 \\
b & 2\end{pmatrix}.
$$

(I)若方程组$AX=0$的解均是$B^{T}X=0$的解,但这两个方程组不同解,求$a,b$的值;

(II)若方程组$AX=0$与$B^{T}X=0$有非零公共解,求$a,b$的值,并求全部非零公共解.

#### Q182｜原题(10)｜PDF第71页

设

$$
A=\begin{pmatrix}2 & 0 & 0 & 2 \\
1 & 1 & 0 & 3 \\
0 & 1 & 3 & 5\end{pmatrix},B=\begin{pmatrix}1 & 0 & 1 & 2 \\
0 & 2 & 0 & 4 \\
0 & -1 & a-1 & a-3\end{pmatrix},\alpha =\begin{pmatrix}2 \\
2 \\
1\end{pmatrix},\beta =\begin{pmatrix}1 \\
2 \\
-1\end{pmatrix}.
$$

(I)证明:方程组$AX=\alpha$的解均是方程组$BX=\beta$的解;

(II)若方程组$AX=\alpha$与方程组$BX=\beta$不同解,求$a$的值.

#### Q183｜原题(11)｜PDF第71页

设矩阵

$$
A=\begin{pmatrix}a & 1 & 1 \\
0 & a-1 & 0 \\
1 & 1 & a\end{pmatrix}
$$

不可逆,

$$
\beta =\begin{pmatrix}b \\
1 \\
1\end{pmatrix}.
$$

已知方程组$A^{T}X=0$的解均是$\beta^{T}X=0$的解.

(I)求$a,b$的值;

(II)求可逆矩阵$P$,使得$P^{-1}AP=\Lambda$.

### 拓展题 · 解答题

#### Q184｜原题(1)｜PDF第72页

设

$$
A=\begin{pmatrix}1 & -2 & 3 \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}\end{pmatrix}
$$

有特征向量$\alpha_{1}=(1,2,1)^{T},\alpha_{2}=(-1,1,1)^{T},\alpha_{3}=(-1,3,2)^{T}$,求方程组

$$
\begin{cases}x_{1}-2x_{2}+3x_{3}=-1, \\
a_{21}x_{1}+a_{22}x_{2}+a_{23}x_{3}=3, \\
a_{31}x_{1}+a_{32}x_{2}+a_{33}x_{3}=2\end{cases}
$$

的通解.

#### Q185｜原题(2)｜PDF第72页

设$A$是$m\times n$矩阵,$b$为$m$维列向量,证明:线性方程组$A^{T}Ax=A^{T}b$必有解.

#### Q186｜原题(3)｜PDF第73页

(I)设实矩阵$A_{m\times n}$的秩为$m$，证明:存在实矩阵$B_{n\times m}$且$r(B)=m$，使得$AB=E$，其中$E$为$m$阶单位矩阵.

(II)若

$$
A=\begin{pmatrix}-1 & 0 & 1 & -1 \\
1 & -1 & -1 & -1 \\
0 & 1 & 0 & 1\end{pmatrix},
$$

求满足$AB=E$且$r(B)=3$的所有实矩阵$B_{4\times 3}$.

## 第十一章相似矩阵

### 基础题 · 选择题

#### Q187｜原题(1)｜PDF第74页

设$\lambda =2$是矩阵$A$的一个特征值，且$\left|A\right|\ne 0$，则$(\frac{1}{3}A^{2})^{-1}$有一个特征值为$()$.

A.$\frac{4}{3}$

B.$\frac{3}{4}$

C.$\frac{1}{2}$

D.$\frac{1}{4}$

#### Q188｜原题(2)｜PDF第74页

设

$$
C=\operatorname{diag}(1,2,2),A=\begin{pmatrix}2 & 0 & 0 \\
0 & 2 & 1 \\
0 & 0 & 1\end{pmatrix},B=\begin{pmatrix}2 & 1 & 0 \\
0 & 2 & 0 \\
0 & 0 & 1\end{pmatrix}
$$

，则$()$.

A.$A$与$C$相似,$B$与$C$不相似

B.$A$与$C$相似,$B$与$C$相似

C.$A$与$C$不相似,$B$与$C$相似

D.$A$与$C$不相似,$B$与$C$不相似

#### Q189｜原题(3)｜PDF第74页

下列矩阵中，不能相似于对角矩阵的是$()$.

A.

$$
A=\begin{pmatrix}1 & -1 & 3 \\
-1 & 2 & 0 \\
3 & 0 & 6\end{pmatrix}
$$

B.

$$
B=\begin{pmatrix}1 & 0 & 0 \\
0 & 2 & 0 \\
5 & 0 & 3\end{pmatrix}
$$

C.

$$
C=\begin{pmatrix}0 & 0 & 0 \\
0 & 0 & 0 \\
1 & 2 & 3\end{pmatrix}
$$

D.

$$
D=\begin{pmatrix}1 & 2 & 0 \\
0 & 0 & 3 \\
0 & 0 & 0\end{pmatrix}
$$

#### Q190｜原题(4)｜PDF第75页

设矩阵$A$与$B$相似，则必有$()$.

A.矩阵$\lambda E-A$与$\lambda E-B$相等

B.$A,B$同时可逆或不可逆

C.$A$和$B$有相同的特征向量

D.$A$和$B$均与同一个对角矩阵相似

#### Q191｜原题(5)｜PDF第75页

设$A$为$3$阶方阵,$A$的三个特征值为$1,1,2,\alpha_{1},\alpha_{2},\alpha_{3}$分别为对应的三个特征向量,则$()$.

A.$\alpha_{1},\alpha_{2},\alpha_{3}$必为$2E-A$的特征向量

B.$\alpha_{1}+\alpha_{3}$必为$2E-A$的特征向量

C.$\alpha_{1}-\alpha_{2}$必为$2E-A$的特征向量

D.$\alpha_{1},\alpha_{2}$必为$2E-A$的特征向量,$\alpha_{3}$不是$2E-A$的特征向量

#### Q192｜原题(6)｜PDF第75页

设$3$阶实矩阵$A$有三重特征值$1,f(x)=\left|xE-A\right|-\left|A^{-1}\right|$,其中$E$是$3$阶单位矩阵,$x\in R$,则至少存在一点$x_{0}\in (0,1)$,使得$y=f(x)$在点$(x_{0},f(x_{0}))$处的切线$()$.

A.平行于直线$y=1$

B.垂直于直线$y=1$

C.平行于直线$y=x$

D.垂直于直线$y=x$

#### Q193｜原题(7)｜PDF第76页

设

$$
P^{-1}AP=\begin{pmatrix}1 & 0 & 0 \\
0 & 2 & 0 \\
0 & 0 & 2\end{pmatrix},\alpha_{1}
$$

是$A$的特征值$\lambda_{1}=1$对应的特征向量,$\alpha_{2}$与$\alpha_{3}$是$A$的特征值$\lambda_{2}=\lambda_{3}= 2$对应的特征向量，则下列选项中关于矩阵$P$的可能取值错误的是$()$.

A.$P=(\alpha_{1},\alpha_{3},\alpha_{2})$

B.$P=(\alpha_{1},-2\alpha_{2},3\alpha_{3})$

C.$P=(\alpha_{1},\alpha_{2}-\alpha_{3},\alpha_{2}+2\alpha_{3})$

D.$P=(\alpha_{1}+\alpha_{2},\alpha_{1}+\alpha_{3},\alpha_{3})$

### 基础题 · 填空题

#### Q194｜原题(1)｜PDF第76页

设方阵$A$满足$A^{2}+2A+E=O$，则$A$有特征值$\underline{\qquad\qquad}$.

#### Q195｜原题(2)｜PDF第76页

设$A$是$3$阶实对称矩阵，$A$的特征值为$1,1,-2$，且$\lambda_{3}=-2$对应的特征向量为$\xi_{3}=(1,1,-1)^{T}$，则$A=\underline{\qquad\qquad}$.

#### Q196｜原题(3)｜PDF第77页

设

$$
A=\begin{pmatrix}2 & 0 & 0 \\
0 & 0 & 1 \\
0 & 1 & a\end{pmatrix}
$$

与

$$
B=\begin{pmatrix}2 & 0 & 0 \\
0 & 3 & 4 \\
0 & -2 & b\end{pmatrix}
$$

相似，则$a=\underline{\qquad\qquad}$，$b=\underline{\qquad\qquad}$.

#### Q197｜原题(4)｜PDF第77页

设$3$阶实对称矩阵$A$的特征值为$1,2,-1$，特征值$1$与$2$的特征向量分别为$\alpha_{1}=(2,3,-1)^{T}$与$\alpha_{2} =(1,a,2a)^{T},A^{*}$是$A$的伴随矩阵,则方程组$(A^{*}-2E)X=0$的通解是$\underline{\qquad\qquad}$.

#### Q198｜原题(5)｜PDF第77页

设$\alpha_{1},\alpha_{2},\alpha_{3}$为线性无关的$3$维列向量，$A=(\alpha_{1},\alpha_{2},\alpha_{3})$，交换$A$的第$2$列与第$3$列，再将第$2$列乘以$(-4)$、第$3$列乘以$(-1)$得$C$，若$BA=C$，则$\operatorname{tr}(B)=\underline{\qquad\qquad}$.

### 基础题 · 解答题

#### Q199｜原题(1)｜PDF第78页

设

$$
A=\begin{pmatrix}1 & 2 & 2 \\
2 & 1 & 2 \\
2 & 2 & 1\end{pmatrix}.
$$

(I)求$A$的全部特征值和特征向量;

(II)求可逆矩阵$P$，使得$P^{-1}AP=\Lambda$；

(III)求正交矩阵$Q$,使得$Q^{-1}AQ=\Lambda$.

#### Q200｜原题(2)｜PDF第78页

判别下列矩阵$A$与$B$是否相似.若相似，求可逆矩阵$P$，使得$P^{-1}AP=B$.

(I)

$$
A=\begin{pmatrix}1 & 1 & 1 \\
1 & 1 & 1 \\
1 & 1 & 1\end{pmatrix},B=\begin{pmatrix}3 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0\end{pmatrix};
$$

(II)

$$
A=\begin{pmatrix}2 & 0 & 0 \\
0 & 0 & 1 \\
0 & 1 & 0\end{pmatrix},B=\begin{pmatrix}1 & 0 & 0 \\
0 & -1 & 0 \\
0 & -6 & 2\end{pmatrix}.
$$

#### Q201｜原题(3)｜PDF第79页

设矩阵

$$
A=\begin{pmatrix}2 & -1 & 2 \\
5 & a & 3 \\
-1 & b & -2\end{pmatrix}
$$

有特征向量$\alpha =(1,1,-1)^{T}$.

(I)确定参数$a,b$及$\alpha$对应的特征值$\lambda$;

(II)问$A$能否相似于对角矩阵?说明理由.

#### Q202｜原题(4)｜PDF第79页

设

$$
A=\begin{pmatrix}1 & -1 & 1 \\
x & 4 & y \\
-3 & -3 & 5\end{pmatrix},A\sim \Lambda,
$$

且$\lambda =2$是$A$的二重特征值,求$x,y$的值及可逆矩阵$P$,使得$P^{-1}AP =\Lambda$.

#### Q203｜原题(5)｜PDF第80页

设$A$是$3$阶矩阵,$\alpha_{1},\alpha_{2},\alpha_{3}$是线性无关的$3$维列向量,且$A\alpha_{1}=\alpha_{1}+\alpha_{2}+\alpha_{3},A\alpha_{2}=2\alpha_{2}+\alpha_{3},A\alpha_{3}= 2\alpha_{2}+3\alpha_{3}$.

(I)求$A$的全部特征值;

(II)求可逆矩阵$P$及$\Lambda$,使得$P^{-1}AP=\Lambda$,并计算$\left|A-2E\right|$.

#### Q204｜原题(6)｜PDF第80页

设实矩阵

$$
A=\begin{pmatrix}-1 & 0 & 2 \\
a & 1 & 1 \\
1 & 0 & 0\end{pmatrix}
$$

有三个线性无关的特征向量.

(I)求$a$的值;

(II)求可逆矩阵$P$,使得$P^{-1}AP$为对角矩阵.

#### Q205｜原题(7)｜PDF第81页

设$A$是$3$阶实对称矩阵,

$$
A\sim B,B=\begin{pmatrix}1 & 2 & 3 \\
2 & 4 & 6 \\
3 & 6 & 9\end{pmatrix},A
$$

的二重特征值对应的特征向量为$\alpha_{1}=(1,1,0)^{T}$,$\alpha_{2}=(0,2,1)^{T}$.

(I)求$A$的特征值与特征向量;

(II)求可逆矩阵$P$,使得$P^{-1}AP=\Lambda$.

#### Q206｜原题(8)｜PDF第81页

已知

$$
A\sim B,A=\begin{pmatrix}1 & a & -1 \\
1 & 5 & 1 \\
4 & 12 & 6\end{pmatrix},B=\begin{pmatrix}b &  &  \\
 & b &  \\
 &  & c\end{pmatrix},
$$

求$a,b,c$的值.

#### Q207｜原题(9)｜PDF第82页

设

$$
A=\begin{pmatrix}a & 0 & 1 \\
0 & -a & 0 \\
1 & 0 & a\end{pmatrix}
$$

与

$$
B=\begin{pmatrix}-1 & 1 & 0 \\
1 & -1 & 0 \\
0 & 0 & a^{2}\end{pmatrix}(a\ne 0)
$$

相似.

(I)求$a$的值;

(II)求正交矩阵$Q$,使得$Q^{-1}AQ=B$;

(III)求一个$3$阶矩阵$P$,使得$AB=P^{2}$.

#### Q208｜原题(10)｜PDF第82页

设$3$阶实对称矩阵$A$的特征值为$\lambda_{1}=\lambda_{2}=1,\lambda_{3}=-1,\alpha_{1}=(1,1,1)^{T},\alpha_{2}=(2,2,1)^{T}$是$\lambda_{1}=\lambda_{2}=1$对应的特征向量.

(I)求$A$的属于$\lambda_{3}=-1$的特征向量;

(II)求矩阵$A$.

#### Q209｜原题(11)｜PDF第83页

(I)设$A$是$n$阶实对称矩阵，且$A^{2}=A$，$r(A)=r(r<n)$，计算了$\left|3E-A\right|$；

(II)设$A$是$n$阶矩阵,且$A^{2}=A,r(A)=r(r<n)$,计算$\left|3E-A\right|$.

#### Q210｜原题(12)｜PDF第83页

设

$$
A=\begin{pmatrix}2 & 0 & 4 & 0 \\
0 & 6 & 0 & 0 \\
4 & 0 & a & 0 \\
0 & 0 & 0 & -2\end{pmatrix}
$$

与

$$
\Lambda =\begin{pmatrix}6 & 0 & 0 & 0 \\
0 & 6 & 0 & 0 \\
0 & 0 & b & 0 \\
0 & 0 & 0 & -2\end{pmatrix}
$$

相似.

(I)求$a,b$的值；

(II)求一个正交矩阵$P$,使得$P^{-1}AP=\Lambda$.

#### Q211｜原题(13)｜PDF第84页

(I)设$A$与$B$是$n$阶方阵,$A$可逆,且$A\sim B$,证明:$A^{*}\sim B^{*}$;

(II)若$A\sim B$,证明:存在可逆矩阵$P($非数量矩阵$)$,使得$AP\sim BP$.

#### Q212｜原题(14)｜PDF第84页

设矩阵

$$
A=\begin{pmatrix}1 & 1 & 1 \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}\end{pmatrix}
$$

有$3$个特征向量$\alpha_{1}=(1,1,1)^{T},\alpha_{2}=(1,1,0)^{T},\alpha_{3}=(1,0,0)^{T}$.

(I)求$A$;

(II)求一个可逆矩阵$P$,使得$P^{-1}AP=A^{T}$.

#### Q213｜原题(15)｜PDF第85页

设

$$
A=\begin{pmatrix}1 & 1 & a \\
1 & a & 1 \\
a & 1 & 1\end{pmatrix},b=\begin{pmatrix}1 \\
1 \\
-2\end{pmatrix}.
$$

方程组$AX=b$有无穷多解.

(I)求$a$的值及$AX=b$的通解;

(II)求正交矩阵$Q$及对角矩阵$\Lambda$，使得$Q^{T}AQ=\Lambda$.

### 综合题 · 选择题

#### Q214｜原题(1)｜PDF第85页

设$A,B$是$n$阶可逆矩阵，且$A^{-1}\sim B^{-1}$，则下列结果

①$AB\sim BA$；②$A\sim B$；③$A^{2}\sim B^{2}$；④$A^{T}\sim B^{T}$中正确的个数为$()$.

A.$1$

B.$2$

C.$3$

D.$4$

#### Q215｜原题(2)｜PDF第86页

设矩阵$B$相似于

$$
A=\begin{pmatrix}1 & 1 & 0 & 0 \\
1 & 1 & 0 & 0 \\
0 & 0 & 2 & 2 \\
0 & 0 & 2 & 2\end{pmatrix}
$$

，则$r_{1}=r(B),r_{2}=r(B-E),r_{3}=r(B-2E)$满足$()$.

A.$r_{1}<r_{2}<r_{3}$

B.$r_{2}<r_{3}<r_{1}$

C.$r_{3}<r_{1}<r_{2}$

D.$r_{1}<r_{3}<r_{2}$

#### Q216｜原题(3)｜PDF第86页

与

$$
\Lambda =\begin{pmatrix}0 &  &  \\
 & 1 &  \\
 &  & -1\end{pmatrix}
$$

既相似又合同的矩阵是$()$.

A.

$$
A=\begin{pmatrix}1 & 0 & 0 \\
0 & 1 & -1 \\
0 & 2 & -2\end{pmatrix}
$$

B.

$$
B=\begin{pmatrix}1 & 0 & 0 \\
0 & -1 & -2 \\
0 & -2 & -4\end{pmatrix}
$$

C.

$$
C=\begin{pmatrix}1 & 0 & 0 \\
0 & -\frac{1}{2} & \frac{1}{2} \\
0 & \frac{1}{2} & -\frac{1}{2}\end{pmatrix}
$$

D.

$$
D=\begin{pmatrix}1 & 0 & 0 \\
0 & -1 & 2 \\
0 & 2 & 2\end{pmatrix}
$$

#### Q217｜原题(4)｜PDF第86页

下列矩阵中，与矩阵

$$
\begin{pmatrix}1 & 1 & 0 \\
0 & 1 & 1 \\
0 & 0 & 1\end{pmatrix}
$$

相似的是$()$.

A.

$$
\begin{pmatrix}1 & 1 & -1 \\
0 & 1 & 1 \\
0 & 0 & 1\end{pmatrix}
$$

B.

$$
\begin{pmatrix}1 & 0 & -1 \\
0 & 1 & 1 \\
0 & 0 & 1\end{pmatrix}
$$

C.

$$
\begin{pmatrix}1 & 1 & -1 \\
0 & 1 & 0 \\
0 & 0 & 1\end{pmatrix}
$$

D.

$$
\begin{pmatrix}1 & 0 & -1 \\
0 & 1 & 0 \\
0 & 0 & 1\end{pmatrix}
$$

#### Q218｜原题(5)｜PDF第87页

设$n$阶矩阵$A$有特征值$\lambda_{1}=1,\lambda_{2}=-1$,对应的特征向量为$\alpha_{1},\alpha_{2},k$为任意常数,则下列选项正确的是$()$.

A.$k\alpha_{1}$必是$A$的特征向量

B.$\alpha_{1}-\alpha_{2}$必是$A$的特征向量

C.$\alpha_{1}+\alpha_{2}$必是$A$的特征向量

D.$\alpha_{1}+\alpha_{2}$必是$A^{2}$的特征向量

#### Q219｜原题(6)｜PDF第87页

设$A$是$3$阶实对称矩阵,$\alpha =(-1,1,1)^{T}$满足$(A-2E)\alpha =0$,且$r(A)=1.k_{1},k_{2}$为任意常数,则方程组$AX=0$的通解为$()$.

A.$k_{1}(1,1,0)^{T}+k_{2}(1,-1,0)^{T}$

B.$k_{1}(1,1,0)^{T}+k_{2}(1,0,1)^{T}$

C.$k_{1}(1,1,0)^{T}+k_{2}(1,1,1)^{T}$

D.$k_{1}(1,1,0)^{T}+k_{2}(1,0,-1)^{T}$

#### Q220｜原题(7)｜PDF第87页

设$3$维列向量$\alpha_{1},\alpha_{2},\alpha_{3}$线性无关，$A=(a_{ij})_{3\times 3}$满足$A\alpha_{1}=\alpha_{1},A\alpha_{2}=\alpha_{2}+\alpha_{3},A\alpha_{3}=\alpha_{1}+\alpha_{3},A_{ij}$是$a_{ij}$的代数余子式,则$A_{11}+A_{22}+A_{33}=()$.

A.$1$

B.$2$

C.$3$

D.$4$

#### Q221｜原题(8)｜PDF第88页

设$A,B,C$均为$3$阶矩阵，$r(C)=1$，$r(B)=2$，且满足$(A+E)C=O,B(A^{T}-2E)=O$，则下列矩阵中与$A$相似的是$()$.

A.

$$
\begin{pmatrix}2 & 1 & 0 \\
0 & 2 & 1 \\
0 & 0 & 1\end{pmatrix}
$$

B.

$$
\begin{pmatrix}-1 & 1 & 0 \\
0 & -1 & 1 \\
0 & 0 & 2\end{pmatrix}
$$

C.

$$
\begin{pmatrix}-2 & 0 & 0 \\
0 & -2 & 0 \\
0 & 0 & 1\end{pmatrix}
$$

D.

$$
\begin{pmatrix}-1 & 0 & 0 \\
0 & 2 & 0 \\
0 & 0 & 2\end{pmatrix}
$$

#### Q222｜原题(9)｜PDF第88页

设两个不相等的$3$阶矩阵$A,B$满足$(A-B)^{2}=O$，则下列选项正确的是$()$.

A.$A-B$是对角矩阵

B.$A-B$只有一个线性无关的特征向量

C.$A-B$只有两个线性无关的特征向量

D.$A-B$有三个线性无关的特征向量

### 综合题 · 填空题

#### Q223｜原题(1)｜PDF第88页

设$A$是$3$阶方阵,$\alpha$为$3$维列向量,$P=(\alpha,A\alpha,A^{2}\alpha)$为可逆矩阵,$B=P^{-1}AP$,且$A^{3}\alpha +2A^{2}\alpha =3A\alpha$，则$\left|A+E\right|=\underline{\qquad\qquad}$.

#### Q224｜原题(2)｜PDF第89页

设$A_{3\times 3}$是秩为$1$的实对称矩阵，$\lambda_{1}=2$是$A$的一个特征值，对应的特征向量为$\alpha_{1}=(-1,1,1)^{T}$，则方程组$Ax=0$的基础解系为$\underline{\qquad\qquad}$.

#### Q225｜原题(3)｜PDF第89页

设$3$阶矩阵$A$的特征值为$0,1,2,B=A^{3}-2A^{2}$，则$r(B)=\underline{\qquad\qquad}$.

#### Q226｜原题(4)｜PDF第89页

设$\alpha_{1},\alpha_{2},\cdots,\alpha_{k}(k>1)$是$n$维正交单位实列向量组，$A=\sum_{i=1}^{k}\alpha_{i}\alpha_{i}^{T},E$是$n$阶单位矩阵，则行列式$\left|(A+E)^{*}\right|=\underline{\qquad\qquad}$.

### 综合题 · 解答题

#### Q227｜原题(1)｜PDF第90页

设

$$
A=\begin{pmatrix}1 & 2 & 1 \\
2 & 4 & k \\
1 & k & 1\end{pmatrix}
$$

有一个特征值为$0$,求$k$的值.并求一个正交矩阵$Q$,使得$Q^{T}AQ=\Lambda$.

#### Q228｜原题(2)｜PDF第90页

已知$A=(\alpha_{1},\alpha_{2},\alpha_{3})$是$3$阶可逆矩阵，$B$是$3$阶矩阵，且$BA=(\alpha_{1},-4\alpha_{3},-\alpha_{2})$.

(I)求$B$的全部特征值;

(II)求可逆矩阵$P$和对角矩阵$\Lambda$,使得$P^{-1}BP=\Lambda$.

#### Q229｜原题(3)｜PDF第91页

设$A$是$n(n\ge 2)$阶矩阵，$\alpha_{1},\alpha_{2},\cdots,\alpha_{n}$是$n$维列向量，且$A\alpha_{1}=\alpha_{2},A\alpha_{2}=\alpha_{3},\cdots,A\alpha_{n-1}=\alpha_{n}$，$A\alpha_{n} =0,\alpha_{n}\ne 0$.

(I)证明:$\alpha_{1},\alpha_{2},\cdots,\alpha_{n}$线性无关;

(II)求可逆矩阵$P$及三角矩阵$B$,使得$P^{-1}AP=B$.

#### Q230｜原题(4)｜PDF第91页

设$\alpha_{1}$是$3$阶矩阵$A$的属于特征值$\lambda (\lambda \ne 0)$的特征向量,$3$维列向量$\alpha_{2},\alpha_{3}$满足$(\lambda E-A)\alpha_{2}=\alpha_{1},(\lambda E-A)\alpha_{3}=\alpha_{2}$.

(I)证明:$\alpha_{1},\alpha_{2},\alpha_{3}$线性无关;

(II)计算行列式$\left|A+A^{*}\right|$,其中$A^{*}$是$A$的伴随矩阵.

#### Q231｜原题(5)｜PDF第92页

设$A_{3\times 3}$有三个不同的特征值$\lambda_{1},\lambda_{2},\lambda_{3}$,它们对应的特征向量分别为$\alpha_{1},\alpha_{2},\alpha_{3}$,令$\beta =\alpha_{1}+\alpha_{2}+\alpha_{3}$.

(I)证明:$\beta,A\beta,A^{2}\beta$线性无关;

(II)若$A^{3}\beta =A\beta$,求$r(A-E)$.

#### Q232｜原题(6)｜PDF第92页

设

$$
A=\begin{pmatrix}1 & a & 0 & 2 \\
0 & 1 & 2 & 0 \\
0 & 0 & -1 & b \\
0 & 0 & 0 & -1\end{pmatrix}
$$

有四个线性无关的特征向量.

(I)求可逆矩阵$P$,使得$P^{-1}AP=\Lambda$;

(II)求$(2E-A^{2})^{-1}$.

#### Q233｜原题(7)｜PDF第93页

设$\alpha =(a_{1},a_{2},\cdots,a_{n})^{T},\beta =(b_{1},b_{2},\cdots,b_{n})^{T}$均为非零列向量,$A=\alpha \beta^{T}$.

(I)求$A$的全部特征值;

(II)当$\alpha^{T}\beta$满足什么条件时,$A$可以相似于对角矩阵$\Lambda $?并求可逆矩阵$P$,使$P^{-1}AP=\Lambda$.

#### Q234｜原题(8)｜PDF第93页

设$n(n>2)$阶矩阵

$$
A=\begin{pmatrix}a & 1 & 1 & \cdots  & 1 \\
1 & a & 1 & \cdots  & 1 \\
1 & 1 & a & \cdots  & 1 \\
\vdots  & \vdots  & \vdots  &  & \vdots  \\
1 & 1 & 1 & \cdots  & a\end{pmatrix}.
$$

(I)求可逆矩阵$P$及对角矩阵$\Lambda$,使得$P^{-1}AP=\Lambda$;

(II)求$r(A^{*})$.

#### Q235｜原题(9)｜PDF第94页

设$A$是$3$阶实对称矩阵,存在可逆矩阵$P$,使得$P^{-1}AP=\operatorname{diag}(1,2,-1)$,且$\alpha_{1}=(1,k+1,2)^{T},\alpha_{2}= (k-1,-k,1)^{T}$分别为$A$的特征值$\lambda_{1}=1,\lambda_{2}=2$的特征向量,$A^{*}$的特征值$\lambda_{0}$对应的特征向量$\beta = (2,-5k,2k+1)^{T}$.求:

(I)$\lambda_{0}$与$k$的值;

(II)矩阵$(A^{-1})^{*}$.

#### Q236｜原题(10)｜PDF第94页

设$\alpha,\beta$为$3$维单位列向量,且$\alpha^{T}\beta =0$,记$A=\alpha \beta^{T}+\beta \alpha^{T}$.

(I)证明:$A$相似于对角矩阵;

(II)若存在$3$维列向量$\gamma \ne 0$,使得$A\gamma =0$,记$P=(\gamma,2(\alpha +\beta),\beta -\alpha)$,求$P^{-1}AP$.

#### Q237｜原题(11)｜PDF第95页

设

$$
A=\begin{pmatrix}1 & a_{12} & a_{13} \\
1 & a_{22} & a_{23} \\
1 & a_{32} & a_{33}\end{pmatrix}
$$

可逆,$B$是$3$阶实对称矩阵,且满足

$$
BA=\begin{pmatrix}1 & 2a_{12} & 2a_{13} \\
1 & 2a_{22} & 2a_{23} \\
1 & 2a_{32} & 2a_{33}\end{pmatrix}.
$$

求:

(I)$B$的特征值和对应的特征向量;

(II)正交矩阵$Q$，使得$Q^{T}BQ=\Lambda$.

#### Q238｜原题(12)｜PDF第95页

设向量组$(i)\alpha_{1}=(-a,0,1)^{T},\alpha_{2}=(1-a,a,1-a)^{T},\alpha_{3}=(1,0,-a)^{T},(ii)\beta_{1}=(-1,0,a)^{T},\beta_{2}= (-1,1,a)^{T},\beta_{3}=(1,-1,-a)^{T}(a\ne 0)$,向量组$(i)$与$(ii)$等价.

(I)求$a$的值;

(II)记$A=(\alpha_{1},\alpha_{2},\alpha_{3})$,当$a$为何值时,存在正交矩阵$Q$,使得$Q^{-1}AQ=\Lambda$,并求$Q$及$\Lambda$.

#### Q239｜原题(13)｜PDF第96页

设

$$
A=\begin{pmatrix}a & 0 & 1 \\
0 & -a & 0 \\
1 & 0 & a\end{pmatrix},B=\begin{pmatrix}-1 & 1 & 0 \\
1 & -1 & 0 \\
0 & 0 & -a\end{pmatrix},\beta =\begin{pmatrix}1 \\
1 \\
a\end{pmatrix},a\ne 0.
$$

若方程组$AX=\beta$有无穷多解.

(I)求$a$的值,并求方程组$AX=\beta$的全部解;

(II)当$a$为何值时,存在正交矩阵$Q$,使得$Q^{-1}AQ=B$?并求正交矩阵$Q$.

#### Q240｜原题(14)｜PDF第96页

设$A,B$均是$n$阶矩阵.

(I)证明:$AB$与$BA$有相同的特征值;

(II)若$AB=BA$,且$A$有$n$个不同的特征值,证明:$B$相似于对角矩阵.

#### Q241｜原题(15)｜PDF第97页

设

$$
A=\begin{pmatrix}0 & 2 & 3 \\
2 & 2 & a \\
2 & 3 & 4\end{pmatrix},3
$$

阶实对称矩阵$B$满足$AB+B=A+E,B\ne E$,其中$E$为单位矩阵.

(I)求$a$的值;

(II)求所有满足题干的矩阵$B$;

(III)求可逆矩阵$P$及对角矩阵$\Lambda$,使得$P^{-1}BP=\Lambda$.

#### Q242｜原题(16)｜PDF第97页

设$A,B$均是$3$阶方阵,$AB=A-B,A$有三个不同的特征值$\lambda_{1},\lambda_{2},\lambda_{3}$.证明:

(I)$\lambda_{i}\ne -1(i=1,2,3)$;

(II)存在可逆矩阵$P$，使$P^{-1}AP,P^{-1}BP$同时为对角矩阵.

#### Q243｜原题(17)｜PDF第98页

设$A$是$2$阶矩阵,$\alpha$是非零向量,且$\alpha$不是$A$的特征向量.

(I)证明:$\alpha,A\alpha$线性无关;

(II)记$P=(\alpha,A\alpha)$,若$A^{2}\alpha -2A\alpha =8\alpha$,证明:$A$相似于对角矩阵,并求$P^{-1}AP$.

#### Q244｜原题(18)｜PDF第98页

设向量$\beta =(b,1,1)^{T}$可由$\alpha_{1}=(a,0,1)^{T},\alpha_{2}=(1,a-1,1)^{T},\alpha_{3}=(1,0,a)^{T}$线性表示,且表示法不唯一.记$A=(\alpha_{1},\alpha_{2},\alpha_{3})$.求:

(I)$a,b$的值,并写出$\beta$由$\alpha_{1},\alpha_{2},\alpha_{3}$表示的线性表达式.

(II)一个可逆矩阵$P$,使得$P^{-1}AP=\Lambda (\Lambda$为对角矩阵$)$.

#### Q245｜原题(19)｜PDF第99页

设

$$
A=\begin{pmatrix}2 & 1 & 0 \\
1 & 2 & 0 \\
0 & 0 & 1\end{pmatrix}
$$

与

$$
B=\begin{pmatrix}a & b & c \\
0 & 1 & 0 \\
-1 & -2 & 4\end{pmatrix}
$$

相似.

(I)求$a,b,c$的值;

(II)求可逆矩阵$P$，使得$P^{-1}AP=B$；

(III)记$A$的伴随矩阵为$A^{*}$,求方程组$(3E-A^{*})X=0$的通解.

#### Q246｜原题(20)｜PDF第99页

设

$$
B=\begin{pmatrix}1 & -1 & 0 \\
1 & 0 & k \\
-1 & 1 & 1-k\end{pmatrix}
$$

不可逆,且满足$AB=B,B^{*}(A^{T}+E)=O$,其中$A$是$3$阶矩阵,$E$是$3$阶单位矩阵,$B^{*}$是$B$的伴随矩阵.

(I)求$r(B^{*})$;

(II)证明:$A$相似于对角矩阵,并求$A^{2}$.

### 拓展题 · 解答题

#### Q247｜原题(1)｜PDF第100页

设$A$是$3$阶实对称矩阵，且$A^{2}-2A=O,r(A)=1$.方程组$Ax=0$的通解为$k_{1}(1,1,0)^{T}+ k_{2}(1,0,1)^{T}(k_{1},k_{2}$为任意常数$)$.

(I)求可逆矩阵$P$及对角矩阵$\Lambda$,使得$P^{-1}AP=\Lambda$;

(II)求矩阵$A$.

#### Q248｜原题(2)｜PDF第100页

设数列$\{a_{n}\},\{b_{n}\}$满足$a_{0}=1,b_{0}=-1$,且

$$
\begin{cases}a_{n}=a_{n-1}+2b_{n-1}, \\
b_{n}=-a_{n-1}+4b_{n-1},\end{cases}
$$

记

$$
\alpha_{n}=\begin{pmatrix}a_{n} \\
b_{n}\end{pmatrix}
$$

，矩阵$A$满足$A\alpha_{n-1}= \alpha_{n}$,求$A^{n}$及$\lim_{n\to\infty}\frac{b_{n}}{a_{n}}$.

## 第十二章二次型

### 基础题 · 选择题

#### Q249｜原题(1)｜PDF第101页

二次型$f(x_{1},x_{2},x_{3})=x_{1}x_{2}+x_{2}x_{3}+x_{1}x_{3}$的矩阵为$()$.

A.

$$
\begin{pmatrix}1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1\end{pmatrix}
$$

B.

$$
\begin{pmatrix}0 & \frac{1}{2} & \frac{1}{2} \\
\frac{1}{2} & 0 & \frac{1}{2} \\
\frac{1}{2} & \frac{1}{2} & 0\end{pmatrix}
$$

C.

$$
\begin{pmatrix}1 & \frac{1}{2} & \frac{1}{2} \\
\frac{1}{2} & 1 & \frac{1}{2} \\
\frac{1}{2} & \frac{1}{2} & 1\end{pmatrix}
$$

D.

$$
\begin{pmatrix}\frac{1}{2} & 1 & 1 \\
1 & \frac{1}{2} & 1 \\
1 & 1 & \frac{1}{2}\end{pmatrix}
$$

#### Q250｜原题(2)｜PDF第101页

二次型$f(x_{1},x_{2},x_{3})=(x_{1}-x_{2})^{2}+(x_{2}-x_{3})^{2}+(x_{3}-x_{1})^{2}$的标准形为$()$.

A.$f=y_{1}^{2}+y_{2}^{2}+y_{3}^{2}$

B.$f=2y_{1}^{2}+\frac{3}{2}y_{2}^{2}$

C.$f=y_{1}^{2}+y_{2}^{2}-y_{3}^{2}$

D.$f=2y_{1}^{2}+\frac{3}{2}y_{2}^{2}+y_{3}^{2}$

#### Q251｜原题(3)｜PDF第101页

设

$$
A=\begin{pmatrix}1 &  &  \\
 & 2 &  \\
 &  & 3\end{pmatrix}
$$

与

$$
B=\begin{pmatrix}2 &  &  \\
 & 3 &  \\
 &  & 1\end{pmatrix}
$$

合同,则合同变换矩阵$P=()$.

A.

$$
\begin{pmatrix}1 & 0 & 0 \\
0 & 0 & 1 \\
0 & 0 & 1\end{pmatrix}
$$

B.

$$
\begin{pmatrix}0 & 0 & 1 \\
1 & 0 & 0 \\
0 & 1 & 0\end{pmatrix}
$$

C.

$$
\begin{pmatrix}0 & 1 & 0 \\
1 & 0 & 0 \\
0 & 0 & 1\end{pmatrix}
$$

D.

$$
\begin{pmatrix}0 & 0 & 1 \\
1 & 0 & 0 \\
0 & 0 & 1\end{pmatrix}
$$

#### Q252｜原题(4)｜PDF第102页

设$A$是$n$阶方阵，将$A$的第$i$列与第$j$列互换，再交换第$i$行与第$j$行得到$B$，则$()$.

A.$A$与$B$等价、相似且合同

B.$A$与$B$相似、合同但不等价

C.$A$与$B$相似但不合同

D.$A$与$B$等价但不相似

#### Q253｜原题(5)｜PDF第102页

二次型$f(x_{1},x_{2},x_{3})=x_{1}^{2}+4x_{2}^{2}+4x_{3}^{2}-4x_{1}x_{2}+4x_{1}x_{3}-8x_{2}x_{3}$的规范形为$()$.

A.$f=z_{1}^{2}$

B.$f=z_{1}^{2}-z_{2}^{2}$

C.$f=z_{1}^{2}+z_{2}^{2}+z_{3}^{2}$

D.$f=z_{1}^{2}+z_{2}^{2}-z_{3}^{2}$

#### Q254｜原题(6)｜PDF第102页

设$A,B$均为$n$阶实对称矩阵，则$A$与$B$合同的充分必要条件是$()$.

A.$A$与$B$有相同的特征值

B.$A$与$B$有相同的特征向量

C.$A$与$B$有相同的行列式

D.$A$与$B$有相同的秩且有相同的正惯性指数

#### Q255｜原题(7)｜PDF第103页

设$E$是$n$阶单位矩阵,则$n(n$为偶数$)$阶实对称矩阵$A$正定的充分必要条件是$()$.

A.存在$n$阶矩阵$C$，使得$A=C^{T}C$

B.二次型$X^{T}AX$的负惯性指数为$0$

C.存在可逆矩阵$P$,使得$P^{-1}AP=E$

D.$A$的伴随矩阵$A^{*}$与$E$合同

#### Q256｜原题(8)｜PDF第103页

设

$$
A=\begin{pmatrix}1 & 2 & 0 \\
2 & 0 & 2 \\
0 & 2 & -1\end{pmatrix},
$$

若存在可逆矩阵$C$,使得$C^{T}AC=\Lambda$,则$C$可能为$()$.

A.

$$
\begin{pmatrix}1 & -1 & -1 \\
0 & \frac{1}{2} & \frac{1}{2} \\
0 & 0 & 1\end{pmatrix}
$$

B.

$$
\begin{pmatrix}1 & 2 & 0 \\
0 & 2 & -1 \\
0 & 0 & 1\end{pmatrix}
$$

C.

$$
\begin{pmatrix}1 & 2 & 0 \\
0 & 1 & 2 \\
0 & 0 & 1\end{pmatrix}
$$

D.

$$
\begin{pmatrix}1 & 1 & 1 \\
0 & \frac{1}{2} & \frac{1}{2} \\
0 & 0 & 1\end{pmatrix}
$$

#### Q257｜原题(9)｜PDF第103页

设

$$
A=\begin{pmatrix}1 & 1 & 0 \\
1 & 1 & 0 \\
0 & 0 & 1\end{pmatrix},
$$

则下列矩阵中与$A$既不相似也不合同的是$()$.

A.

$$
\begin{pmatrix}3 & 0 & 0 \\
0 & 2 & 0 \\
0 & 0 & 0\end{pmatrix}
$$

B.

$$
\begin{pmatrix}1 & 2 & 1 \\
2 & 5 & 2 \\
1 & 2 & 1\end{pmatrix}
$$

C.

$$
\begin{pmatrix}1 & -1 & 0 \\
-1 & 1 & 0 \\
0 & 0 & 1\end{pmatrix}
$$

D.

$$
\begin{pmatrix}1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & -1\end{pmatrix}
$$

#### Q258｜原题(10)｜PDF第104页

设$A$是实对称矩阵,$B=(b_{ij})_{3\times 3}$是可逆矩阵,且

$$
AB=\begin{pmatrix}b_{11} & 2b_{12} & -b_{13} \\
b_{21} & 2b_{22} & -b_{23} \\
b_{31} & 2b_{32} & -b_{33}\end{pmatrix},
$$

则二次型$X^{T}AX$的规范形为$()$.

A.$y_{1}^{2}+y_{2}^{2}+y_{3}^{2}$

B.$y_{1}^{2}+y_{2}^{2}-y_{3}^{2}$

C.$y_{1}^{2}-y_{2}^{2}-y_{3}^{2}$

D.$-y_{1}^{2}-y_{2}^{2}-y_{3}^{2}$

### 基础题 · 填空题

#### Q259｜原题(1)｜PDF第104页

已知二次型$f(x_{1},x_{2},x_{3})=x_{1}^{2}+4x_{2}^{2}+4x_{3}^{2}+2ax_{1}x_{2}-2x_{1}x_{3}+4x_{2}x_{3}$正定,则$a$的取值范围为$\underline{\qquad\qquad}$.

#### Q260｜原题(2)｜PDF第104页

设二次型$f(x_{1},x_{2},x_{3})=X^{T}AX(A^{T}=A)$在正交变换下的标准形为$-2y_{1}^{2}+8y_{2}^{2}$，且$E+B=AB$，其中$B$为$3$阶矩阵，则迹$\operatorname{tr}(B^{-1}+2E)=\underline{\qquad\qquad}$.

### 基础题 · 解答题

#### Q261｜原题(1)｜PDF第105页

设二次型$f(x_{1},x_{2},x_{3})=2x_{1}^{2}+5x_{2}^{2}+5x_{3}^{2}+4x_{1}x_{2}-4x_{1}x_{3}-8x_{2}x_{3}$.

(I)求一个正交变换$x=Qy$,将$f$化为标准形;

(II)利用配方法,将$f$化为标准形.

#### Q262｜原题(2)｜PDF第105页

已知二次型$f=2x_{1}^{2}+3x_{2}^{2}+3x_{3}^{2}+2ax_{2}x_{3}(a>0)$，经过正交变换化成标准形$y_{1}^{2}+2y_{2}^{2}+5y_{3}^{2}$，求参数$a$及所用的正交变换.

#### Q263｜原题(3)｜PDF第106页

证明:$n$阶矩阵$A$正定的充分必要条件是存在可逆矩阵$P$，使得$A=P^{T}P$.

#### Q264｜原题(4)｜PDF第106页

设$3$阶实对称矩阵$A=(\alpha_{1},\alpha_{2},\alpha_{3}),r(A)=2$，且满足$\alpha_{1}+2\alpha_{2}+\alpha_{3}=(3,6,3)^{T},\alpha_{1}-\alpha_{2}+\alpha_{3}= (-1,1,-1)^{T}$.

(I)求$A$;

(II)若$X=(x_{1},x_{2},x_{3})^{T}$,求方程$X^{T}(A+E)X=0$的全部解.

#### Q265｜原题(5)｜PDF第107页

设二次型$f(x_{1},x_{2},x_{3})=(x_{1}+x_{2})^{2}+(x_{2}-x_{3})^{2}+(x_{1}+ax_{3})^{2}$.

(I)求$f(x_{1},x_{2},x_{3})=0$的解;

(II)当$f(x_{1},x_{2},x_{3})=0$有非零解时,求正交变换$X=QY$,将$f(x_{1},x_{2},x_{3})$化为标准形;

(III)求$f(x_{1},x_{2},x_{3})$的规范形.

#### Q266｜原题(6)｜PDF第107页

设$3$阶实对称矩阵$A=(\alpha_{1},\alpha_{2},\alpha_{3})$有二重特征值$1$,且$\alpha_{1}+2\alpha_{2}-\alpha_{3}=0,A^{*}$是$A$的伴随矩阵.

(I)求正交变换$X=QY$，将二次型$f(x_{1},x_{2},x_{3})=X^{T}AX$化为标准形；

(II)求方程组$A^{*}X=0$的通解.

#### Q267｜原题(7)｜PDF第108页

设$A$是$3$阶实对称矩阵，$\alpha =(-1,1,1)^{T}$满足$(A-2E)\alpha =0$，且$r(A)=1$.

(I)求方程组$AX=0$的通解；

(II)求$A$;

(III)若$X=(x_{1},x_{2},x_{3})^{T}$,求方程$X^{T}AX=0$的全部解.

#### Q268｜原题(8)｜PDF第108页

设

$$
A=\begin{pmatrix}2 & 0 & 1 \\
0 & 2 & -1 \\
1 & -1 & a-1\end{pmatrix}
$$

与

$$
B=\begin{pmatrix}0 & 0 & 0 \\
0 & b & 0 \\
0 & 0 & 3\end{pmatrix}
$$

合同.

(I)求$a$的值及$b$的取值范围;

(II)若存在正交矩阵$Q$,使得$Q^{T}AQ=B$,求$b$及$Q$.

#### Q269｜原题(9)｜PDF第109页

设实对称矩阵$A=(a_{ij})_{3\times 3}$有二重特征值$1$，且$\sum_{i=1}^{3}a_{ij}=0(j=1,2,3)$.

(I)记$X=(x_{1},x_{2},x_{3})^{T}$,求方程$X^{T}AX=0$的全部解;

(II)求可逆矩阵$P$,使得$X^{T}(2E-A)X=\lVert PX\rVert^{2}$.

### 综合题 · 选择题

#### Q270｜原题(1)｜PDF第109页

二次型$f(x_{1},x_{2},x_{3})=x_{1}x_{2}+x_{2}x_{3}$的正、负惯性指数分别为$()$.

A.$p=1,q=1$

B.$p=1,q=2$

C.$p=1,q=0$

D.$p=0,q=2$

#### Q271｜原题(2)｜PDF第110页

$A$是$n$阶实对称矩阵，$B$是$n$阶矩阵，则$A$合同于矩阵$B$的充分必要条件是$()$.

①$r(A)=r(B)$；②$A$与$B$的正惯性指数相等;

③$A$与$B$均正定矩阵；④$B$是实对称矩阵.

A.①成立

B.④成立

C.①②④均成立

D.③成立

#### Q272｜原题(3)｜PDF第110页

设

$$
A=\begin{pmatrix}2 & 1 \\
-1 & 0\end{pmatrix},B=\begin{pmatrix}1 & 1 \\
0 & 1\end{pmatrix},C=\begin{pmatrix}1 & 0 \\
1 & 1\end{pmatrix},D=\begin{pmatrix}1 & 0 \\
0 & 1\end{pmatrix}
$$

，则下列选项正确的是$()$.

A.$A$与$B$相似，$B$与$C$合同

B.$A$与$D$相似，$B$与$D$合同

C.$A$与$D$合同,$B$与$C$相似

D.$B$与$D$相似,$C$与$D$合同

#### Q273｜原题(4)｜PDF第110页

设$A$是$3$阶实对称矩阵,且$\left|A\right|=2,A^{*}=A-E$，其中$A^{*}$是$A$的伴随矩阵，则二次型$x^{T}Ax$的规范形为$()$.

A.$y_{1}^{2}+y_{2}^{2}+y_{3}^{2}$

B.$-y_{1}^{2}-y_{2}^{2}-y_{3}^{2}$

C.$y_{1}^{2}+y_{2}^{2}-y_{3}^{2}$

D.$-y_{1}^{2}-y_{2}^{2}+y_{3}^{2}$

#### Q274｜原题(5)｜PDF第111页

设

$$
A=\begin{pmatrix}1 & 2 \\
2 & 1\end{pmatrix},B=\begin{pmatrix}1 & 4 \\
1 & 1\end{pmatrix},
$$

则下列选项正确的是$()$.

A.必存在正交矩阵$Q$,使得$Q^{-1}AQ=B$

B.必存在可逆矩阵$P$,使得$P^{-1}AP=B$

C.必存在可逆矩阵$P$,使得$P^{T}AP=B$

D.必存在可逆矩阵$P$,使得$A=P^{T}P$

#### Q275｜原题(6)｜PDF第111页

设$3$阶实矩阵$A$的特征向量为$\alpha_{1}=(-1,1,0)^{T},\alpha_{2}=(1,1,1)^{T},\alpha_{3}=(-1,-1,2)^{T}$,则$A$必为$()$.

A.可逆矩阵

B.正交矩阵

C.对称矩阵

D.正定矩阵

#### Q276｜原题(7)｜PDF第111页

设实矩阵

$$
A=\begin{pmatrix}a & a-1 \\
a-1 & a-1\end{pmatrix}
$$

，若对任意的二维非零实列向量$X$，都有$\left|X^{T}AX\right|<\left|X^{T}X\right|$，则$a$的取值范围为$()$.

A.$(\frac{1}{3},1)$

B.$(-1,1)$

C.$(-1,0]$

D.$(\frac{1}{3},1]$

#### Q277｜原题(8)｜PDF第112页

设$\alpha_{1}=(1,2)^{T},\alpha_{2}=(a,1)^{T},X=(x_{1},x_{2})^{T}$,若二次型$f(x_{1},x_{2})=(\alpha_{1},X)^{2}+(\alpha_{2},X)^{2}$经可逆线性变换$X=PY$化为$g(y_{1},y_{2})=by_{1}^{2}+by_{2}^{2}+2by_{1}y_{2}(b\ne 0)$,则$()$.

A.$a=\frac{1}{2},b>0$

B.$a=-\frac{1}{2},b>0$

C.$a=\frac{1}{2},b>-1$

D.$a=-\frac{1}{2},b>-1$

#### Q278｜原题(9)｜PDF第112页

设$\alpha$是$3$维实列向量，且满足$\alpha^{T}\alpha =1,A=E-\alpha \alpha^{T},A^{*}$是$A$的伴随矩阵，则二次型$f(x_{1},x_{2},x_{3})= X^{T}A^{*}X$在正交变换$X=QY$下的标准形为$()$.

A.$y_{1}^{2}+y_{2}^{2}$

B.$-y_{1}^{2}$

C.$-y_{1}^{2}-y_{3}^{2}$

D.$y_{1}^{2}$

#### Q279｜原题(10)｜PDF第112页

设$A$是$2$阶实对称矩阵,若对任意的$2$维非零列向量$X$，都有$\left|X^{T}AX\right|<\left|X^{T}X\right|$，$X_{1},X_{2}$均为$2$维列向量，则二次型

$$
\begin{pmatrix}X_{1} \\
X_{2}\end{pmatrix}^{T}\begin{pmatrix}A+E & O \\
O & E-A\end{pmatrix}\begin{pmatrix}X_{1} \\
X_{2}\end{pmatrix}
$$

的规范形为$()$.

A.$y_{1}^{2}+y_{2}^{2}-y_{3}^{2}-y_{4}^{2}$

B.$y_{1}^{2}+y_{2}^{2}+y_{3}^{2}-y_{4}^{2}$

C.$y_{1}^{2}+y_{2}^{2}+y_{3}^{2}+y_{4}^{2}$

D.$-y_{1}^{2}-y_{2}^{2}-y_{3}^{2}-y_{4}^{2}$

#### Q280｜原题(11)｜PDF第113页

设$A$是$3$阶实矩阵,$\left|A\right|=3$,且$A^{*}=-A+4E$,其中$A^{*}$是$A$的伴随矩阵,$E$是$3$阶单位矩阵,则二次型$X^{T}(2E-A)^{T}(2E-A)X$的规范形为$()$.

A.$y_{1}^{2}-y_{2}^{2}-y_{3}^{2}$

B.$y_{1}^{2}+y_{2}^{2}-y_{3}^{2}$

C.$y_{1}^{2}+y_{2}^{2}+y_{3}^{2}$

D.$-y_{1}^{2}-y_{2}^{2}-y_{3}^{2}$

#### Q281｜原题(12)｜PDF第113页

设

$$
A=\begin{pmatrix}-1 & 1 \\
1 & 1\end{pmatrix},
$$

非零实列向量$\alpha =(a,b)^{T}$,则二次型

$$
f(x_{1},x_{2},x_{3})=X^{T}\begin{pmatrix}A+\alpha \alpha^{T} & \alpha  \\
\alpha^{T} & 1\end{pmatrix}X
$$

的规范形为$()$.

A.$y_{1}^{2}+y_{2}^{2}+y_{3}^{2}$

B.$-y_{1}^{2}-y_{2}^{2}-y_{3}^{2}$

C.$y_{1}^{2}+y_{2}^{2}-y_{3}^{2}$

D.$y_{1}^{2}-y_{2}^{2}-y_{3}^{2}$

#### Q282｜原题(13)｜PDF第113页

设$A$是$3$阶实对称矩阵，$B=(\alpha_{1},\alpha_{2},\alpha_{3})$是$3$阶可逆矩阵，且$AB=(\alpha_{1},\alpha_{2}-2\alpha_{3},\alpha_{3}-2\alpha_{2})$，记$X =(x_{1},x_{2},x_{3})^{T}$,则二次型$f(x_{1},x_{2},x_{3})=\operatorname{tr}(AXX^{T})$的规范形为$()$.

A.$y_{1}^{2}-y_{2}^{2}-y_{3}^{2}$

B.$y_{1}^{2}+y_{2}^{2}-y_{3}^{2}$

C.$y_{1}^{2}+y_{2}^{2}+y_{3}^{2}$

D.$-y_{1}^{2}-y_{2}^{2}-y_{3}^{2}$

#### Q283｜原题(14)｜PDF第114页

已知

$$
A=\begin{pmatrix}1-a & a \\
a & a\end{pmatrix},X=(x_{1},x_{2})^{T}
$$

，二次型

$$
f(x_{1},x_{2})=\begin{vmatrix}A & X \\
-X^{T} & 0\end{vmatrix}
$$

，则$A$正定是$f(x_{1},x_{2})$正定的$()$.

A.充分不必要条件

B.必要不充分条件

C.充分必要条件

D.既不充分也不必要条件

### 综合题 · 填空题

#### Q284｜原题(1)｜PDF第114页

若$3$阶实对称矩阵$A$与

$$
B=\begin{pmatrix}1 & 0 & 0 \\
0 & 0 & 3 \\
0 & 3 & 0\end{pmatrix}
$$

合同，则二次型$x^{T}Ax$的规范形为$\underline{\qquad\qquad}$.

#### Q285｜原题(2)｜PDF第114页

设$A$是$n$阶矩阵，方程组$Ax=b$有唯一解，则二次型$x^{T}(A^{T}A)x$的正惯性指数为$\underline{\qquad\qquad}$.

#### Q286｜原题(3)｜PDF第115页

设$A$是$3$阶实对称矩阵，二次型$x^{T}Ax$经过正交变换$x=Qy$后的标准形为$y_{1}^{2}+y_{2}^{2}-y_{3}^{2},A^{*}$是$A$的伴随矩阵,则二次型$x^{T}A^{*}x$的规范形为$\underline{\qquad\qquad}$.

#### Q287｜原题(4)｜PDF第115页

设$3$阶实对称矩阵$A$的特征值为$2,3,4,A^{*}$是$A$的伴随矩阵.若对任意$3$维实列向量$X$，都有$\left|X^{T}A^{*}X-X^{T}AX\right|\le aX^{T}X$，则$a$的最小取值为$\underline{\qquad\qquad}$.

### 综合题 · 解答题

#### Q288｜原题(1)｜PDF第115页

设二次型$f(x_{1},x_{2},x_{3})=x^{T}Ax=x_{1}^{2}+ax_{2}^{2}+x_{3}^{2}+2x_{1}x_{2}-2ax_{1}x_{3}-2x_{2}x_{3}$的正负惯性指数都是$1$.

(I)求$a$的值;

(II)求可逆线性变换$x=By$,将$f(x_{1},x_{2},x_{3})$化为标准形.

#### Q289｜原题(2)｜PDF第116页

设$3$阶实对称矩阵$A=(a_{ij})_{3\times 3}$有特征值$\lambda_{1}=\lambda_{2}=2$，且$\sum_{i=1}^{3}a_{ii}=1,\alpha =(1,0,-2)^{T}$是方程组$A^{*}x= 4\alpha$的解向量.

(I)求矩阵$A$;

(II)求正交变换$x=Qy$,将二次型$f(x_{1},x_{2},x_{3})=x^{T}Ax$化为标准形.

#### Q290｜原题(3)｜PDF第116页

设二次型$f(x_{1},x_{2},\cdots,x_{n})=nx_{1}^{2}+nx_{2}^{2}+\cdots +nx_{n}^{2}-(x_{1}+x_{2}+\cdots +x_{n})^{2}$.

(I)求二次型$f(x_{1},x_{2},\cdots,x_{n})=x^{T}Ax$的秩;

(II)求可逆矩阵$P$,使得$P^{-1}AP=\Lambda$,并求二次型的正惯性指数.

#### Q291｜原题(4)｜PDF第117页

设方程组

$$
\begin{cases}(k+3)x_{1}+x_{2}+2x_{3}=0, \\
2kx_{1}+(k-1)x_{2}+x_{3}=0, \\
(k-3)x_{1}-3x_{2}+kx_{3}=0\end{cases}
$$

有非零解,且

$$
A=\begin{pmatrix}3 & 1 & 2 \\
1 & k & -2 \\
2 & -2 & 9\end{pmatrix}
$$

是正定矩阵.

(I)求$k$的值;

(II)设$x=(x_{1},x_{2},x_{3})^{T}$,求当$x^{T}x=1$时,$x^{T}Ax$的最大值.

#### Q292｜原题(5)｜PDF第117页

设$n$阶实对称矩阵$A$只有两个不同的特征值$\lambda_{1}=1$和$\lambda_{2}$，且$A$属于$\lambda_{1}=1$的特征向量仅有$k(1,0,\cdots,0,1)^{T}$,其中$k\ne 0$.

(I)求矩阵$A$;

(II)当$\lambda_{2}$满足什么条件时,$A$是正定矩阵?

#### Q293｜原题(6)｜PDF第118页

设$A$是实对称矩阵,证明:$A$可逆的充要条件是存在方阵$B$,使得$AB+B^{T}A$为正定矩阵.

#### Q294｜原题(7)｜PDF第118页

设二次型$f(x_{1},x_{2},x_{3})=ax_{1}^{2}-ax_{2}^{2}+ax_{3}^{2}+2x_{1}x_{3}$与$g(y_{1},y_{2},y_{3})=-y_{1}^{2}-y_{2}^{2}+a^{2}y_{3}^{2}+2y_{1}y_{2}$的秩相等$(a\ne 0)$.

(I)当$a$为何值时,仅存在可逆$($非正交$)$线性变换$x=Py$,可将$f(x_{1},x_{2},x_{3})$化为$g(y_{1},y_{2},y_{3})$?求一个可逆矩阵$P$.

(II)当$a$为何值时,存在正交变换$x=Qy$,将$f(x_{1},x_{2},x_{3})$化为$g(y_{1},y_{2},y_{3})$?说明理由.

#### Q295｜原题(8)｜PDF第119页

设二次型$f(x_{1},x_{2},x_{3})=x^{T}Ax=ax_{1}^{2}+ax_{2}^{2}+(a-1)x_{3}^{2}+2x_{1}x_{3}-2x_{2}x_{3}(a\text{为常数},A^{T}=A)$.

(I)求一个正交变换$x=Qy$,将$f(x_{1},x_{2},x_{3})$化为标准形;

(II)设$x=(x_{1},x_{2},x_{3})^{T}$,求方程$x^{T}(aE-A)^{2}x=0$的全部解.

#### Q296｜原题(9)｜PDF第119页

设二次型$x^{T}Ax=a(x_{1}^{2}+x_{2}^{2}+x_{3}^{2})+2x_{1}x_{2}+2bx_{1}x_{3}+2x_{2}x_{3}$,在正交变换$x=Qy$下的标准形为$y_{1}^{2}+ y_{2}^{2}+4y_{3}^{2}$,其中$A^{T}=A$.

(I)求$a,b$的值及正交矩阵$Q$;

(II)若正定矩阵$B$满足$B^{2}=A+A^{*}$,其中$A^{*}$是$A$的伴随矩阵,求$B$.

#### Q297｜原题(10)｜PDF第120页

设$A$是$3$阶矩阵,方程组$AX=b$的通解为$k_{1}(-1,1,0)^{T}+k_{2}(2,0,1)^{T}+(1,1,-2)^{T}$.其中$b= (6,6,-12)^{T},k_{1},k_{2}$为任意常数.

(I)求$A$;

(II)若$A$的列向量组的极大线性无关组为$\alpha$,求一个$3$维行向量$\beta$,使得$A^{2}=\alpha \beta$;

(III)记$X=(x_{1},x_{2},x_{3})^{T}$,求方程$X^{T}AX=0$的全部解.

#### Q298｜原题(11)｜PDF第120页

已知二次型$f(x_{1},x_{2},x_{3})=x_{1}^{2}+2x_{2}^{2}+2x_{3}^{2}+2ax_{2}x_{3}(a>0)$在正交变换$X=QY$下化为$g(y_{1},y_{2},y_{3}) =2y_{1}^{2}+by_{2}^{2}+2y_{3}^{2}-2y_{1}y_{3}$.

(I)求$a,b$的值;

(II)求正交矩阵$Q$.

#### Q299｜原题(12)｜PDF第121页

设

$$
A=\begin{pmatrix}1 & 0 & 1 \\
0 & 1 & 0 \\
1 & 0 & 1\end{pmatrix},B=\begin{pmatrix}1 & 0 & 1 \\
0 & 1 & 0 \\
1 & 0 & 2\end{pmatrix},E
$$

是$3$阶单位矩阵.

(I)求可逆矩阵$C$,使得$C^{T}BC=E$;

(II)求一个可逆矩阵$P$,使得$P^{T}AP=\operatorname{diag}(0,1,1)$,且$P^{T}BP=E$.

#### Q300｜原题(13)｜PDF第121页

已知二次型$f(x_{1},x_{2},x_{3})=x_{1}^{2}+2x_{2}^{2}+ax_{3}^{2}+2x_{1}x_{3}$经过可逆线性变换$X=PY$化为$y_{1}^{2}+y_{3}^{2}$.

(I)求$a$的值及可逆矩阵$P$;

(II)设$X=(x_{1},x_{2},x_{3})^{T}$,当$X^{T}X=1$时,求$f(x_{1},x_{2},x_{3})$的最大值,并求满足$x_{1}=x_{2}>0$的最大值点.

#### Q301｜原题(14)｜PDF第122页

设$3$阶矩阵$A=(\alpha_{1},\alpha_{2},\alpha_{3})$，且满足

$$
(\alpha_{1}+\alpha_{3},-\alpha_{1}+2\alpha_{2},\alpha_{2}+\alpha_{3})=\begin{pmatrix}1 & 1 & 0 \\
0 & -2 & -1 \\
1 & 0 & -1\end{pmatrix}.
$$

(I)若$X=(x_{1},x_{2},x_{3})^{T}$,证明:$X^{T}A^{2}X$为正定二次型;

(II)求可逆矩阵$P$,使得$P^{-1}AP=A^{T}$.

#### Q302｜原题(15)｜PDF第122页

设

$$
A=\begin{pmatrix}a & 0 \\
-1 & a \\
-1 & 0\end{pmatrix},B=\begin{pmatrix}-1 & 0 & a \\
-1 & 1 & a\end{pmatrix},
$$

已知方程组$ABX=0$与$BX=0$同解.

(I)求$a$的取值范围;

(II)当$AB$为实对称矩阵时,求正交变换$X=QY$,将二次型$f(x_{1},x_{2},x_{3})=X^{T}ABX$化为标准形.

#### Q303｜原题(16)｜PDF第123页

设

$$
A=\begin{pmatrix}1 & -1 & 0 \\
-1 & 1+a^{2} & a \\
0 & a & 1\end{pmatrix}(a\ne 0),X=(x_{1},x_{2},x_{3})^{T}.
$$

(I)若对$\forall X\ne 0$,有$X^{T}(A-kE)X\le 0$,求$k$的最小值;

(II)求可逆线性变换$X=CY$,将二次型$f(x_{1},x_{2},x_{3})=X^{T}AX$化为$g(y_{1},y_{2},y_{3})=y_{1}^{2}+y_{2}^{2}+y_{3}^{2}-2y_{1}y_{2}$.

#### Q304｜原题(17)｜PDF第123页

设二次型$f(x_{1},x_{2},x_{3})=2(x_{1}^{2}+x_{2}^{2}+x_{3}^{2})+2a(x_{1}x_{2}+x_{1}x_{3}+x_{2}x_{3}),a$为正整数.

(I)求正交变换$X=QY$,将$f(x_{1},x_{2},x_{3})$化为标准形;

(II)若存在可逆矩阵$P$,对任意$X=(x_{1},x_{2},x_{3})^{T}$,有$f(x_{1},x_{2},x_{3})=\Vert PX\Vert^{2}$.求$a$的值及$P$.

### 拓展题 · 解答题

#### Q305｜原题(1)｜PDF第124页

设二次型$f(x_{1},x_{2},x_{3})=2x_{1}x_{2}+3x_{2}x_{3}+4x_{1}x_{3}$，求可逆线性变换$x=Pz$，使得$f(x_{1},x_{2},x_{3})$化为标准形,并求二次型的秩及正、负惯性指数.

#### Q306｜原题(2)｜PDF第125页

设$A$为$3$阶实对称矩阵，二次型$f(x_{1},x_{2},x_{3})=x^{T}Ax$在正交变换$x=Qy$下的标准形为$-y_{1}^{2}+2y_{2}^{2} +ay_{3}^{2}$,其中$Q$的第$1$列为$(\frac{1}{\sqrt{3}},\frac{1}{\sqrt{3}},\frac{1}{\sqrt{3}})^{T}$,且$\left|A\right|=-4$.

(I)求$a$的值;

(II)求正交矩阵$Q$.

#### Q307｜原题(3)｜PDF第126页

设二次型$f(x_{1},x_{2},x_{3})=x^{T}Ax(A^{T}=A)$经正交变换$x=Qy$化为$by_{2}^{2}+c^{2}y_{3}^{2}$，其中

$$
Q=\frac{1}{\sqrt{2}}\begin{pmatrix}1 & 0 & a \\
0 & c & 0 \\
b & 0 & 1\end{pmatrix}(b>0,c>0).
$$

(I)求$a,b,c$的值及矩阵$A$;

(II)求可逆矩阵$P$,使得$A+E=P^{T}P$.

#### Q308｜原题(4)｜PDF第127页

设二次型$f(x_{1},x_{2},x_{\cdot 3})=X^{T}AX(A^{T}=A)$经过正交变换$X=QY$化为标准形$2y_{1}^{2}-y_{2}^{2}-y_{3}^{2}$,又$A^{*}\alpha = \alpha$,其中$\alpha =(1,1,-1)^{T},A^{*}$是$A$的伴随矩阵.

(I)求正交矩阵$Q$及实对称矩阵$A$；

(II)若正定矩阵$B$满足$B^{2}=A+2E$,求矩阵$B$.

#### Q309｜原题(5)｜PDF第128页

设二次型$f(x_{1},x_{2},x_{3})=x_{1}^{2}+x_{2}^{2}+x_{3}^{2}+2ax_{1}x_{2}+2ax_{1}x_{3}+2ax_{2}x_{3}$经过可逆线性变换$X=PY$化为$g(y_{1},y_{2},y_{3})=y_{1}^{2}+y_{2}^{2}+3y_{3}^{2}+2y_{1}y_{2}$.

(I)求$a$的值;

(II)求可逆矩阵$P$.

#### Q310｜原题(6)｜PDF第129页

设

$$
A=\begin{pmatrix}a & -\frac{1}{2} & -\frac{1}{2} \\
-\frac{1}{2} & a & -\frac{1}{2} \\
-\frac{1}{2} & -\frac{1}{2} & a\end{pmatrix}
$$

与

$$
B=\begin{pmatrix}b & 0 & 0 \\
0 & b & 0 \\
0 & 0 & 0\end{pmatrix}(b\ne 0)
$$

合同.

(I)求$a$的值;

(II)若存在正交矩阵$Q$,使得$Q^{T}AQ=B$,求$b$的值及$Q$;

(III)对于$(II)$中的$Q$,若$Q^{T}(A+A^{*})Q=\Lambda$,其中$A^{*}$是$A$的伴随矩阵,求对角矩阵$\Lambda$.

#### Q311｜原题(7)｜PDF第130页

设$3$阶实对称矩阵$A$有二重特征值$1$，且$(A-4E)\alpha =0$，其中$E$是单位矩阵，$\alpha =(1,1,1)^{T}$.

(I)求矩阵$A$;

(II)记$X=(x_{1},x_{2},x_{3})^{T}$,利用正交变换将二次型

$$
f(x_{1},x_{2},x_{3})=\begin{vmatrix}A & -X \\
X^{T} & 0\end{vmatrix}
$$

化为标准形.

## 原文校对说明

以下是对照原页发现的原文疑点，正文均照录，未按推测改题。

| PDF页码 | 位置 | 说明 |
|---|---|---|
| 37 | 基础题·选择题(4) | 命题①中两处向量组均印作 (I)，按原文保留。 |
| 37 | 基础题·选择题(6) | 题干末尾多出一个右括号，按原文保留。 |
| 56 | 基础题·填空题(1) | 原文仅给出方程组并要求填写 k，未写明关于解的附加条件；未补写。 |
| 64 | 综合题·选择题(9) D | 等号左边原文未印秩符号 r，按原文保留。 |
| 83 | 基础题·解答题(11) | 第(I)问原文为“计算了”，按原文保留。 |
| 101 | 基础题·选择题(3) | 原文 A、D 两个选项的矩阵相同，按原文保留。 |
| 127 | 拓展题·解答题(4) | 原文第三个变量的下标在 3 前有一个乘点，转写为 x_{\cdot 3}；未擅自删改。 |

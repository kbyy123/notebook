# 导引
## 向量与矩阵
+ 向量：若无说明，所指向量均为列向量．向量的分量数称为向量的**维度**．
+ 矩阵：$m$ 行 $n$ 列的数表，其可以看作 $n$ 个 $m$ 维向量拼在一起．

在本笔记中，用加粗小写字母或希腊字母代表向量，非加粗大写字母代表矩阵，对应的非加粗小写字母代表矩阵的元素，如 $A$ 第 $i$ 行第 $j$ 列的元素为 $a_{ij}$．

如果出现向量未加粗的情况，此时约定行向量为右下角下标+右上角转置，列向量为右上角上标，而仅有右下角下标的为一个数．

!!! warning "注意"

	线性代数中 $m$ 表示行而 $n$ 表示列，这与算法题中的命名习惯是相反的．

### 向量乘积
+ 向量内积：只有维数相同的行向量与列向量才可以内积，结果是对应分量乘积之和．

$$
x^T y \in \mathbb{R} = 
\begin{bmatrix} x_1 & x_2 & \dots & x_n \end{bmatrix}
\begin{bmatrix} y_1 \\ y_2 \\ \vdots \\ y_n \end{bmatrix}
= \sum_{i=1}^{n} x_i y_i
$$

+ 向量外积：任意 $m$ 维列向量与 $n$ 维行向量都可以外积，结果是 $m\times n$ 的秩1矩阵．

$$
xy^T \in \mathbb{R}^{m \times n} = 
\begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_m \end{bmatrix}
\begin{bmatrix} y_1 & y_2 & \dots & y_n \end{bmatrix}
=
\begin{bmatrix}
x_1 y_1 & x_1 y_2 & \dots & x_1 y_n \\
x_2 y_1 & x_2 y_2 & \dots & x_2 y_n \\
\vdots & \vdots & \ddots & \vdots \\
x_m y_1 & x_m y_2 & \dots & x_m y_n
\end{bmatrix}
$$

### 向量与矩阵乘积
+ 矩阵左乘列向量：**行视角**，将矩阵的每一行与列向量内积得到新列向量的一个分量．

$$
Ax = 
\begin{bmatrix}
— & a_1^T & — \\
— & a_2^T & — \\
& \vdots & \\
— & a_m^T & —
\end{bmatrix} x
=
\begin{bmatrix}
a_1^T x \\
a_2^T x \\
\vdots \\
a_m^T x
\end{bmatrix}.
$$

+ 矩阵左乘列向量：**列视角**，矩阵的第 $i$ 列被赋予系数 $x_i$，得到结果是 $A$ 列向量的线性组合．

$$
Ax = 
\begin{bmatrix}
| & | & & | \\
a^1 & a^2 & \dots & a^n \\
| & | & & |
\end{bmatrix}
\begin{bmatrix}
x_1 \\
x_2 \\
\vdots \\
x_n
\end{bmatrix}
= a^1 x_1 + a^2 x_2 + \dots + a^n x_n.
$$

+ 矩阵右乘行向量：**行视角**，矩阵的第 $i$ 行被赋予系数 $x_i$，得到结果是 $A$ 行向量的线性组合．

$$
x^T A = 
\begin{bmatrix} x_1 & x_2 & \dots & x_m \end{bmatrix}
\begin{bmatrix}
— & a_1^T & — \\
— & a_2^T & — \\
& \vdots & \\
— & a_m^T & —
\end{bmatrix}
= x_1 a_1^T + x_2 a_2^T + \dots + x_m a_m^T.
$$

+ 矩阵右乘行向量：**列视角**，将行向量与矩阵的每一列内积得到新行向量的一个分量．

$$
x^T A = x^T
\begin{bmatrix}
| & | & & | \\
a^1 & a^2 & \dots & a^n \\
| & | & & |
\end{bmatrix}
=
\begin{bmatrix}
x^T a^1 & x^T a^2 & \dots & x^T a^n
\end{bmatrix}.
$$

### 矩阵乘积
+ **向量内积**视角：新矩阵每一个元素都是一对向量的内积．

$$
AB = 
\begin{bmatrix}
— & a_1^T & — \\
— & a_2^T & — \\
& \vdots & \\
— & a_m^T & —
\end{bmatrix}
\begin{bmatrix}
| & | & & | \\
b^1 & b^2 & \dots & b^p \\
| & | & & |
\end{bmatrix}
=
\begin{bmatrix}
a_1^T b^1 & a_1^T b^2 & \dots & a_1^T b^p \\
a_2^T b^1 & a_2^T b^2 & \dots & a_2^T b^p \\
\vdots & \vdots & \ddots & \vdots \\
a_m^T b^1 & a_m^T b^2 & \dots & a_m^T b^p
\end{bmatrix}.
$$

+ **向量外积**视角：新矩阵是由向量外积得到的所有秩1矩阵的和．

$$
AB = 
\begin{bmatrix}
| & | & & | \\
a^1 & a^2 & \dots & a^p \\
| & | & & |
\end{bmatrix}
\begin{bmatrix}
— & b_1^T & — \\
— & b_2^T & — \\
& \vdots & \\
— & b_p^T & —
\end{bmatrix}
= \sum_{i=1}^{p} a^i b_i^T .
$$

+ **列视角**：左矩阵分别作用于右矩阵的每一列．

$$
AB = A
\begin{bmatrix}
| & | & & | \\
b^1 & b^2 & \dots & b^n \\
| & | & & |
\end{bmatrix}
=
\begin{bmatrix}
| & | & & | \\
Ab^1 & Ab^2 & \dots & Ab^n \\
| & | & & |
\end{bmatrix} .
$$

+ **行视角**：右矩阵分别作用与左矩阵的每一行．

$$
AB = 
\begin{bmatrix}
— & a_1^T & — \\
— & a_2^T & — \\
& \vdots & \\
— & a_m^T & —
\end{bmatrix} B
=
\begin{bmatrix}
— & a_1^T B & — \\
— & a_2^T B & — \\
& \vdots & \\
— & a_m^T B & —
\end{bmatrix}.
$$

## 线性方程组
未知数最高次数为一次的方程组称为线性方程组．线性代数只研究线性方程组．线性方程组可以看作矩阵与向量的乘积．
例如，线性方程组

$$
\begin{cases}
x_{1}\,\,\,-2x_{2}=1 \\
3x_{1}+2x_{2}=11
\end{cases}
$$

可以看作是

$$
\begin{bmatrix}
 1 & -1 \\
 3 & 2 
\end{bmatrix}
\cdot
\begin{bmatrix}
 x_{1}  \\
 x_{2}  
\end{bmatrix} 
=
\begin{bmatrix}
 1 \\
 11 
\end{bmatrix}
$$

即 $A\boldsymbol{x=b}$．
### 视角
对于线性方程组的矩阵形式 $A\boldsymbol{x=b}$，我们可以从三个视角看待．

+ 从 $A$ 的各行与 $\boldsymbol{x}$ 看：参考[行视角](#_4)．
+ 从 $A$ 的各行与 $\boldsymbol{x}$ 看：参考[列视角](#_4)．
<!-- + 从 $A$ 的各行与 $\boldsymbol{x}$ 看： $A$ 含有 $m$ 个行向量，每一个行向量有 $n$ 个分量；$\boldsymbol{x}$ 为 $n$ 维列向量，其与 $A$ 的行向量分量数相对应；$\boldsymbol{b}$ 有 $m$ 个分量，其第 $i$ 个分量为 $A$ 的第 $i$ 行与 $\boldsymbol{x}$ 的点积．该视角被称为**行视角**．
+ 从 $A$ 的各行与 $\boldsymbol{x}$ 看：$A$ 含有 $n$ 个列向量，$\boldsymbol{x}$ 有 $n$ 个分量，$A\boldsymbol{x}$ 可以看作是 $A$ 的第 $i$ 列被赋予系数 $x_i$，从而得到 $A$ 列向量的线性组合，线性组合的结果为 $b$．该视角被称为**列视角**，也是老师最推荐的视角． -->
+ 从 $A$ 的整体与 $\boldsymbol{x}$ 看：$A$ 刻画了一种线性变换规则，其将一个 $n$ 维向量转化为 $m$ 维向量．如果这个变换过程是可逆的，那么 $A^{-1}$ 对应的就是将得到的 $m$ 维向量转化为原来的 $n$ 维向量的过程．

特别地：在低维度下，我们可以将行视角在坐标系中表示：

+ 如 $n=2$ 时，每一个点积都对应一个二元一次方程，我们很容易就可以在平面直角坐标系中画出图像，而图像的交点就是方程组的解，即 $\boldsymbol{x}$；
+ 或 $n=3$ 时，每一个点积都对应一个平面方程，多个平面的交点就是方程组的解．

!!! info "补充"

	矩阵乘以列向量可以看作是矩阵各列向量的线性组合；同理，行向量乘以矩阵可以看作是矩阵各行向量的线性组合．
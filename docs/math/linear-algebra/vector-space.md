# 向量空间
## 向量空间
$n$ 维实列向量构成的全体向量集合称为向量空间 $\mathbb{R}^{n}$．这是狭义上的定义，广义的向量空间定义为任何满足加法与数乘封闭性的空间，如实多项式空间 $\mathbb{P}^{n}$、复向量空间 $\mathbb{C}^{n}$、二维矩阵空间等．

本章节默认谈论的向量与矩阵均为实向量、实矩阵．

向量空间的本质特征是对加法和数乘封闭．对于空间内的任意的元素 $\boldsymbol{u},\boldsymbol{v}$，其必须满足：对于任意实数 $\lambda,\mu$，$\lambda\boldsymbol{u}+\mu\boldsymbol{v}$ 仍然在该向量空间内．

具体而言，向量空间需要满足如下八条定律

1. 满足加法交换律： $\boldsymbol{x}+\boldsymbol{y}=\boldsymbol{y}+\boldsymbol{x}$
2. 满足加法结合律： $(\boldsymbol{x}+\boldsymbol{y})+\boldsymbol{z}=\boldsymbol{x}+(\boldsymbol{y}+\boldsymbol{z})$
3. 存在加法单位元 $\boldsymbol{0}$ 使得对任意元素 $\boldsymbol{x}$：$\boldsymbol{x}+boldsymbol{0}=\boldsymbol{x}$
4. 对任意元素 $\boldsymbol{x}$ 存在加法逆元 $-\boldsymbol{x}$：$\boldsymbol{x}+(-\boldsymbol{x})=boldsymbol{0}$
5. 对在乘法单位元 $1$ 使得对任意元素 $\boldsymbol{x}$：$1\cdot \boldsymbol{x}=\boldsymbol{x}$
6. 满足数乘结合律：$(c_{1}c_{2})\boldsymbol{x}=c_{1}(c_{2}\boldsymbol{x})$
7. 满足向量分配律：$c(\boldsymbol{x}+\boldsymbol{y})=c\boldsymbol{x}+c\boldsymbol{y}$
8. 满足标量分配律：$(c_{1}+c_{2})\boldsymbol{x}=c_{1}\boldsymbol{x}+c_{2}\boldsymbol{x}$

显然，一个向量空间必须包含零元．
## 子空间
子空间是特定向量空间的一个子集，子空间也必须满足上述八条性质．

对于向量空间 $\boldsymbol{V}$ 中给定的有限向量集合 $S$，其本身因有限集特性必然不能称为 $\boldsymbol{V}$ 的子空间；将 $S$ 内所有向量的所有线性组合构成一个无限集 $SS$，则 $SS$ 是 $\boldsymbol{V}$ 的一个子空间．

!!! warning "注意"

	子空间本质上是向量空间，但要注意其所在的维度．如由 $\boldsymbol{u}=(1,0,0)^{T}$ 与 $\boldsymbol{v}=(0,1,0)^{T}$ 的所有线性组合形成的子空间是三维空间中的一个平面，其为 $\mathbb{R}^{3}$ 的一个子空间而不是向量空间 $\mathbb{R}^{2}$．我们可以先直观地感受出该子空间的维数是二维，关于维数后文有更严谨的定义．

## 列空间
对于一个 $m\times n$ 的矩阵 $A$，其列向量在 $\mathbb{R}^{m}$ 中．其 $n$ 个列向量可以通过线性组合得到一个 $\mathbb{R}^{m}$ 的子空间，这个子空间称为 $A$ 的列空间，记作 $\boldsymbol{C}(A)$．由于其是由有限向量的所有线性组合构成的无限向量集，因此其合法性必然成立．

线性方程组本质就是列向量的线性组合，因此若 $\boldsymbol{b}\in \boldsymbol{C}(A)$，该方程有解，反之无解．

!!! warning "行变换会改变列空间"

	以
	
	$$
	A=
	\begin{bmatrix}
	 1 & 2 \\
	 1 & 2 
	\end{bmatrix}
	\implies R=\begin{bmatrix}
	 1 & 2 \\
	 0 & 0 
	\end{bmatrix} 
	$$
	
	为例，显然 $\boldsymbol{C}(A)$ 为终点在 $y=x$ 上的所有向量，$\boldsymbol{C}(R)$ 为终点在 $x$ 轴上的所有向量，列空间不一致．

## 零空间
满足 $A\boldsymbol{x}=\boldsymbol{0}$ 的所有解向量 $\boldsymbol{x}$ 构成一个集合 $\boldsymbol{N}(A)$，称为 $A$ 的零空间．显然零空间中的向量在 $\mathbb{R}^{n}$ 中．接下来检查零空间是否为 $\mathbb{R}^{n}$ 的一个子空间：

+ 包含零向量：$A\cdot \boldsymbol{0}=\boldsymbol{0}$．
+ 符合加法封闭性：若 $A\boldsymbol{u}=\boldsymbol{0}$ 且 $A\boldsymbol{v}=\boldsymbol{0}$，则 $A(\boldsymbol{\lambda u+\mu v})=\lambda A\boldsymbol{u} + \mu A\boldsymbol{v}=\boldsymbol{0}$，仍然在零空间内．
+ 符合数乘封闭性：若 $A\boldsymbol{u}=\boldsymbol{0}$，则 $A(c\boldsymbol{u})=cA\boldsymbol{u}=c\cdot\boldsymbol{0}=0$．

因此，零空间是 $\mathbb{R}^{n}$ 的一个子空间．

与列空间不同，行变换相当于方程组消元操作，该过程不会改变方程组 $A\boldsymbol{x}=\boldsymbol{0}$ 的解，即不会改变矩阵的零空间．

### 求解
由于行变换不会改变零空间，我们可以用 Gauss-Jordan 消元将矩阵消元得到简化行阶梯形矩阵 $R=\text{rref}(A)$，接着解方程 $R\boldsymbol{x}=\boldsymbol{0}$ 通过求零空间的**特殊解**（special solutions，与之后的特解 particular solutions 不同），通过线性组合得到整个零空间．

$\text{rref}$ 中的主元数就是矩阵的**秩** $r$，它代表了多少个有效方程组．对于 $n$ 个变量，其自由度为 $n$，当有 $r$ 个有效方程将其约束时，其自由度减少为 $n-r$，也就是说该方程组只要确定 $n-r$ 个变量，剩下 $r$ 个就会自动确定．

为了方便求解，我们可以直接将主元所在列视为**约束变量**，非主元所在列视为**自由变量**（因为主元的系数为 $1$，自由变元确定后只需移项即可解得主元变量）．也就是说一共有 $n-r$ 个自由变量，为了让这 $n-r$ 个自由变量对应的特殊解向量在零空间中线性无关，我们可以对第 $i$ 个特殊解向量的第 $i$ 个自由变元取 $1$ 而其他自由变元取 $0$．

此时我们会得到 $n-r$ 个线性无关的特殊解向量，我们可以用这 $n-r$ 个向量张成 $\mathbb{R}^N$ 空间的一个 $n-r$ 维子空间，得到零空间中的所有向量．

???+ example

	$$
	R=\begin{bmatrix}
	 1 & 0 & a & 0 & c \\
	 0 & 1 & b & 0 & d \\
	 0 & 0 & 0 & 1 & e \\
	 0 & 0 & 0 & 0 & 0 
	\end{bmatrix}
	$$
	
	其有三个主元，$r=3$，自由变量数为 $n-r=5-3=2$，为 $x_{3}$ 和 $x_{5}$；为了求解零空间，我们分别取
	
	$$
	\begin{cases}
	x_{3} = 1 \\   
	x_{5}=0
	\end{cases}
	\quad
	\begin{cases}
	x_{3} = 0 \\   
	x_{5}=1
	\end{cases}
	$$
	
	得到两个特殊解向量 $\boldsymbol{s_1}=(-a, -b, 1, 0,0)^{T}$ 与 $\boldsymbol{s_2}=(-c,-d,0,-e,1)^{T}$，即为零空间中两个基向量．
	
	!!! quote "简便求法"
		由于我们每次只将一个自由变元设置为非 $0$ 值，以 $x_{3}=1$ 为例，我们将所有主元列移到左边而自由列移到右边
		
		$$
		x_{1}\begin{bmatrix}
		 1 \\
		 0 \\
		 0  \\
		 0
		\end{bmatrix}+x_{2}\begin{bmatrix}
		 0 \\
		 1 \\
		 0  \\
		 0
		\end{bmatrix} + x_{4}\begin{bmatrix}
		 0 \\
		 0 \\
		 1  \\
		 0
		\end{bmatrix}
		=-x_{3}\begin{bmatrix}
		 a \\
		 b \\
		 0 \\
		 0 
		\end{bmatrix}
		$$
		
		显然这三个主元取的值就是自由变元列从上到下的分量的相反数．对于所有自由变元都是如此．

## $A\boldsymbol{x=b}$ 的全解
### 增广行阶梯形
在之前的讨论中，由于右侧为 $0$ 向量，因此不用考虑行变换对其影响；此处我们讨论 $A\boldsymbol{x=b}$ 的解，$\boldsymbol{b}$ 会被行变换改变，因此我们需要对增广矩阵 $[A,\boldsymbol{b}]$ 同时做行变换得到矩阵 $[R,\boldsymbol{b}]$．

> 此处我们可以提前判断是否有解：在 $[R,\boldsymbol{d}]$ 中，若存在一行使得 $R$ 中该行元素全为 $0$ 而 $\boldsymbol{d}$ 的该分量不为 $0$，此时任何线性组合都无法得到 $\boldsymbol{d}$，方程组无解．

### 特解
我们尝试寻找 $R\boldsymbol{x=d}$ 的一个特解 $\boldsymbol{x_{p}}$（particular solutions）．由于自由变元的取值不影响解的存在性（后文会解释），因此不妨将其全部设为 $0$．解出此时的 $\boldsymbol{x_{p}}$．接着利用其零空间得到所有解 $\boldsymbol{x}=\boldsymbol{x_{n}+x_{p}}$．

???+ example "例"

	$$
	R=\begin{bmatrix}
	 1 & 3 & 0 & 2 \\
	 0 & 0 & 1 & 4 \\
	 0 & 0 & 0 & 0 
	\end{bmatrix}
	\quad
	\boldsymbol{d}=\begin{bmatrix}
	 1 \\
	 6 \\
	 0 
	\end{bmatrix}
	$$
	
	将 $x_{2}$ 与 $x_{4}$ 取为 $0$，解得 $\boldsymbol{x_{p}}=(1,0,6,0)^{T}$（此处可以参考上文零空间的简便求法，主元取值就是 $\boldsymbol{d}$ 的前 $r$ 行值）．由于零空间基向量为 $\boldsymbol{s_{1}}=(-3,1,0,0)^{T}$ 与 $\boldsymbol{s_{2}}=(-2,0,-4,1)^{T}$，因此特解为 
	
	$$
	\begin{aligned}
	\boldsymbol{x}&=\boldsymbol{x_{p}}+x_{2}\boldsymbol{s_{1}}+x_{4}\boldsymbol{s_{2}} \\
	&=\begin{bmatrix}
	 1 \\
	 0 \\
	 6 \\
	 0 
	\end{bmatrix}+x_{2}\begin{bmatrix}
	 -3 \\
	 1 \\
	 0 \\
	 0 
	\end{bmatrix}
	+x_{4}\begin{bmatrix}
	 -2 \\
	 0 \\
	 -4 \\
	 1 
	\end{bmatrix}
	\end{aligned}
	$$

### 全解性证明
先证明所有 $\boldsymbol{x}=\boldsymbol{x_{n}+x_{p}}$ 均为 $A\boldsymbol{x=b}$ 的解：

$$
A(\boldsymbol{x_{n}+x_{p}})=A\boldsymbol{x_{n}}+A\boldsymbol{x_{p}}=\boldsymbol{0}+\boldsymbol{b}=\boldsymbol{b}
$$

得证．

在证明所有 $A\boldsymbol{x=b}$ 的解 $\boldsymbol{x}$ 均可被 $\boldsymbol{x_{n}+x_{p}}$ 表示：

由于 $A\boldsymbol{x=b}$，考虑 $A(\boldsymbol{x-x_{p}})=A\boldsymbol{x}-A\boldsymbol{x_{p}}=\boldsymbol{b-b}=\boldsymbol{0}$，因此所有解减去特解后必定落在零空间上，而我们的 $x_{n}$ 表示的是零空间中的所有向量，因此解向量必然已经被我们所表示．

综上，我们得到的解即为原方程组 $A\boldsymbol{x=b}$ 的解．

!!! warning "注意"

	与零空间、列空间不同，$A\boldsymbol{x=b}$ 的解空间在 $\boldsymbol{b\ne0}$ 时并不是一个向量空间，因为其不含有零元 $0$．其解空间是零空间在特解向量上的一个偏移．

此时上方的问题”自由变元取值不影响解的存在性“就显然了：如果解存在，由于全解需要加上整个零空间，自由变元自然可以取遍所有值；而如果解不存在，自由变元取任何值都无法得到目标向量．
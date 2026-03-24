# Random Variables
## 随机变量
**随机变量**是一种以概率方式取值的变量．一般用大写字母 $X,Y,Z$ 来表示随机变量，而用 $E,F,G$ 来表示事件．

当随机变量被赋予或限定了特定的范围，其成为了事件．如 $X=2$，$Y<5$ 等．

## 离散随机变量
若一个随机变量有有限个可能取值，我们称其为离散随机变量．
### 概率密度函数
**概率质量函数**（Probability Mass Funtion）是离散随机变量在各特定取值上的概率函数．

我们通常用 $\text{P}(X=x)$ 来表示随机变量 $X$ 的PMF，有时也会简写为 $\text{P}(x)$．

???+ example "例"

	对于随机变量 $X$：掷一次骰子的点数，其PMF为
	
	$$
	P(X=x)=\dfrac{1}{6} \quad \text{if }x\in \mathbb{Z}, 1\le x\le 6
	$$

显然对于PMF，有 $\sum_{x}P(X=x)=1$，其中 $x$ 为随机变量 $X$ 的所有可能取值．

### 期望
随机变量 $X$ 所有可能取到的值与该值对应出现概率的加权平均称为随机变量 $X$ 的期望，记作 $\text{E}[X]$．

$$
\text{E}[X]=\sum_{x}x\cdot \text{P}(X=x) 
$$

期望具有如下性质：

+ 线性性：$\text{E}[aX+b]=a\text{E}[X]+b$，$\text{E}[X+Y]=\text{E}[X]+\text{E}[Y]$．（不管 $X,Y$ 具有何种关系）
+ 无意识统计学家法则（LOTUS）：$\text{E}[g(X)]=\sum_xg(x)\text{P}(X=x)$．

### 方差
方差是用来衡量随机变量离散程度的指标．对于期望为 $\text{E}[X]=\mu$ 的随机变量 $X$，其方差定义为 

$$
\text{Var}(X)=\text{E}[(X-\mu)^{2}]
$$

该计算可以被简化：

$$
\begin{aligned}
\text{Var}(X)&=\text{E}[(X-\mu)^{2}]\\
&=\sum_x(x-\mu)^{2}\text{P}(X=x)\\
&=\sum_{x} (x^{2}-2\mu x+\mu ^{2})\text{P}(X=x)\\
&=\sum_{x} x^{2}\text{P}(X=x)-2\mu \sum_{x} x\text{P}(X=x)+\mu^{2}\sum_x \text{P}(X=x) \\
&=\text{E}[X^{2}]-2\text{E}^{2}[X]+\text{E}^{2}[X]\\
&=\text{E}[X^{2}]-\text{E}^{2}[X]
\end{aligned}
$$

方差具有以下性质：

+ 线性变换的方差：$\text{Var}(aX+b)=a^{2}\text{Var}(X)$．
+ 若 $X,Y$ 为独立随机变量：$\text{Var}(X+Y)=\text{Var}(X)+\text{Var}(Y)$．

### 标准差
方差的单位是原单位的平方，为了让单位变回原来的单位，我们将方差开根号得到标准差：$\text{Std}(X)=\sqrt{\text{Var}(X)}$．

### 伯努利随机变量
 伯努利随机变量是一个布尔变量，其取值只有 $1$ 或 $0$，概率分别为 $p$ 与 $1-p$．如果 $X$ 服从伯努利分布，则记作 $X\sim \text{Ber}(p)$．

**离散PMF**：

$$
\text{P}(X=x)= \begin{cases}p \,\,\qquad x=1, \\
1-p\,\,\,\,x=0.
\end{cases}
$$

**连续PMF**：$\text{P}(X=x)=p^{x}(1-p)^{1-x}$．

**期望**：$\text{E}[X]=p$．

**方差**：$\text{Var}(X)=p(1-p)．$

???+ quote "伯努利分布期望与方差证明"

	期望：
	
	$$
	\begin{aligned}
	\text{E}[X]&=\sum_x x\cdot \text{P}(X=x)\\
	&= 1\cdot p+0\cdot(1-p)\\
	&=p
	\end{aligned}
	
	$$
	
	方差：
	
	$$
	\begin{aligned}
	\text{E}[X^{2}]&=\sum_x x^{2}\cdot \text{P}(X=x)\\&=1^{2}\cdot p+0^{2}\cdot(1-p)\\
	&=p\\\\
	\text{则 } \text{Var}(X)&=\text{E}[X^{2}]-\text{E}^{2}[X]\\&=p-p^{2}\\&=p(1-p)
	\end{aligned}
	$$

### 二项分布
在 $n$ 次独立重复试验中，每次试验都有 $p$ 的概率成功，则这一系列试验称为 $n$ 重伯努利试验．设 $X$ 为 $n$ 次实验中的成功次数，则 $X$ 服从**二项分布**，记作 $X\sim \text{Bin}(n,p)$．

**PMF**：

$$
\text{P}(X=k) =\binom{n}{k}p^{k}(1-p)^{n-k},k=0,1,2,\cdots, n
$$

**期望**：$\text{E}[X]=n\cdot p$．

**方差**：$\text{Var}(X)=n\cdot p(1-p)$．

??? example "二项分布的应用"

	一场七局四胜的比赛，必须比完七场，我方球队每局胜率为 $p=0.55$，则总胜率为？
	
	显然答案为
	
	$$
	\text{P(win)}=\sum_{k=4}^{7}\binom{7}{k}(0.55)^{k}(1-0.55)^{7-k} 
	$$
	
	我们用Python得到答案：
	
	```python
	from scipy import stats
	
	def binomial():  
	    n = 7  
	    p = 0.55  
	    win = sum(stats.binom.pmf(i, n, p) for i in range(4, n + 1))  
	    return win # 0.608287796875
	```
	
	如果出现某一方球队打赢了四场，那么直接判该球队获胜而不进行后续比赛，此时我方胜率又为多少？
	
	此时仍然为上述答案．因为当一方球队赢下四场后，后续单场比赛结果都不影响最终的结果，我们可以将后面的比赛当作是全概率公式的事件划分，其事件总和为样本空间而每一个情况的最终结果都是同一支队伍获胜，因此后续比赛的概率累计和为 $1$ 且贡献给同一支队伍，不影响结果．
	
	实际上，如果我们使用**负二项分布**计算，即准确在第 $k$ 场赢下第四场，则胜率为
	
	$$
	\text{P(win)} = \sum_{k=4}^{7} \binom{k-1}{3} p^4 (1-p)^{k-4}
	$$
	
	```python
	def negative_binomial():  
	    n = 7  
	    p = 0.55  
	    # nbinom.pmf(k, n, p) 中，k 为失败次数，n 为需要达到的成功次数  
	    win = sum(stats.nbinom.pmf(i - 4, 4, p) for i in range(4, n + 1))  
	    return win # 0.608287796875
	```
	
	这与我们使用二项分布计算的结果一样．

???+ quote "二项分布期望与方差证明"

	不妨设 $Y$ 为成功概率为 $p$ 的伯努利变量，$Y_{i}$ 表示第 $i$ 次试验是否成功，即 $Y_{i}\sim \text{Ber}(p)$．
	
	期望：
	
	$$
	\begin{aligned}
	\text{E}[X]&=\text{E}\left[ \sum_{i=1}^{n}Y_{i}  \right] \\
	&=\sum_{i=1}^{n}\text{E}[Y_{i}]\\
	&=\sum_{i=1}^{n}p\\
	&=n\cdot p
	\end{aligned}
	$$
	
	方差：由于各次试验相互独立
	
	$$
	\begin{aligned}
	\text{Var}(X)&=\sum_{i=1}^{n}\text{Var}(Y_{i}) \\
	&=\sum_{i=1}^{n}p(1-p) \\
	&=n \cdot p(1-p)
	\end{aligned}
	$$


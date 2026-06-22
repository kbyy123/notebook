# The Information Theory

## Amount of Information

*Def*. 事件发生的信息量大小，满足：

+ 小概率事件有更大的信息量
+ 独立事件的积事件信息量等于事件信息量的和，即 $I(AB)=I(A)+I(B)$

符合条件的定义信息量为 $I(x):=-\log_2p_x$．

## Entropy

*Def*. 概率分布 $p$ 的信息量期望 

$$
H(p):=E(I(x))=\sum p_i I^p_i=-\sum p_i\log_2 p_i
$$

用于评估概率模型的不确定性，不确定性越大熵越大；概率密度均匀则不确定性大、熵也大．

## Cross Entropy

*Def*. 预测概率分布 $q$ 对真实概率分布 $p$ 的平均信息量估计
$$
H(p,q)=\sum p_iI_i^q=-\sum p_i\log_2 q_i
$$

吉布斯不等式可以证明，交叉熵 $H(p,q)$ 总是大于等于熵 $H(p)$ 的值；概率分布越接近交叉熵越小，当 $p,q$ 为相同概率分布时交叉熵最小，为熵的值．

## KL Divergence

*Def*. KL 散度用于衡量两个概率分布的相对差异，预测概率分布 $q$ 对真实概率分布 $p$ 的平均信息量差值估计
$$
\begin{aligned}
D_{KL}(p\|q)&=\sum p_i[I_q-I_p]\\
&=H(p,q)-H(p)\\
&= \sum p_i \log_2(p_i / q_i)
\end{aligned}
$$

由交叉熵可知 $D(p\|q)\ge 0$，当且仅当 $p,q$ 相同分布时取等．

**注意**：$D(p\|q)\ne D(q\|p)$，括号内前者为真实概率分布后者为估计概率分布

## Cross Entropy Loss

*Def*. KL 散度能衡量两个概率分布的相对差异，可以直接将损失函数定义为 KL 散度

$$
\text{Loss}=D(p\|q)=H(p,q)-H(p)=\sum p_i\log_2p_i - \sum p_i\log_2q_i
$$

对于分类问题，真实分布是一个单点分布，即错误类别 $p_i=0$，而正确类别 $p_i=1$ 又有 $\log_2p_i=0$，故前项被消去，后项剩下 $-\log_2q_j$，其中 $q_j$ 为正确类别预测概率． 

对于二分类问题，由于知道其中一个预测概率就知道另一个，所以二分类常只输出一个 $p$，表示预测标签为 1 的概率（二分类是标签一般选择 1 与 0）．因此，如果真实标签为 1，损失即为 $-\log_2p$；如果真实标签为 0，等价于以 $1-p$ 概率预测标签为 0， 损失为 $-\log_2(1-p)$．即

$$
\text{CE}(p,y)=
\begin{cases}
-\log p \qquad \quad\text{if }y=1\\
-\log(1-p)\ \  \text{otherwise.}
\end{cases}
$$

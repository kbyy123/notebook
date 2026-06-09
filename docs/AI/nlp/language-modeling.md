# Language Modeling

语言模型关注 sequences 上的概率分布．它既可以用于评价一段文本出现的可能性，也可以用于生成新序列．

语言模型常见用途：

+ Score sequences
+ Classify text
+ Generate sequences（& Conditional generation：如机器翻译）

Auto-regressive Language Models：

$$
P(X)=\prod_{t=1}^TP(x_t|x_1,\dots, x_{t-1})
$$

## Gram Models

### Bigram Models

Bigram model 只使用前一个 token 作为上下文：

$$
P(X)\approx \prod_{t=1}^T p_{\theta}(x_t| x_{t-1})
$$

转化为对数：

$$
\log P(X)\approx \sum_{t=1}^{T}\log p_{\theta}(x_t|x_{t-1})
$$

在训练集中进行计数，得到概率：

$$
p(x_t| x_{t-1})=\frac{\text{count}(x_{t-1},x_t)}{\sum_{x'}\text{count}(x_{t-1},x')}
$$

生成时，根据当前字符，用 multinomial（按概率随机抽样）生成下一个 token．

### N-gram Models

类似 bigram，只是上下文变成 $n - 1$ 个 token．问题是 n 大了以后，很多上下文在训练集根本没出现过，导致概率为 0．

于是引入 smoothing（概率总和还是 1，于是分母加上 $|V|$）：

$$
p(x_t \mid c)
=
\frac{1+\operatorname{count}(c,x_t)}
{|V|+\sum_{x'}\operatorname{count}(c,x')}
$$

### Evaluation

对生成结果进行评估：

+ Log-likelihood：越大越好，也就是生成的文本概率越高越好．

$$
LL(X_{\mathrm{test}})=\sum_{X \in X_{\mathrm{test}}}\log P(X)
$$

长度不同，则需要对 token 求平均：Per-word Log likelihood．

$$
WLL(X_{\mathrm{test}})
=
\frac{1}{\sum_{X \in X_{\mathrm{test}}}|X|}
\sum_{X \in X_{\mathrm{test}}}\log P(X)
$$

+ Perplexity：困惑度，越低越好．

$$
PPL(X_{\mathrm{test}})
=
e^{-WLL(X_{\mathrm{test}})}
$$

## RNN Language Models

使用前馈神经网络来计算条件概率，可以把相似的词学习到接近的词向量，这是 n-gram 做不到的．同时，基于 [RNN](../dl/recurrent-neural-networks.md) 的序列建模可以实现长距离依赖．

在 RNN 语言模型中，模型读入一个 token 后更新 hidden state，再根据当前 hidden state 预测下一个 token．

<div style="text-align: center; margin-top: 15px;">
<img src="language-modeling.assets/image-20260525164225677.png" alt="image-20260525164225677" style="zoom:50%;" />
</div>

> RNN 语言模型训练时和测试时采用不同的方式
>
> + 训练时：每一个输入对应一个输出，一般而言输入序列为 `<BOS>` + 原序列，输出序列为 原序列 + `<EOS>`，偏移一位；同时训练时即使输出错误，也只用于计算 loss 而不会用错误的输出继续往下计算；这种训练方式称为 Teacher Forcing．
> + 测试时：测试时不会提前给出正确的输出序列，如果一次输出错误，它就会接着这个错误的输出继续生成．

    !!! info "Sequence-to-Sequence Models"

    语言模型通常根据已有上下文预测下一个 token，而 Seq2Seq 更关心“把一个完整序列转换为另一个完整序列”，例如机器翻译、摘要生成等任务．如果输入序列和输出序列都是长度可变的，一般用 “Encoder-Decoder” 架构．

    **RNN Encoder:**

    编码器把长度可变的输入序列转换成形状固定的上下文变量 $c$，并传入到解码器中．即通过

    $$
    c=q(h_1,\dots,h_t)
    $$

    将所有时间步的隐状态转化为上下文变量．常直接取 $c=h_t$．

    **RNN Decoder：**

    解码器也是一个 RNN，其在时间步 $t$ 时，将来自上一时间步的输出 $y_{t-1}$、上下文变量 $c$、上一隐状态 $s_{t-1}$ 作为输入，转化为新隐状态 $s_t$，即

    $$
    s_t=g(y_{t-1},s_{t-1},c)
    $$

    <div style="text-align: center; margin-top: 15px;">
    <img src="language-modeling.assets/image-20260525230537232.png" alt="image-20260525230537232" style="zoom:33%;" />
    </div>


## Transformer Language Models

基于 Attention 的 Encoder-Decoder 会进一步缓解固定上下文变量的信息瓶颈，具体见 [Transformer](../dl/attention-and-transformer.md)．
# LLM Architecture

现代大语言模型大多基于 Transformer．基础 Attention、Self-Attention 与 Encoder-Decoder Transformer 放在 [Attention and Transformer](../dl/attention-and-transformer.md) 中；这里主要记录 GPT、LLaMA 一类自回归语言模型常用的 Decoder-only Transformer 结构．

<img src="llm-architecture.assets/image-20260605111419930.png" alt="image-20260605111419930" style="zoom: 38%;" />

## Decoder-only Transformer

Decoder-only Transformer 使用 causal mask，使每个位置只能看到它之前的 token，因此天然适合自回归语言建模：

$$
P(X)=\prod_{t=1}^{T}P(x_t|x_1,\dots,x_{t-1})
$$

它通常由多层相同结构堆叠而成，每层包含：

+ masked self-attention
+ feed-forward network / MLP
+ residual connection
+ normalization

## LLaMA

|              | Vaswani et al. | LLaMA | LLaMA 2 |
| ------------ | -------------- | ----- | ------- |
| Norm Position | Post | Pre | Pre |
| Norm Type | LayerNorm | RMSNorm | RMSNorm |
| Non-linearity | ReLU | SwiGLU | SwiGLU |
| Positional Encoding | Sinusoidal | RoPE | RoPE |
| Attention | Multi-head | Multi-head | Grouped-query |

这张表保留的是架构上的粗略对比．实际模型会因规模和版本而有差异，例如 grouped-query attention 并不是所有 LLaMA 2 尺寸都完全相同．

### Rotary Positional Encodings

Rotary Positional Encoding（RoPE）把位置信息编码为向量空间中的旋转操作，使 attention score 同时包含 token 内容和相对位置信息．相比绝对位置向量相加，RoPE 更适合自回归模型处理相对位置关系．

### Pre-Norm

Pre-Norm 指在 attention 或 MLP 子层之前做 normalization．相比 Post-Norm，它通常让深层 Transformer 的训练更加稳定．

### RMSNorm

RMSNorm 是 LayerNorm 的变体，只使用均方根进行归一化，不减均值，因此计算更轻量．LLaMA 系列使用 RMSNorm 替代标准 LayerNorm．

### Grouped-Query Attention

Grouped-Query Attention（GQA）介于 Multi-Head Attention 和 Multi-Query Attention 之间：多个 query head 共享较少数量的 key/value head，从而减少推理时 KV cache 的存储和带宽开销．

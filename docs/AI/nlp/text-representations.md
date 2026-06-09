# Text Representations

文本模型无法直接处理自然语言字符串，因此通常先把文本切分为 token，再把 token 映射为向量表示．

## Word-Level Representations

### Token

在处理文本时，计算机并不能直接理解文本的含义，因此我们需要和图像一样把文本处理成张量数据。**token** 是模型处理文本的最小单位，可以是字母、字符、单词等。以字母为例，我们可以将 "hello" 切成四个 token 形成词表 $[h,e,l,o]$，每个 token 对应一个 id。

### One-hot Vector

one-hot 是把一个 token id 表示为长度为 $V$ 的向量，其中 $V$ 是词表大小；该向量只有对应位置为 1，其余位置为 0。如 "hello" 对应词表 $[h,e,l,o]$ 的 one-hot vector 为：

```python
# shape = (n, V), n is number of tokens
[[1, 0, 0, 0]
 [0, 1, 0, 0]
 [0, 0, 1, 0]
 [0, 0, 1, 0]
 [0, 0, 0, 1]]
```

### Embedding

由于不同 token 之间的*距离*不同，如 dog 与 cat 的距离一定比与 blackboard 更近，而只使用 one-hot 无法体现距离，因此需要将每一个 token 抽象为一个 $D$ 维向量，词表变成一个 $E\in \mathbb{R}^{V\times d}$ 的矩阵（如 $50000\times 512$），称为 **embedding**（嵌入层）．当 token id = $i$ 时，直接取 $E[i]$ 即为 token 对应的向量．

> Embedding 可以在训练中学习，例如学习到 dog 与 cat 的距离相近．

## Sequence‑level representation

### Bag of Words

Bag of Words（BoW）：对一个 sequence，将所有 token 的 one-hot 向量相加，得到出现频率向量，将文本向量化．

这种表示忽略 token 顺序，只保留“出现了什么”和“出现了多少次”。它简单、可解释，但很难表达上下文和语义相似性．

### CBoW

CBoW：改用 token 词向量表示而非 one-hot．

相比 one-hot，词向量是可学习的稠密表示，模型可以把相似语义或相似上下文中的 token 学到比较接近的位置．

### Deep CBoW

Deep CBoW：CBoW + MLP．

可以把多个上下文词向量汇聚后输入 MLP，用更强的非线性函数学习文本表示．
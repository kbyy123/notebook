# Text Representations

文本模型无法直接处理自然语言字符串，因此通常先把文本切分为离散单位．

## Token

在处理文本时，计算机并不能直接理解文本的含义，因此我们需要和图像一样把文本处理成张量数据．**token** 是模型处理文本的最小单位，可以是字母、字符、单词等．以字母为例，我们可以将 "hello" 切成四个 token 形成词表 $[h,e,l,o]$，每个 token 对应一个 id；或者是单词，如 `I love deep learning` 切分成 `["I", "love", "deep", "learning"]` 并映射成整数 ID．将文本切分成 token 的过程叫 tokenize，切分的工具一般称为 tokenizer．

## One-hot Vector

one-hot 是把一个 token id 表示为长度为 $V$ 的向量，其中 $V$ 是词表大小；该向量只有对应位置为 1，其余位置为 0。如 "hello" 对应词表 $[h,e,l,o]$ 的 one-hot vector 为：

```python
# shape = (n, V), n is number of tokens
[[1, 0, 0, 0]
 [0, 1, 0, 0]
 [0, 0, 1, 0]
 [0, 0, 1, 0]
 [0, 0, 0, 1]]
```

## Bag of Words

Bag of Words（BoW）属于 sequence-level representation：对一句话 / 一段文本，将所有 token 的 one-hot 向量相加，得到出现频率向量，将文本向量化．

这种表示忽略 token 顺序，只保留“出现了什么”和“出现了多少次”。它简单、可解释，但很难表达上下文和语义相似性．

## TF-IDF

TF-IDF 也属于 sequence-level sparse text representation，即把一整段文本、一个句子、一篇文档表示成一个高维稀疏向量．其核心是：一个词 $t$ 在当前文档 $d$ 里出现越多越重要；但如果在很多文档里都出现，重要性就要被降低．

TF：Term Frequency 词频，衡量这个词在当前文档出现频率．若 $t$ 在 $d$ 出现次数为 $\text{count}(t,d)$，$d$ 总词数为 $\sum_{t' \in d}\text{count}(t',d)$，则

$$
\text{TF}(t,d)=\frac{\text{count}(t,d)}{\sum_{t' \in d}\text{count}(t',d)}
$$

IDF：Inverse Document Frequency 逆文档频率，表示这个词在整个语料是否稀有．设语料库共有 $N$ 篇文档，包含词 $t$ 的文档数量是 $\text{df}(t)$，则

$$
\text{IDF}(t)=\log\frac{N}{\text{df}(t)}
$$

或者使用平滑版本，防止除以 0 或者数值过于极端

$$
\text{IDF}(t)=\log\frac{N+1}{\text{df}(t)+1}+1
$$

TF-IDF 还是一个 $|V|$ 维度的向量，表示一篇文章中所有词的频率，每一个词的 TF-IDF 的值都是在这篇文章中 TF 值与 IDF 值乘积．

## Embedding 

由于不同 token 之间的距离不同，如 dog 与 cat 的距离一定比与 blackboard 更近，one-hot 表示的向量无法用余弦相似度计算向量之间的相似度．Embedding 将每一个 token 映射为一个 $D$ 维稠密词向量，词表变成一个 $E\in \mathbb{R}^{V\times d}$ 的矩阵（如 $50000\times 512$）．当 token id = $i$ 时，直接取 $E[i]$ 即为 token 对应的向量．

## Word2Vec

Word2Vec 是一组学习词向量的方法，目标是学习到 $E\in \R^{|V|\times d}$，包含 CBWO、Skip Gram 等．

### CBOW

CBOW 用中心词周围的上下文词预测中心词，例如 `I love natural language processing`，将 `I love language processing` 四个词的词向量平均后输入 `embed_dim -> vocab_size` 的线性层，预测中间词的 id，训练 embedding 和线性投影层．

### Skip-Gram

Skip-Gram 与 CBOW 相反，其用中间词预测上下文词．它会将其拆成多次用中间词预测单个上下文词的过程，即 `natural` 分别预测 `I`、`love`、`language`、`processing`；线性层同样也是 `embed_dim -> vocab_size` 的．






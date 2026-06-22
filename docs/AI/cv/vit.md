# Vision Transformer

## Patch

如果想用 Transformer 处理图像，就要解决怎么把图像表示成 token 的问题．如果一个像素为一个 token，那么 token 数量是 $O(n^2)$，叠加注意力的复杂度就是 $O(n^4)$，显存和算力开销难以接受．

ViT 把 $H\times W$ 图像切成一组小块，每一个小块叫做 patch，大小为 $C\times P\times P$，将一个 patch 视为一个 token，整张图可以被切成 $N=\dfrac{H}{P}\times \dfrac{W}{P}$ 个 token（$H$ 和 $W$ 都可以被 $P$​ 整除）．$P$ 越小，patch 数量越多，每个 token 覆盖区域更小、细节保留更多，但复杂度会增加；$P$ 越大，复杂度更低，但空间信息可能损失更多．

将 patch 展平后得到 $C\times P^2$ 长度的向量，再用线性层投影到 Transformer 使用的 embedding 维度 $D$，整体形状变化就是
$$
(B,C,H,W)\to (B,N,C\times P^2)\to (B,N,D)
$$
上述 $C\times P \times P$ 的 patch 展平并经过线性层的操作与使用卷积操作时等价的，对应的卷积层形状是

```python
nn.Conv2d(
	in_channels=C,
    out_channels=D,
    kernel_size=P,
    stride=P,
)
```

## Class Token

Transformer Encoder 的输出和输入是同一个形状，为融合了其他 token 的序列．对于图像分类问题，我们需要有一个能表示整张图的向量表示．一个想法是对 patch token 做平均池化，这当然是可行的．

原始 ViT 在 patch token 前加入了可学习的 class token，也常写作 `[CLS]`．

即把输入 patch token 序列 $[x_1,x_2,\dots,x_N]$ 增加为 $[x_\text{cls},x_1,x_2,\dots,x_N]$，最后取 class token 的输出 $h_\text{cls}=H[:,0,:]$​，再送入分类头即可．

需要注意的是，class token 的形状是 `(1, 1, D)` 而不是 `(B, 1, D)`，因为它是模型参数；前向传播时将其扩展到 batch size．

## Positional Embedding

与 Transformer 一样，需要添加位置编码保留位置信息．ViT 采用的是可学习的位置向量 $P\in\R^{(N+1)\times D}$，注意位置向量需要包含 class token．

## Encoder

一般而言，ViT 只使用 Encoder 作为 backbone，因为 Encoder 能让每一个 patch token 看到全局其他的 token；由于图像是一次性传入的，patch 是在同一张图像上分割的，因此完全可以让 patch token 不需要 mask 做自注意力．


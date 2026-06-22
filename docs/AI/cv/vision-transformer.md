# Vision Transformer

Vision Transformer（ViT）把 Transformer Encoder 引入图像分类任务．其核心思想是把图像切分成 patch，并把每个 patch 当作一个视觉 token，再使用自注意力建模全局关系．基础 Self-Attention 与 Transformer 结构见 [Attention and Transformer](../dl/attention-and-transformer.md)，传统 CNN 图像分类模型见 [Image Classification](image-classification.md)．

## Motivation

CNN 通过局部卷积、权重共享和层级堆叠逐渐扩大感受野．这种归纳偏置非常适合图像，但也限制了模型从一开始直接建模全局关系的能力．ViT 减少了卷积结构中的局部先验，转而依赖大规模数据和 Transformer 的 self-attention 来学习 patch 之间的关系．

ViT 的基本判断是：如果有足够大的数据集和计算资源，图像也可以像文本序列一样被表示为 token 序列，并交给 Transformer 处理．

## Patch Embedding

给定输入图像 $x\in\mathbb{R}^{H\times W\times C}$，设 patch size 为 $P\times P$，则 patch 数量为：

$$
N=\frac{HW}{P^2}
$$

每个 patch 被展平成长度为 $P^2C$ 的向量，再经过线性投影映射到 $D$ 维 token embedding．如果使用分类任务常见的 `[CLS]` token，初始输入序列可写为：

$$
z_0=[x_{\text{class}};x_p^1E;x_p^2E;\ldots;x_p^NE]+E_{\text{pos}}
$$

其中 $E$ 是 patch embedding 矩阵，$E_{\text{pos}}$ 是 position embedding．位置编码是必要的，因为 self-attention 本身不包含 token 顺序或空间位置信息．

## Transformer Encoder

ViT 主体由多层 Transformer Encoder 组成．每一层通常包含 multi-head self-attention、MLP、residual connection 和 layer normalization：

$$
z_\ell'=\operatorname{MSA}(\operatorname{LN}(z_{\ell-1}))+z_{\ell-1}
$$

$$
z_\ell=\operatorname{MLP}(\operatorname{LN}(z_\ell'))+z_\ell'
$$

分类时通常取最终层 `[CLS]` token 的表示，送入 MLP head 得到类别预测．

## Relation to CNN

| Aspect | CNN | ViT |
| --- | --- | --- |
| 基本单元 | 卷积核 | Patch token |
| 归纳偏置 | 局部性、平移等变性、权重共享 | 较弱，主要依赖数据学习 |
| 全局关系 | 通过堆叠逐渐扩大感受野 | self-attention 可直接建模全局关系 |
| 数据需求 | 中小数据集上较强 | 通常更依赖大规模预训练 |
| 计算瓶颈 | 卷积计算 | attention 的 $O(N^2)$ token 交互 |

CNN 在视觉任务中自带强归纳偏置，因此数据较少时更容易训练．ViT 的归纳偏置较弱，但在大规模预训练后具有很强的可扩展性．

## Training and Variants

原始 ViT 在大规模数据集上预训练，再迁移到下游任务进行 fine-tuning．如果只在较小数据集上从头训练，ViT 往往不如强 CNN 稳定，因此常结合 data augmentation、regularization、knowledge distillation 和更强的预训练策略．

常见变体包括：

+ **DeiT**：通过数据增强与蒸馏改进 ViT 在 ImageNet 规模数据上的训练效率．
+ **Swin Transformer**：使用 shifted window attention 降低计算复杂度，并形成层级视觉特征．
+ **Hybrid ViT**：先用 CNN 提取低层特征，再把特征图 patch 化后交给 Transformer．

!!! note "ViT 的定位"

    Transformer 的通用机制放在深度学习部分，ViT 作为视觉模型放在计算机视觉部分．因此本节重点记录 ViT 如何把图像转化为 token 序列，以及它与 CNN 图像分类模型的关系．
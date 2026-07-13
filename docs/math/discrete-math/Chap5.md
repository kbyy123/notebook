# Chap 5: Induction and Recursion

## Mathematical Induction

**Mathematical induction** is used to prove that a proposition holds for every integer from some starting point onward.

### Ordinary Induction

Let $P(n)$ be a proposition about an integer $n$. To prove

$$
\forall n\geq n_0, P(n)
$$

it is sufficient to prove

$$
\begin{cases}
P(n_0) \\
\forall k\geq n_0,\ P(k)\rightarrow P(k+1)
\end{cases}
$$

> [!important]+ Mathematical Induction Steps
>
> 1. **Target**: Let us say we want to prove $\forall n \geq n_{0} ,P(n)$.
> 2. **Basic Step**: Prove $P(n_{0})$.
> 3. **Inductive Step**: Assume $P(k)$ is true, prove $P(k+1)$.
> 4. **Conclusion**: By mathematical induction, $\forall n \geq n_{0} ,P(n)$ is true.

### Strong Induction

In **strong induction**, the inductive step may use every preceding case from the starting point through $k$, rather than only $P(k)$. The strong inductive hypothesis is

$$
P(n_0)\land P(n_0+1)\land\cdots\land P(k).
$$

The corresponding inference rule is

$$
\forall k\geq n_0,
\left(\bigwedge_{j=n_0}^{k}P(j)\right)\rightarrow P(k+1)
\quad\Longrightarrow\quad
\forall n\geq n_0,\ P(n).
$$

> [!important]+ Mathematical Induction Steps
>
> 1. **Target**: Let us say we want to prove $\forall n \geq n_{0} ,P(n)$.
> 2. **Basic Step**: Prove $P(n_{0})$.
> 3. **Inductive Step**: Assume $P(n_{0}),\cdots, P(k-1),P(k)$ is true, prove $P(k+1)$.
> 4. **Conclusion**: By mathematical induction, $\forall n \geq n_{0} ,P(n)$ is true.

> [!example]+ Prove Every Postage $n\geq12$ Can Be Formed
>
> Prove that every postage of at least $12$ cents can be formed using only $4$-cent and $5$-cent stamps.
>
> === "Proof 1: Strong Induction"
>
> 	**1. Target**: Let $P(n)$ be the proposition *"12 cents or more can be formed using just 4-cent and 5-cent stamps"*.
>	
> 	**2. Basic Step**: Verify 4 consecutive initial cases:
>	
> 	$$
> 	\begin{aligned}
> 	12&=3\cdot4,\\
> 	13&=2\cdot4+1\cdot5,\\
> 	14&=1\cdot4+2\cdot5,\\
> 	15&=3\cdot5.
> 	\end{aligned}
> 	$$
>	
> 	Hence, $P(12),P(13),P(14)$, and $P(15)$ are true.
>	
> 	**3. Inductive Step**: Let $k\geq15$ be arbitrary. Assume that
>	
> 	$$
> 	P(12),P(13),\ldots,P(k-1),P(k)
> 	$$
>	
> 	Since $k\geq15$, we have
>	
> 	$$
> 	12\leq k-3\leq k.
> 	$$
>	
> 	The strong inductive hypothesis therefore gives $P(k-3)$. Hence, there are $a,b\in\mathbb N$ such that
>	
> 	$$
> 	k-3=4a+5b.
> 	$$
>	
> 	Adding one $4$-cent stamp gives
>	
> 	$$
> 	k+1=(k-3)+4=4(a+1)+5b.
> 	$$
>	
> 	Hence, $P(k+1)$ is true.
>	
> 	**4. Conclusion**: By strong induction, $P(n)$ is true for every integer $n\geq12$.
>
> === "Proof 2: Ordinary Induction"
>	
> 	**1. Target**: Let $P(n)$ be the proposition *"12 cents or more can be formed using just 4-cent and 5-cent stamps"*.
>	
> 	**2. Basic Step**: The postage $12$ can be formed using three $4$-cent stamps:
>	
> 	$$
> 	12=3\cdot4.
> 	$$
>	
> 	Thus, $P(12)$ is true.
>	
> 	**3. Inductive Step**: Let $k\geq12$ be arbitrary and assume that $P(k)$ is true. Then there are $a,b\in\mathbb N$ such that
>	
> 	$$
> 	k=4a+5b.
> 	$$
>	
> 	We consider two cases.
>	
> 	+ If $a\geq1$, replace one $4$-cent stamp with one $5$-cent stamp. Then
>	
> 	  $$
> 	  k+1=4(a-1)+5(b+1),
> 	  $$
>	
> 	  so $P(k+1)$ is true.
>	
> 	+ If $a=0$, then $k=5b\geq12$, so $b\geq3$. Replace 3 $5$-cent stamps with 4 $4$-cent stamps. Then
>	
> 	  $$
> 	  k+1=4\cdot4+5(b-3),
> 	  $$
>	
> 	  so $P(k+1)$ is true.
>	
> 	Therefore, $P(k)\rightarrow P(k+1)$ for every integer $k\geq12$.
>	
> 	**4. Conclusion**: By mathematical induction, $P(n)$ is true for every integer $n\geq12$.

> [!example]+ Fundamental Theorem of Arithmetic
> Show that if n is an integer greater than 1, then n can be written as the product of primes
>
> **1. Target**: Let $P(n)$ be the proposition *"$n$ can be written as a product of one or more primes"*. Prove $\forall n>1,P(n)$.
>
> **2. Basic Step**: $P(2)$ is true because $2$ is itself prime.
>
> **3. Inductive Step**: Let $k\geq2$ be arbitrary. Assume that
>
> $$
> P(2),P(3),\ldots,P(k-1),P(k)
> $$
>
> are all true. We need to prove $P(k+1)$.
>
> + If $k+1$ is prime, then it is already a product consisting of one prime, so $P(k+1)$ is true.
> + If $k+1$ is composite, then
>
>   $$
>   k+1=ab
>   $$
>
>   for some integers $a$ and $b$ satisfying
>
>   $$
>   2\leq a\leq b<k+1.
>   $$
>
>   In particular, $2\leq a,b\leq k$. By the inductive hypothesis, both $a$ and $b$ can be written as products of primes, therefore $k+1=ab$ can also be written as a product of primes. Hence, $P(k+1)$ is true.
>
> **4. Conclusion**: By strong induction, every integer greater than $1$ can be written as a product of one or more primes.

### Strengthening Induction Hypothesis

If $P(k)$ does not provide enough information to prove $P(k+1)$, another useful technique is to prove a stronger statement $Q(k)$ such that

$$
Q(k)\rightarrow P(k).
$$

The stronger proposition may be easier to prove because its inductive hypothesis provides more information.

> [!quote]- Well-Ordering Property
>
> The **well-ordering property** states that every nonempty set of nonnegative integers has a least element. Mathematical induction, strong induction, and the well-ordering property are logically equivalent. Here, the emphasis is on using induction rather than proving the validity of these principles.

## Recursion

### Recursive Definitions

A **recursive definition** defines larger objects in terms of smaller objects of the same type. A complete recursive definition usually contains three parts:

1. **Basis**: Specify the initial values or basic objects.
2. **Recursive Step**: Describe how new objects are constructed from objects already defined.
3. **Exclusion Rule**: No objects other than those obtained from the basis and recursive rules are included.

> [!warning] A Recursion Needs a Base
>
> Repeated applications of a recursive rule must eventually reach a defined basis case. Otherwise, the recursion does not determine a value.

<div></div>

<!-- 

### Recursively Defined Functions and Sequences

For a function $f:\mathbb N\rightarrow S$, one may define $f(0)$ first and then define $f(n)$ using values at smaller arguments.

> [!example]+ Powers of Two
>
> The sequence $a_n=2^n$ can be defined recursively by
>
> $$
> a_0=1,
> \qquad
> a_n=2a_{n-1}\quad(n\geq1).
> $$
>
> Consequently, $a_1=2$, $a_2=4$, and $a_3=8$.

> [!example]+ Factorial
>
> The factorial function has the recursive definition
>
> $$
> 0!=1,
> \qquad
> n!=n(n-1)!\quad(n\geq1).
> $$

> [!example]+ Fibonacci Sequence
>
> The Fibonacci sequence requires two basis values because each new term depends on the preceding two terms:
>
> $$
> f_0=0,
> \qquad
> f_1=1,
> \qquad
> f_n=f_{n-1}+f_{n-2}\quad(n\geq2).
> $$
>
> This gives $0,1,1,2,3,5,8,\ldots$. Proofs about the Fibonacci sequence often use strong induction with two initial cases.

### Recursively Defined Sets

An infinite set can be defined using a small number of basis elements and a rule for generating new elements. For example, define a set $S$ by the following rules:

1. $3\in S$.
2. If $x,y\in S$, then $x+y\in S$.
3. No other elements belong to $S$.

Starting from $3$, the rules generate $6,9,12,\ldots$. Hence,

$$
S=\{3,6,9,12,\ldots\}
=\{3m\mid m\in\mathbb Z^+\}.
$$

The set of strings over an alphabet can also be defined recursively. Given an alphabet $\Sigma$, the set $\Sigma^*$ of all finite strings over $\Sigma$ is defined by:

1. The empty string $\varepsilon$ belongs to $\Sigma^*$.
2. If $w\in\Sigma^*$ and $x\in\Sigma$, then the concatenated string $wx\in\Sigma^*$.
3. No other strings belong to $\Sigma^*$. 
   
-->

### Structural induction

**Structural induction** proves properties of recursively defined objects by following the structure of their recursive definitions.

1. **Basis Step**: Prove that every basis object has property $P$.
2. **Structural Inductive Hypothesis**: Assume that the smaller objects used in a construction have property $P$.
3. **Recursive Step**: Prove that an object built by the recursive rule also has property $P$.

Structural induction can be viewed as induction over the construction process of an object. It is commonly used for recursively defined formulas, strings, and trees.

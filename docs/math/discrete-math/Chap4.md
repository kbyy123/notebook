# Chap4 Number Theory

## Divisibility and Modular Arithmetic

Number theory studies arithmetic properties of integers. In computer science, it appears in hashing, congruence calculations, digital signatures, and cryptography.

### Divisibility

Let $a,b\in\mathbb{Z}$ and $a\neq0$.

**Divides**:

$$
a\mid b \Leftrightarrow \exists c\in\mathbb{Z}(b=ac)
$$

If $a\mid b$, then $a$ is a **factor** or **divisor** of $b$, and $b$ is a **multiple** of $a$.

!!! quote "Basic Properties"

    For $a,b,c\in\mathbb{Z}$ and $a\neq0$:
    
    + $a\mid0$
    + $(a\mid b\wedge a\mid c)\Rightarrow a\mid(b+c)$
    + $a\mid b\Rightarrow a\mid bc$
    + $(a\mid b\wedge b\mid c)\Rightarrow a\mid c$
    
    More generally, if $a\mid b$ and $a\mid c$, then $a\mid(mb+nc)$ for all $m,n\in\mathbb{Z}$.

### Division Algorithm

For any integers $a,d$ with $d\neq0$, there exist unique integers $q,r$ such that

$$
a=dq+r,\qquad 0\leq r<|d|
$$

$q$ is the **quotient** and $r$ is the **remainder**.

We write:

$$
q=a\operatorname{ div }d,\qquad r=a\bmod d
$$

The remainder is always nonnegative in this theorem, for example:
+ $-11 \operatorname{ div } 3=-4$
+ $-11 \bmod3 = 1$

### Modular and Congruence

Let $a,b\in\mathbb{Z}$ and $m\in\mathbb{Z}^+$.

**Congruence modulo**(同余) $m$:

$$
a\equiv b\pmod m
\Leftrightarrow
m\mid(a-b)
$$

Equivalent forms:

$$
a\equiv b\pmod m
\Leftrightarrow
a\bmod m=b\bmod m
$$

Every integer is congruent to its remainder:

$$
a\equiv a\bmod m\pmod m
$$

!!! quote "Congruence Rules"

    If
    
    $$
    a\equiv b\pmod m,\qquad c\equiv d\pmod m
    $$
    
    then
    
    $$
    a+c\equiv b+d\pmod m
    $$
    
    and
    
    $$
    ac\equiv bd\pmod m
    $$
    
    Therefore:
    
    $$
    (a+b)\bmod m=((a\bmod m)+(b\bmod m))\bmod m
    $$
    
    $$
    ab\bmod m=((a\bmod m)(b\bmod m))\bmod m
    $$

## Integer Representations and Algorithms

### Base-$b$ Representation

For any positive integers $n$ and $b>1$, there is a unique sequence of digits

$$
a_k,a_{k-1},\dots,a_1,a_0
$$

where $0\leq a_i<b$, such that

$$
n=\sum_{i=0}^{k}a_ib^i
$$

We write this as

$$
n=(a_ka_{k-1}\cdots a_1a_0)_b
$$

Common bases:

+ base $10$: decimal.
+ base $2$: binary.
+ base $8$: octal.
+ base $16$: hexadecimal.

To convert $n$ to base $b$, repeatedly divide by $b$ and record remainders from right to left.

```pseudocode
procedure base_b_expansion(n: positive integer, b: integer greater than 1)
    q := n
    k := 0
    while q != 0
        ak := q mod b
        q := q div b
        k := k + 1
    return ak-1...a1a0
```

### Integer Operations

Binary addition, multiplication, and division are built from the same ideas as decimal arithmetic.

Binary addition uses a carry bit:

```pseudocode
procedure add(an-1...a0, bn-1...b0: binary representations)
    carry := 0
    for i := 0 to n - 1
        bitSum := ai + bi + carry
        si := bitSum mod 2
        carry := bitSum div 2
    sn := carry
    return sn...s0
```

Binary multiplication adds shifted copies of one factor:

```pseudocode
procedure multiply(a, b: binary representations)
    product := 0
    for i := 0 to n - 1
        if bi = 1 then product := add(a shifted left by i, product)
    return product
```

### Modular Exponentiation

The modular exponentiation problem is to compute $b^n\bmod m$ efficiently.

We use **Exponentiation by squaring**:

```pseudocode
procedure modularExp(b: integer, n = (ak-1...a0)2, m: positive integer)
    x := 1
    power := b mod m
    for i := 0 to k - 1
        if ai = 1 then x := (x * power) mod m
        power := (power * power) mod m
    return x
```

???+ quote "RSA Encryption"

    RSA is an application of modular exponentiation and modular inverses.
    
    1. Choose two large primes $P,Q$.
    2. Let $N=PQ$ and $L=(P-1)(Q-1)$.
    3. Choose $E<L$ with $\gcd(E,L)=1$.
    4. Find $D$ such that
    
       $$
       DE\equiv1\pmod L
       $$
    
    The public key is $(E,N)$ and the private key is $D$.
    
    Encryption:
    
    $$
    C\equiv M^E\pmod N
    $$
    
    Decryption:
    
    $$
    M\equiv C^D\pmod N
    $$
    
    This is treated as an application rather than a core number-theory theorem here.

## Primes and GCD

### Prime Numbers

An integer $p>1$ is **prime**(质数) if its only positive divisors are $1$ and $p$.

An integer greater than $1$ that is not prime is **composite**(合数).

*Thm.* **Fundamental Theorem of Arithmetic**: Every positive integer has a unique prime factorization when primes are written in nondecreasing order.

+ $2000=2^4\cdot5^3$
+ $2001=3\cdot23\cdot29$
+ $2002=2\cdot7\cdot11\cdot13$

*Thm.* **Trial Division**: If $n$ is composite, then $n$ has a prime divisor less than or equal to $\sqrt n$.

To test whether $n$ is prime, it is enough to check divisibility by primes $\leq\sqrt n$.

???+ example "Show 101 Is Prime"

    Since
    
    $$
    \sqrt{101}<11
    $$
    
    it is enough to test primes $2,3,5,7$.
    
    $101$ is divisible by none of them, so $101$ is prime.

*Thm.* There are infinitely many primes. See proof in [Chap1 6.3.1](Chap1.md).

??? quote "Mersenne Primes"

    Prime numbers of the form
    
    $$
    2^p-1
    $$
    
    where $p$ is prime are called **Mersenne primes**.
    
    Examples:
    
    $$
    2^2-1=3,\quad 2^3-1=7,\quad 2^5-1=31,\quad 2^7-1=127
    $$
    
    But $2^{11}-1=2047=23\cdot89$, so not every number of this form is prime.

### GCD & LCM

For integers $a,b$ not both $0$, the **greatest common divisor** is

$$
\gcd(a,b)=\max\{d\in\mathbb{Z}^+\mid d\mid a\wedge d\mid b\}
$$

and the **least common multiple** is

$$
\operatorname{lcm}(a,b)=\min\{m\in\mathbb{Z}^+\mid a\mid m\wedge b\mid m\}
$$

If $a=p_1^{a_1}p_2^{a_2}\cdots p_n^{a_n}$ and $
b=p_1^{b_1}p_2^{b_2}\cdots p_n^{b_n}$, then

$$
\gcd(a,b)=p_1^{\min(a_1,b_1)}p_2^{\min(a_2,b_2)}\cdots p_n^{\min(a_n,b_n)}
$$

$$
\operatorname{lcm}(a,b)=p_1^{\max(a_1,b_1)}p_2^{\max(a_2,b_2)}\cdots p_n^{\max(a_n,b_n)}
$$

For positive integers $a,b$:

$$
ab=\gcd(a,b)\operatorname{lcm}(a,b)
$$

### Relative Primality

Integers $a$ and $b$ are **relatively prime** or **coprime** if

$$
\gcd(a,b)=1
$$

A set of integers is **pairwise relatively prime** if every pair of distinct elements is relatively prime. For example $\{10,17,21\}$. 

### Euclidean Algorithm

$$
\gcd(a,b)=\gcd(b,a\bmod b)
$$

```pseudocode
procedure gcd(a, b: positive integers)
    while b != 0
        r := a mod b
        a := b
        b := r
    return a
```

The last nonzero remainder is the gcd.

???+ example "Example"

    $$
    \begin{aligned}
    \gcd(372,164)
    &=\gcd(164,44)\\
    &=\gcd(44,32)\\
    &=\gcd(32,12)\\
    &=\gcd(12,8)\\
    &=\gcd(8,4)\\
    &=\gcd(4,0)\\
    &=4
    \end{aligned}
    $$

### Bézout's Theorem

If $a$ and $b$ are positive integers, then there exist integers $s,t$ such that

$$
\gcd(a,b)=sa+tb
$$

$s$ and $t$ are called **Bézout coefficients**(贝祖系数), the equation is called **Bézout's identity**.

???+ example "Back Substitution"

    Express $\gcd(252,198)=18$ as a linear combination.
    
    Euclidean algorithm:
    
    $$
    \begin{aligned}
    252&=1\cdot198+54\\
    198&=3\cdot54+36\\
    54&=1\cdot36+18\\
    36&=2\cdot18
    \end{aligned}
    $$
    
    Work backward: each time, represent the smaller number as a combination of the larger number in Euclidean algorithm
    
    $$
    \begin{aligned}
    18&=54-36\\
    &=54-(198-3\cdot54)\\
    &=4\cdot54-198\\
    &=4(252-198)-198\\
    &=4\cdot252-5\cdot198
    \end{aligned}
    $$

*Lem*. If $\gcd(a,b)=1$ and $a\mid bc$, then $a\mid c$.

*Lem*. If $ac\equiv bc\pmod m$, and $\gcd(c,m)=1$, then $a\equiv b\pmod m$.

*Lem*. If $p$ is prime and $p\mid a_1a_2\cdots a_n$, then $p\mid a_i$ for some $i$.

## Solving Congruences

### Inverses Modulo $m$

An integer $\overline{a}$ is an **inverse of $a$ modulo $m$** if

$$
a\overline{a}\equiv1\pmod m
$$

An inverse exists iff

$$
\gcd(a,m)=1
$$

When it exists, it is unique modulo $m$.

??? proof "Why it exists"

    If $\gcd(a,m)=1$, Bézout's theorem gives integers $s,t$ such that

    $$
    sa+tm=1
    $$

    Therefore

    $$
    sa\equiv1\pmod m
    $$

    so $s$ is an inverse of $a$ modulo $m$.


### Linear Congruences

*Def*. A congruence of the form

$$
ax\equiv b\pmod m
$$

where $m$ is positive, is called a **linear congruence**.

If $\gcd(a,m)=1$, multiplying both sides by the inverse $\overline{a}$ to solve the congruence:

$$
x\equiv \overline{a}b\pmod m
$$

### Chinese Remainder Theorem

Let $m_1,m_2,\dots,m_n$ be pairwise relatively prime positive integers greater than $1$, and let $a_1,a_2,\dots,a_n$ be arbitrary integers.

To solve the system

$$
\begin{cases}
x\equiv a_1\pmod{m_1}\\
x\equiv a_2\pmod{m_2}\\
\cdots\\
x\equiv a_n\pmod{m_n}
\end{cases}
$$

Let $m=m_1m_2\cdots m_n$ and $M_k=\dfrac{m}{m_k}$, since $\gcd(M_k,m_k)=1$, choose $y_k$ such that

$$
M_ky_k\equiv1\pmod{m_k}
$$

Then a solution is

$$
x\equiv\sum_{k=1}^{n}a_kM_ky_k\pmod m
$$

> 中国剩余定理类似寻找向量空间中的正交基向量，每一个 $M_ky_k$ 都满足模 $m_k$ 同余 1 而模 $m_{i,i \ne k}$ 同余 0，这样就能直接通过投影得到系数．

???+ example "Sun-Tsu's Problem"

    Solve:
    
    $$
    x\equiv2\pmod3,\qquad x\equiv3\pmod5,\qquad x\equiv2\pmod7
    $$
    
    Here
    
    $$
    m=3\cdot5\cdot7=105
    $$
    
    $$
    M_1=35,\quad M_2=21,\quad M_3=15
    $$
    
    Inverses:
    
    $$
    35\cdot2\equiv1\pmod3,\quad
    21\cdot1\equiv1\pmod5,\quad
    15\cdot1\equiv1\pmod7
    $$
    
    Therefore
    
    $$
    x\equiv2\cdot35\cdot2+3\cdot21\cdot1+2\cdot15\cdot1
    \equiv233\equiv23\pmod{105}
    $$

???+ tip "Back Substitution"

    A system of congruences can also be solved by rewriting one congruence as an equality and substituting step by step.

    Solve:
    
    $$
    x\equiv1\pmod5,\quad x\equiv2\pmod6,\quad x\equiv3\pmod7
    $$
    
    From $x\equiv1\pmod5$, write
    
    $$
    x=5t+1
    $$
    
    Substitute into $x\equiv2\pmod6$:
    
    $$
    5t+1\equiv2\pmod6
    $$
    
    Thus $t\equiv5\pmod6$, so $t=6u+5$.
    
    Then
    
    $$
    x=5(6u+5)+1=30u+26
    $$
    
    Substitute into $x\equiv3\pmod7$:
    
    $$
    30u+26\equiv3\pmod7
    $$
    
    Thus $u\equiv6\pmod7$, so $u=7v+6$.
    
    Hence
    
    $$
    x=30(7v+6)+26=210v+206
    $$
    
    Therefore
    
    $$
    x\equiv206\pmod{210}
    $$

### CRT Representation of Large Integers

If $m_1,m_2,\dots,m_n$ are pairwise relatively prime and $m=m_1m_2\cdots m_n$, then every integer $a$ with $0\leq a<m$ can be uniquely represented by

$$
(a\bmod m_1,\ a\bmod m_2,\ \dots,\ a\bmod m_n)
$$

This representation can make large-integer arithmetic easier, because computations modulo different $m_k$ can be done separately.

???+ example "Modulo 3 and 4"

    For integers less than $12$, use the pair
    
    $$
    (a\bmod3,\ a\bmod4)
    $$
    
    Then:
    
    $$
    \begin{array}{c|c}
    a & (a\bmod 3,\ a\bmod 4) \\
    \hline
    0  & (0,0) \\
    1  & (1,1) \\
    2  & (2,2) \\
    3  & (0,3) \\
    4  & (1,0) \\
    5  & (2,1) \\
    6  & (0,2) \\
    7  & (1,3) \\
    8  & (2,0) \\
    9  & (0,1) \\
    10 & (1,2) \\
    11 & (2,3)
    \end{array}
    $$

???+ quote "CRT in RSA Decryption"

    RSA decryption computes
    
    $$
    M\equiv C^D\pmod N
    $$
    
    where $N=PQ$ for large primes $P,Q$.
    
    Instead of computing directly modulo $N$, compute
    
    $$
    M\equiv C^D\pmod P,\qquad M\equiv C^D\pmod Q
    $$
    
    and combine the two results with CRT.
    
    This reduces the modulus size and also allows parallel computation.

## Fermat's Little Theorem and Related Ideas

### Fermat's Little Theorem

If $p$ is prime and $p\nmid a$, then

$$
a^{p-1}\equiv1\pmod p
$$

Also we have $a^{p-2}\times a \equiv1\pmod p$, so $a^{p-2}$ is an inverse of $a$ modulo $p$. 

### Pseudoprimes

If $n$ is composite and

$$
b^{n-1}\equiv1\pmod n
$$

then $n$ is a **pseudoprime to base $b$**(伪质数).

???+ example "Example"

    $341=11\cdot31 $ is a pseudoprime to base $2$ because $2^{340}\equiv1\pmod{341}$.


???+ quote "Carmichael Numbers"

    A **Carmichael number** is a composite integer $n$ such that
    
    $$
    b^{n-1}\equiv1\pmod n
    $$
    
    for every positive integer $b$ with $\gcd(b,n)=1$.
    
    $561=3\cdot11\cdot17$ is the classic example, for every $b$ coprime to $561$ we have $b^{560}\equiv1\pmod{561}$.

### Primitive Roots

Let $p$ be prime. An integer $r\in\mathbb{Z}_p$ is a **primitive root modulo $p$**(原根) if every nonzero element of $\mathbb{Z}_p$ is congruent to a power of $r$.

$$
\{r^1,r^2,\dots,r^{p-1}\}\equiv\{1,2,\dots,p-1\}\pmod p
$$

???+ example "Modulo 11"

    $2$ is a primitive root modulo $11$ because:
    
    $$
    \begin{aligned}
    2^1&\equiv2\\
    2^2&\equiv4\\
    2^3&\equiv8\\
    2^4&\equiv5\\
    2^5&\equiv10\\
    2^6&\equiv9\\
    2^7&\equiv7\\
    2^8&\equiv3\\
    2^9&\equiv6\\
    2^{10}&\equiv1
    \end{aligned}
    \pmod{11}
    $$

### Discrete Logarithms

Suppose $p$ is prime, $r$ is a primitive root modulo $p$, and $a\in\{1,2,\dots,p-1\}$.

If

$$
r^e\equiv a\pmod p,\qquad 0\leq e\leq p-1
$$

then $e$ is the **discrete logarithm**(离散对数) of $a$ modulo $p$ to the base $r$.

???+ example "Example"

    Modulo $11$ with base $2$:
    
    + $2^8\equiv3\pmod{11}$ so $\log_2 3=8$
    + $2^4\equiv5\pmod{11}$ so $\log_2 5=4$
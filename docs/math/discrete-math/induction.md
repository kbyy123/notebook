# Induction
Induction is a powerful tool which is used to establish a statement holds for all natural numbers.
## Simple Induction
Simple Induction is a induction which prove the next statement by assuming the previous one.

If $P(n)$ is a predictate, and we want to prove that $\forall n \in \mathbb{N}, P(n)$, the *principle of induction* asserts that to prove this requires three simple steps:

1. Base Case: Prove that $P(0)$ is true.
2. Induction Hypothesis: For arbitrary $k\geq 0$, assume that $P(k)$ is true.
3. Inductive Step: With the assumption of the Induction Hypothesis, prove that $P(k+1)$ is true.

!!! quote "Strengthen the Induction Hypothesis"

    Sometimes we can't prove $P(k+1)$ from $P(k)$, since the information $P(k)$ provides is not enough. To tackle this, we can choose to prove a stronger statement $Q(n)$ instead of $P(n)$, i.e. $Q(n)\implies P(n)$.

    You may think that $Q(n)$ is a stronger statement and it's harder to prove than $P(n)$, but remember that stronger statements provide more information, i.e. strengthen the Induction Hypothesis. And the extra information may be the key.
## Strong Induction
Strong induction is similar to simple induction, except that instead of just assuming $P(k)$ is true, we assume the stronger statement $\land_{i=0}^kP(i)$ is true. 

Strong induction can't prove statements which weak induction can't, because strong induction is just the "sum" of weak inductions. But it can make proofs easier.

!!! example "Prove: Every natural number > 1 can be written as a product of one or more primes"
    Let $P(n)$ be the proposition that $n$ can be written as a product of one or more primes.

    1. Base Case: $n=2$, and clearly $P(2)$ is true, because $2$ is a prime number.
    2. Induction Hypothesis: Assume $P(n)$ for all $2\leq n \leq k$.
    3. Inductive Step: Prove that $n=k+1$ can be written as a product of primes.
        + If $k+1$ is a prime number, it can be the product of itself, so it's true.
        + If $k+1$ is not a prime number, then we have $k+1=xy$ for some $x,y\in \mathbb{Z}^+$ and $1< x,y<k+1$. By the Induction Hypothesis, x and y can each written as a product of primes (since $x,y<k$), so $k+1$ can be written as a product of primes.

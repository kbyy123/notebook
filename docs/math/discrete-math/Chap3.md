# Chap3 Algorithms

## Algorithms

**Def.** A procedure that follows a sequence of steps that leads to the desired answer.

??? quote "Features of Algos"

    + *input*. Information or data that comes in.
    + *Output*. Information or data that goes out.
    + *Definiteness*. Algorithm is precisely defined.
    + *Correctness*. Outputs correctly relate to inputs.
    + *Finiteness*. Won’t take forever to describe or run.
    + *Effectiveness*. Individual steps are all do-able.
    + *Generality*. Works for many possible inputs.
    + *Efficiency*. Takes little time & memory to run.

### Pseudocode

The type of pseudocode is not fixed, it just needs to be understandable to others. Below is the pseudocode in the slides.

1. `procedure procname(arg: type)` 

```pseudocode
procedure maximum(L: list of integers)
	[statements]
	return expression
```

2. Assignment statement `variable := expression`. e.g. `x := the largest integer in the list L`

3. Informal statement, e.g. `swap x and y`
4. begin & end (like "{}" in C-like languages)

```pseudocode
begin
	statement 1
	statement 2
	...
end
```

5. {comment} 
6. Condition: `if condition then stmt1 else stmt2`
7. Loop: `while condition statement` & `for var:= initial to final stmt`

!!! example "Examples"

    Max:
    
    ```pseudocode
    procedure max(a1, a2, ..., an: integers)
        v := a1
        for i := 2 to n
            if ai > v then v := ai
        return v
    ```
    
    Binary Search:
    
    ```pseudocode
    procedure binary_search(x: integer, a1, a2, ..., an: ordered distinct integers)
        l := 1
        r := n
        while l < r
            begin
            m = (i + j ) / 2	{floor}
            if x > am then i := m + 1 else j := m
            end
        if x = ai then location := i else location := 0
        return location
    ```

### Basic Algorithms

+ Searching: Linear search, Binary search...

+ Sorting: Bubble sort, Insertion sort...
+ Greedy

## Growth of Functions

**Asymptotic growth**(渐进式增长) describes how a function behaves when the input becomes large enough.

When we compare algorithms, we usually:

+ care about **large inputs** rather than small examples.
+ ignore implementation details and constant factors.
+ compare how the resource cost grows as a function of input size.

If $f(n)=30n+8$ and $g(n)=n^2+1$, then $g$ eventually becomes much larger than $f$, even though $g$ may be smaller for some small values of $n$.

### Big-O Notation

Let $f$ and $g$ be functions from $\mathbb{N}$ or $\mathbb{R}$ to $\mathbb{R}$.

**Big-O notation** gives an asymptotic upper bound:

$$
f(n)\in O(g(n))
\Leftrightarrow
\exists c >0\,\exists k\,\forall n(n>k \to \left|f(n)|\leq c|g(n)|\right)
$$

Equivalently, $f$ is at most order $g$.

The constants $c$ and $k$ are called **witnesses** for the Big-O relationship. They are not unique. Once we choose them, we only need to prove the inequality for all sufficiently large $n$.

???+ example "Examples"

    Show $n^2+1\in O(n^2)$:
    
    $$
    n^2+1<n^2+n^2=2n^2,\quad n>1
    $$
    
    Choose $c=2,k=1$.


??? quote "Little-o"

    Little-o gives a strictly smaller order:
    
    $$
    f(n)\in o(g(n))
    \Leftrightarrow
    \forall c>0\,\exists k\,\forall n(n>k\to\left |f(n)|<c|g(n)|\right)
    $$
    
    If $f\in o(g)$, then $f\in O(g)$.
    
    A common limit test is:
    
    $$
    \lim_{n\to\infty}\frac{f(n)}{g(n)}=0
    \Rightarrow f(n)\in o(g(n))
    $$

### Ordering Growth Rates

$$
1
\prec \log\log n
\prec \log n
\prec (\log n)^c
\prec n
\prec n\log n
\prec n^2
\prec n^3
\prec c^n
\prec n!
\prec n^n
$$

where $c>1$ for the exponential term.

???+ example "A Typical Ordering"

    For the functions
    
    $$
    \begin{aligned}
    &10000,\quad \log\log n,\quad (\log n)^2,\quad n^2(\log n)^3,\\
    &n^3+n(\log n)^2,\quad 8n^3+17n^2+111,\quad 1.5^n,\quad 2^n,\quad 2^n(n^2+1),\quad n!
    \end{aligned}
    $$
    
    an increasing order is:
    
    $$
    \begin{aligned}
    10000
    &\prec \log\log n
    \prec (\log n)^2
    \prec n^2(\log n)^3\\
    &\prec n^3+n(\log n)^2
    \sim 8n^3+17n^2+111\\
    &\prec 1.5^n
    \prec 2^n
    \prec 2^n(n^2+1)
    \prec n!
    \end{aligned}
    $$

### Combining Growth Estimates

If $f_1\in O(g_1)$ and $f_2\in O(g_2)$, then

$$
f_1+f_2\in O(\max\{g_1,g_2\})
$$

If $f_1\in O(g_1)$ and $f_2\in O(g_2)$, then

$$
f_1f_2\in O(g_1g_2)
$$

This is why we often simplify an expression by keeping only the fastest-growing part.

### Big-Omega Notation

**Big-Omega notation** gives an asymptotic lower bound:

$$
f(n)\in \Omega(g(n))
\Leftrightarrow
\exists c>0\,\exists k\,\forall n(n>k \to \left|f(n)|\geq c|g(n)|\right)
$$

It likes the inverse of Big-O notation:

$$
f(n)\in \Omega(g(n)) \Leftrightarrow g(n)\in O(f(n))
$$

It tells us that $f$ grows at least as fast as $g$, up to a constant factor after some point.

### Big-Theta Notation

**Big-Theta notation** gives a tight asymptotic bound:

$$
f(n)\in \Theta(g(n))
\Leftrightarrow
f(n)\in O(g(n))\wedge f(n)\in \Omega(g(n))
$$

Equivalently:

$$
f(n)\in \Theta(g(n))
\Leftrightarrow
\exists c_1,c_2>0\,\exists k\,\forall n>k
\left(c_1|g(n)|\leq |f(n)|\leq c_2|g(n)|\right)
$$

So $f$ and $g$ have the same order of growth.

???+ example "Summation"

    $$
    \sum_{i=1}^{n}i=\frac{n(n+1)}{2}\in\Theta(n^2)
    $$
    
    The highest-degree term is $\frac12 n^2$, so the order is $\Theta(n^2)$.

**Polynomial Order**: If $f(x)=a_nx^n+a_{n-1}x^{n-1}+\cdots+a_1x+a_0, a_n\neq0$, then $f(x)\in \Theta(x^n)$.

## Algorithmic Complexity

Algorithmic complexity(算法复杂度) measures the amount of resources required to perform a computation.

Common measures:

+ **time complexity**: number of operations or steps.
+ **space complexity**: number of memory bits.

Because inputs have different sizes, complexity is usually written as a function of input length $n$.

The common cases are:

+ **worst-case complexity**: maximum cost among inputs of size $n$.
+ **best-case complexity**: minimum cost among inputs of size $n$.
+ **average-case complexity**: expected cost under a given input distribution.

### Simple Complexity Analysis

When each line of pseudocode takes constant time, loops usually determine the order.

???+ example "Examples"

    === "Max"
        ```pseudocode
        procedure max(a1, a2, ..., an: integers)
            v := a1
            for i := 2 to n
                if ai > v then v := ai
            return v
        ```
    
        The loop executes $n-1$ times, so the worst-case time complexity is $\Theta(n)$.
    
    === "Linear Search"
        Linear search checks elements one by one.
        
        + worst case: $\Theta(n)$.
        + best case: $\Theta(1)$.
        + average case when the item is present uniformly: $\Theta(n)$.

    === "Binary Search"
        Binary search halves the remaining search interval at each step.
        
        If $n=2^k$, the number of iterations is $k=\log_2 n$. Therefore binary search has time complexity $\Theta(\log n)$.


### Problem Complexity

The complexity of a computational problem is the order of growth of the best possible algorithm for solving that problem.

For example, searching an ordered list has at most logarithmic time complexity because binary search solves it in $O(\log n)$ time.

In practice, we often know an **upper bound** from a known algorithm, but proving that no better algorithm exists can be much harder.

### Tractable and Intractable Problems (Optional)

A problem is **tractable** or **feasible** if it can be solved in polynomial time.

The class **P** is the set of decision problems solvable in polynomial time.

A problem is usually called **intractable** if its best known or required complexity is greater than polynomial time.

!!! warning "Technical vs Practical"

    $n^{1000000}$ is technically polynomial but useless in practice.
    
    $n\log\log\log n$ is technically superlinear but may be easy in practice.
    
    The polynomial/non-polynomial boundary is a theoretical classification, not a complete engineering judgment.

???+ quote "P, NP, NP-Complete, and NP-Hard"

    **NP** is the class of decision problems whose proposed solutions can be checked in polynomial time.

    We know $P\subseteq NP$, and the famous open question is whether $P=NP$.

    Most computer scientists believe $P\neq NP$, but no proof is known.

    **NP-complete** problems satisfy two conditions:

    + they are in NP.
    + every problem in NP can be reduced to them in polynomial time.

    If any NP-complete problem has a polynomial-time algorithm, then every problem in NP has one.

    Common examples include SAT, the decision version of TSP, and Hamiltonian cycle.

    **NP-hard** problems are at least as hard as every problem in NP, but they are not necessarily in NP.

???+ quote "The Halting Problem"

    The halting problem asks whether there is an algorithm that can decide, for any program $P$ and input $I$, whether $P(I)$ eventually halts.
    
    Alan Turing proved that no such algorithm exists.
    
    Proof idea by contradiction:
    
    1. Assume a procedure $H(P,I)$ decides whether $P$ halts on input $I$.
    2. Construct a program $K(P)$:
        + if $H(P,P)$ says "$P(P)$ loops forever", then $K(P)$ halts.
        + if $H(P,P)$ says "$P(P)$ halts", then $K(P)$ loops forever.
    3. Run $K(K)$.
    
    If $H(K,K)$ says it loops forever, then $K(K)$ halts. If $H(K,K)$ says it halts, then $K(K)$ loops forever. Both cases contradict the assumed correctness of $H$.
    
    Therefore the halting problem is undecidable.


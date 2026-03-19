# Proof
## Proofs
A proof is a finite sequence of steps called logical deductions, which established the truth of a desired statement. More specifically, a proof is a sequence of statements where each successive statement is necessarily true if the previous statements were true.

## Proof Techniques
### Direct Proof

Approach: 

$$
\text{Assume:  } P \quad \cdots \quad \text{Therefore: } Q
$$

Conclusion: $P\implies Q$.

### Proof by Contraposition
Recall that: $P \implies Q \equiv \neg Q \implies \neg P$

Approach: 

$$
\text{Assume:  } \neg Q \quad \cdots \quad \text{Therefore: } \neg P
$$

Conclusion: $\neg Q \implies \neg P$, so $P \implies Q$.
 
Example: 

+ Prove Pigeonhole Principle.
### Proof by Contradiction
To prove $P$, we assume that $P$ is false, and show that this leads to a conclusion which is A contradiction.

Approach:

$$
\text{Assume:  } \neg P \quad \cdots \quad \text{Therefore: } R \land \neg R
$$

Conclusion: $\neg P \implies R \land \neg R$, which is a contradiction, i.e. $\neg P \implies \text{False}$, so use contraposition we have $\text{True} \implies P$, so $P$.

Example: 

+ Prove there are infinite prime numbers.
+ Prove $\sqrt{2}$ is irrational.
### Proof by Cases
Sometimes when we wish to prove a claim, we don't know which of a set of possible cases is true, but we know that at least one of them is true.

Example: Prove there exist irrational numbers $x$ and $y$ such that $x^y$ is rational.

Proof: let $x=\sqrt{2}$ and $y=\sqrt{2}$. Make the following two cases:

+ $a$. $\sqrt{2}^{\sqrt{2}}$ is rational.
+ $b$. $\sqrt{2}^{\sqrt{2}}$ is irrational.

Because $a\lor b$ is a tautology, exactly one of them must be true.

+ If $a$ is true, this immediately yields our claim, since $x$ and $y$ are both irrational and $x^y$ is rational. 
+ If $b$ is true, now we have a new irrational number $\sqrt{2}^{\sqrt{2}}$. Let $\sqrt{2}^{\sqrt{2}}$ and $y=\sqrt{2}$, Then,

$$
x^y=(\sqrt{2}^{\sqrt{2}})^{\sqrt{2}}=(\sqrt{2})^{(\sqrt{2}\cdot \sqrt{2})}=\sqrt{2}^2=2,
$$

Now we again started with two irrational numbers $x$ and $y$ and obtained rational $x^y$.

### Mathematical Induction
See [induction](induction.md).

## Common Error
+ Don't assume the claim aim to prove. If we want to prove $P$, we shouldn't assume $P$ is true and implies a tautology. For example, if we want to prove $-2=2$, we assume it and implies $4=4$, which is true, but the proof makes no sense.
+ Never forget to consider whether you divide by zero.
+ Don't forget to flip the direction of the inequality when multiplying a negative number.
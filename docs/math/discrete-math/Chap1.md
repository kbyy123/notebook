# The Foundations: Logic and Proofs

## Propositional Logic
### Propositions
**proposition**(命题): A declarative sentence that is either true or false.

propositional variables(命题变量): Variables that represent propositions, usually letters like $p,q,r,s$.

atomic proposition(原子命题): Propositions that cannot be expressed by simpler propositions.

compound proposition(复合命题): Propositions that formed from existing propositions using logical operators.
### Logical Operators
#### Operators
**negation**(not, 否定): $\neg p$.
<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/image-20260321150511495.png" alt="image-20260321150511495" style="zoom: 58%;" />
</div>

**conjunction**(and, 合取): $p\wedge q$.
<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/image-20260321150527312.png" alt="image-20260321150527312" style="zoom:50%;" />
</div>

**disjunction**(inclusive or, 析取): $p\vee q$.
<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/image-20260321150533321.png" alt="image-20260321150533321" style="zoom:50%;" />
</div>

**XOR**(exclusive or, 异或): $p\oplus q$.
<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/image-20260321150545867.png" alt="image-20260321150545867" style="zoom:50%;" />
</div>

???+ tip "Supplement"

	**NOR**(not or, 或非): $p \downarrow q \equiv \neg(p \vee q)$.

	**NAND**(not and, 与非): $p \mid q \equiv \neg(p \wedge q)$.

**conditional statement**(implication, 蕴含): $p\to q$ .
<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/image-20260321150551483.png" alt="image-20260321150551483" style="zoom:50%;" />
</div>
The statement p is called the **hypothesis**(假设), q is called the **conclusion**(结论).

!!! info "Related Conditional Statements"

	+ converse(逆命题): $q\to p$
	+ inverse(否命题): $\neg p\to\neg q$
	+ contrapositive(逆否命题): $\neg q \to \neg p$

!!! abstract "Equivalent Forms in English"

	<div style="text-align: center; margin-top: 15px;">
	<img src="Chap1.assets/image-20260321150150685.png" alt="image-20260321150150685" style="zoom:50%;" />
	</div>
	
	**Implication Law**: $p\to q\equiv \neg p \vee q$


**biconditional**(equivalence, 等价): $p\leftrightarrow q$​.

<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/image-20260321152151178.png" alt="image-20260321152151178" style="zoom:50%;" />
</div>

#### Precedence

<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/image-20260321152335997.png" alt="image-20260321152335997" style="zoom:50%;" />
</div>

#### Bit Expression
**bit**: A binary digit 0 (false) or 1 (true). 

boolean variable: A variable whose value is either true or false. A boolean variable can be represented by a bit.

bit string: A sequence of bits. The length of bit string is the number of bits.

bit operations: Logical operations used on bits. Bitwise operations are bit operations used on strings with same length and operate for their every bit.

+ bitwise OR
+ bitwise AND
+ bitwise XOR

## Applications of Propositional Logic
### Translating English Sentences
1. Identify atomic propositions and represent using propositional variables.
2. Determine appropriate logical connectives.

### System Specifications
**consistency**: A list of proposition is consistent if it is possible to assign truth values to the proposition variables so that each proposition is true.

### Logical Circuit
Propositional logic can be applied to the design of computer hardware. 

Logic circuit or digital circuit receives input signals and produces output signals.

![image-20260321154732599](Chap1.assets/image-20260321154732599.png)
## Propositional Equivalences
### Logical Equivalences
**tautology**(永真式/重言式): A compound proposition that is always true.

**contradiction**(永假式/矛盾式): A compound proposition that is always false.

**contingency**(偶真式): A compound proposition that is neither a tautology nor a contradiction.

The compound propositions $p$ and $q$ are called **logically equivalent** if $p\leftrightarrow q$ is a tautology, noted by $p\equiv q$.

!!! note "Important Logical Equivalences"

	Exclusive OR:

	+ $p\oplus q\equiv(p\vee q)\wedge\neg(p \wedge q)$
	+ $p\oplus q\equiv(p \wedge \neg q)\vee (\neg p\wedge q)$

		<div style="text-align: center; margin-top: 15px;">
		<img src="Chap1.assets/image-20260321160615977.png" alt="image-20260321160615977" style="zoom: 50%;" />
		</div>
		
		<div style="text-align: center; margin-top: 15px;">
		<img src="Chap1.assets/image-20260321160642043.png" alt="image-20260321160642043" style="zoom:50%;" />
		</div>
		
		<div style="text-align: center; margin-top: 15px;">
		<img src="Chap1.assets/image-20260321160714908.png" alt="image-20260321160714908" style="zoom:50%;" />
		</div>

### Using De Morgan’s Laws
De Morgan's Laws:

+ $\neg(p\wedge q)\equiv\neg p \vee \neg q$
+ $\neg(p\vee q)\equiv\neg p \wedge \neg q$

Extension:

+ $\neg(\bigvee_{i=1}^{n}p_{i})=\bigwedge_{i=1}^{n}\neg p_{i}$
+ $\neg(\bigwedge_{i=1}^{n}p_{i})=\bigvee_{i=1}^{n}\neg p_{i}$

### Satisfiability
**Satisfiability**: A compound proposition is satisfiable if there is an assignment of truth values to its variables that makes it true (like consistency).

> satisfiability = contingency + tautology

### Normal Form
**Simple Disjunction**/Basic Sum(简单析取式): A disjunction with finite proposition variables or their negation.

+ $\neg P \vee Q \vee R$, $\neg P \vee P$.

**Simple Conjunction**/Basic Product(简单合取式): A conjunction with finite proposition variables or their negation.

+ $\neg Q \wedge R \wedge Q$, $\neg P \wedge P$.

**Disjunctive Normal Form**/DNF(析取范式): A disjunction with finite simple conjunctions.

+ $P\vee (P\wedge Q)\vee(\neg P\wedge \neg Q\wedge \neg R)$, $P\vee Q\vee R$.

**Conjunctive Normal Form**/CNF(合取范式): A conjunction with finite simple disjunctions.

+ $(P \vee Q) \wedge \neg Q \wedge (Q \vee \neg R \vee S)$, $P \wedge Q \wedge R$.

!!! quote "Existence Theorem of Normal Forms(范式存在性定理)"

	For any propositional formula, there exists an equivalent formula in **Disjunctive Normal Form (DNF)** and an equivalent formula in **Conjunctive Normal Form (CNF)**.
	
	Steps:
	
	1. Elimination of $\to$ and $\leftrightarrow$: Replace $P\to Q$ with $\neg P \vee Q$, $P\leftrightarrow Q$ with $(P\to Q)\wedge(Q \to P)$.
	2. De Morgan's Laws: Move negations inward so they only apply to atomic variables.
	3. Double Negation Law: Replace $\neg \neg P$ with $P$.
	4. Distributive Laws: 
   
      	+ To get DNF, Distribute $\wedge$ over $\vee$: $P\wedge (Q \vee R)\equiv (P \wedge Q) \vee(P \wedge R)$ 
    	+ To get CNF, Distribute $\vee$ over $\wedge$: $P\vee (Q \wedge R)\equiv (P \vee Q) \wedge(P \vee R)$  

**The problem**: DNF/CNF are not unique.

**Minterm**(极小项): A minterm of $n$ variables is a **conjunction** of all $n$ variables, where each variable appears exactly once in either its direct form $P$ or its negation $\neg P$.

???+ example "Example"

	For $P,Q,R$ in a formula:
	
	+ $P \wedge Q \wedge\neg R$ is minterm.
	+ $P \wedge Q$ is not minterm, because $R$ is excluded.
	+ $P \wedge Q \wedge R \wedge \neg P$ is not minterm, because $P$ appears twice.

A minterm evaluates to True for **exactly one** combination of variable assignment, and evaluates to False for other $2^{n}-1$ combinations.

Minterms are conventionally denoted by $m_i$, where the subscript $i$ is the decimal equivalent of the binary string formed by the variables.

<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/image-20260321171540400.png" alt="image-20260321171540400" style="zoom:50%;" />
</div>

**Principle DNF**(主析取范式): A disjunction of minterms.

+ $(P\wedge Q)\vee(\neg P \wedge R)$ is DNF, but not PDNF.
+ $(P \wedge Q \wedge \neg R)\vee(\neg P \wedge Q \wedge Q)$ is PDNF, also DNF.

!!! quote "Theorem"

	For any propositional formula, there exists a unique equivalent PDNF.

	A PDNF of a proportional formula is the **disjunction** of the **minterms** that correspond to the rows where the formula evaluates to **True**.

	> How to construct PDNF?

	Method 1: The Truth Table Method 

	1. Construct the complete truth table for the formula.
	2. Write the minterm for each true rows.
	3. Connect the minterms with disjunction.

	<div style="text-align: center; margin-top: 15px;">
	<img src="Chap1.assets/image-20260321173214588.png" alt="image-20260321173214588" style="zoom:50%;" />
	</div>

	Method 2: The Equivalence Calculus Method

	1. Transform the formula into DNF
	2. If a simple conjunction is missing a variable (say $R$), multiply it by a tautology($R \vee \neg R$), then expand it using the Distributive law.
	3. Remove duplicate minterms using the Idempotent law($A \vee A \equiv A$).

	<div style="text-align: center; margin-top: 15px;">
	<img src="Chap1.assets/image-20260321173230872.png" alt="image-20260321173230872" style="zoom:50%;" />
	</div>

**Maxterm**(极大项): A maxterm of $n$ variables is a **disjunction** of all $n$ variables, where each variable appears exactly once in either its direct form $P$ or its negation $\neg P$.

A maxterm evaluates to False for **exactly one** combination of variable assignments, and evaluates to True for the other $2^n - 1$ combinations. 

Maxterms are conventionally denoted by $M_i$. The subscript $i$ is the decimal equivalent of the binary string. The binary string should make the propositional formula false.

<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/image-20260321175039694.png" alt="image-20260321175039694" style="zoom:50%;" />
</div>

**Principle CNF**(主合取范式): A conjunction of maxterms.

!!! quote "Theorem"

	For any propositional formula, there exists a unique equivalent CDNF.

	The PCNF of a propositional formula is the **conjunction** of the **maxterms** that correspond to the rows where the formula evaluates to **False**.

	> How to construct PCNF?

	Method 1: The Truth Table Method 

	1. Construct the complete truth table for the formula.
	2. Write the maxterm for each false rows.
	3. Connect the maxterms with conjunction.

	<div style="text-align: center; margin-top: 15px;">
	<img src="Chap1.assets/image-20260321175136454.png" alt="image-20260321175136454" style="zoom: 50%;" />
	</div>

	Method 2: The Equivalence Calculus Method
	
	1. Transform the formula into CNF
	2. If a simple disjunction is missing a variable (say $R$), multiply it by a contradiction($R \wedge \neg R$), then expand it using the Distributive law.
	3. Remove duplicate maxterms using the Idempotent law($A \wedge A \equiv A$).

	<div style="text-align: center; margin-top: 15px;">
	<img src="Chap1.assets/image-20260321175719974.png" alt="image-20260321175719974" style="zoom:50%;" />
	</div>

## Predicates and Quantifiers
### Predicates
predicate(谓词): Propositions which contain variables. When its variables bound by assigning it a value or an object from the **domains of discourse**(论域), predicates become propositions.

We can also regard predicate as propositional function. The result of applying a predicate $P$ to a constant $a$ is the proposition $P(a)$, to a variable $x$ is the proposition form $P(x)$.
### Quantifiers
**universal quantifiers**(全称量词): $\forall$.

$\forall xP(x)$ means: "For all $x$, $P(x)$".

**existential quantifiers**(存在量词): $\exists$.

$\exists xP(x)$ means: "For some $x$, $P(x)$".

**uniqueness quantifiers**(唯一存在量词): $\exists!$.

$\exists!xP(x)$ means: "There is one and only one $x$ such that $P(x)$".

> The uniqueness quantifier is not really need as it can be expressed with universal quantifiers and existential quantifiers:
> 
> $\exists !xP(x)\equiv \exists x(P(x)\wedge \forall y(P(y)\to y=x))$.

If the domain of discourse is null, then

+ $\forall xP(x)$ is a tautology, because we can't find a counterexample.
+ $\exists xP(x)$ is a contradiction, because we can't find any $x$ that satisfies $P(x)$.

#### Quantifiers over Finite Domains
+ $\forall xP(x)=\bigwedge_{i=1}^{n}P(i)$.
+ $\exists xP(x)=\bigvee_{i=1}^{n}P(i)$.
#### Quantifiers with Restricted Domains
+ Universal Quantifier:

	+ Rule: For a universal quantifier, a restricted domain is expressed using **implication**($\to$).

	+ Example: $\forall x \in S, P(x)\equiv\forall x (x \in S \to P(x))$.

+ Existential Quantifier:

	+ Rule: For an existential quantifier, a restricted domain is expressed using **conjunction** ($\wedge$).

	+ Example: $\exists x \in S, P(x)\equiv\exists x (x \in S \wedge P(x))$.

### Property of Quantifiers
#### Binding Variables
+ When a quantifier is used on the variable $x$, we say that this occurrence of the variable is **bound**.

+ An occurrence of a variable that is not bound by a quantifier or set equal to a particular value is said to be **free**.
#### Nesting of Quantifiers

The order of different quantifiers cannot be changed arbitrarily.

<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/file-20260321203500287.png" style="zoom:67%;" />
</div>

!!! example "Example"
	
	Let $P(x,y):y>x$. 
	
	+ $\forall x\exists yP(x,y)$: There isn't the biggest number.
	+ $\exists y \forall xP(x,y)$: The biggest number exists.
	Changing the order of quantifiers completely changes the meaning of the proposition.

#### Logical Equivalences Involving Quantifiers 
Statements involving predicates and quantifiers are **logically equivalent** iff they have the **same truth value** no matter which the predicates an the domain of discourse.

#### Negating Quantified Expressions
De Morgan's Laws for Quantifiers:

<div style="text-align: center; margin-top: 15px;">
<img src="Chap1.assets/image-20260321204423340.png" alt="image-20260321204423340" style="zoom:50%;" />
</div>

> Supplement:
> 
> + $∀x(A(x)∧B(x))≡∀xA(x)∧∀xB(x)$
>+ $∃x(A(x)∨B(x))≡∃xA(x)∨∃xB(x)$
>
> But notice that the following formula can only be derived in one direction:
> 
> + $∀x(A(x)∨B(x)) ⇐∀xA(x)∨∀xB(x)$
> + $∃x(A(x)∧B(x))​⇒∃xA(x)∧∃xB(x)$
#### Some Shorthands
+ $\exists x\exists y\exists  z\,P(x,y,z) \leftrightarrow_{\text{def}}\exists xyz\,P(x,y,z)$.
+  $\forall  x\forall  y\forall   z\,P(x,y,z) \leftrightarrow_{\text{def}}\forall xyz\,P(x,y,z)$.
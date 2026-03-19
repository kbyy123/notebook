# Set
## Definition
A set is a collection of objects, where the order and the repetition do not matter. The objects are called elements of members of the set. If $x$ is an element of $A$, we denote it by $x \in A$, otherwise $x\notin A$.

## Relations between Sets
### Subset and Proper Subset
If every element of set $A$ is also in set $B$, then we say that $A$ is a subset of $B$, denoted by $A\subseteq B$. If $A$ is a subset of $B$ and excludes at least one element of $B$, then we say that $A$ is a proper subset of $B$, denote by $A\subset B$.

### Contain
The relation "contain" is the inverse relation of subset, which means that if $A\subseteq B$, then we say that $B$ contains $A$ or $B$ is a superset of $A$, denoted by $B \supseteq A$.

### Equal
If $A\subseteq B$ and $B\subseteq A$, then we say that $A$ equals to $B, denoted by $A=B$.

### Disjoint
If $A$ and $B$ have no common elements, i.e. $A\cap B = \emptyset$, we say that $A$ and $B$ are disjoint.

## Operations between Sets
### Cardinality
We call the size of a set as its cardinality, denote by $|A|$. There is a unique set which cardinality is $0$, called **empty set**, denote by $\emptyset$. 

A set can also have infinite element.
### Union
The union of a set $A$ and a set $B$, denoted by $A\cup B$, is the set containing all elements which are in either $A$ or $B$ or both. 

### Intersection
The intersection of a set $A$ and a set $B$, denoted by $A\cap B$, is the set containing all elements which are both $A$ and $B$. 

### Complements
The **relative complement** of $A$ in $B$, or the **set difference** between $B$ and $A$, denoted by $B-A$ or $B\setminus A$, contains all elements in $B$ but not in $A$, i.e. $B\setminus A = \{x\mid (x \in B)\land(x \notin A) \}$.

### Product
The **Cartesian product** (also called the **cross product**) of two sets $A$ and $B$ is a set of all pairs whose first component is an element of $A$ and second component is an element of $B$, i.e. $A \times B = \{ (a,b) \mid a \in A,b \in B\}$.

### Power Sets
The power set of a set $S$, denotes by $\mathcal{P}(S)$, is a set of all subset of $S$: $\{T: T\subseteq S\}$. Evidently $|\mathcal{P}(S)|=2^{|S|}$.

## Significant Sets
In mathematics, some sets are referred to so commonly that they are denoted by special symbols. These include:

+ $\mathbb{N}$: The set of all natural numbers.
+ $\mathbb{Z}$: The set of all integer numbers.
+ $\mathbb{Q}$: The set of all rational numbers.
+ $\mathbb{R}$: The set of all real numbers.
+ $\mathbb{C}$: The set of all complex numbers.
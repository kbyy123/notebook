# Chap3 Algorithms

## Algorithms

**Def.** A procedure that follows a sequence of steps that leads to the desired answer.

??? quote "Features of Algos"

    + *input*. Information or data that comes in.
    + *Output*. Information or data that goes out.
    + *Definiteness*. Algorithm is precisely defined.
    + *Correctness*: Outputs correctly relate to inputs.
    + *Finiteness*: Won’t take forever to describe or run.
    + *Effectiveness*: Individual steps are all do-able.
    + *Generality*: Works for many possible inputs.
    + *Efficiency*: Takes little time & memory to run.

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


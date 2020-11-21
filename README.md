# OpenDSPL Overview
OpenDSPL is a minimalistic semi-functional event-based digital signal processing
programming language. Its syntax is heavily influenced by Lisp, Rust and Faust (
another DSP language). The interpreter architecture is heavily influenced by 
Reaktor (an event-based visual DSP language).
## Language Features
### OpenDSPL is Semi-Functional
What makes DSPL not purely functional is the delay operator "`@`" which allows 
access to prior states of a variable, but which is importantly read-only (thus 
preserving some benefits of a purely functional language). Programmers should 
beware of the fact that even if not using the "`@`" operator, the standard 
library functions might do; however the core language (that is if no libraries 
are included) is entirely implemented without the use of this operator, allowing 
some programmers the possibility of a purely functional experience.
### Event-Based Computing
OpenDSPL makes use of an event system, eliminating the necessity for loops. 
Iteration is obtained by feeding an event source into a function, thus calling 
the function as many times as an event is sent out. Events can themselves 
contain values (and this is in fact how I/O is modelled) which makes them useful
for indexing purposes.

The core language does not come with any loop constructs for this reason, 
however if one might want to make use of more traditional for loops, one can 
make use of the standard library function `for()`, a functional version of the 
imperative for statement.
### Atomic Syntax
The syntax of DSPL is made so as to minimize the amount of keywords the 
programmer must learn. In fact the list of all keywords is fairly short:
+ `number`
+ `process`
+ `record`
+ `module` (not implemented)
+ `import` (not implemented)
+ `int`
+ `float`
+ `byte`
+ `bool`

Instead, clever use of operators allows for expressive, concise and idiomatic 
code. For example, without using the standard library, if statements do not 
exist natively, although it is extremely simple to perform the same 
functionality:
```rust
if: bool = some_boolean_expression;
then: int = some_expression;
else: int = some_other_expression;
result: int = if(then, else);
```
This makes use of the fact that boolean variables are callable in OpenDSPL. 
Booleans take two expressions as parameters and returns the first if the value 
of the boolean is true and returns the second if the value is false.
# Language Specification
## Fundamental Principles of The Grammar
1. Every statement produces or modifies a symbol, no statement can be a raw
expression. At interpretation type, the program is thus converted into a list of
symbols.
2. Pieces of code that do not get executed, do not exist at interpretation time.
3. Pieces of code that do not modify or produce an output do not get executed,
thus, by rule 2, they don't exist.
4. Inputs produce events, outputs consume them. Any event must be consumed
eventually. Any output will not produce anything if no event is fed to it.
## Simple Expressions
Expressions use prefix syntax:
```rust
a: int = (- (+ (* 2 3) 5) 7)
```
## Processes (Lambda Expressions / Closures)
Functions in OpenDSPL are always closures. They are completely blind to the
calling scope and do not have side-effects (the delay operator being one major 
exception!).
```rust
foo: process = (a: int, b: int) -> int { return + a b; };
x: int = foo(1, 2);
```
## Delay Operator
The delay operator allows you to access prior values of a variable. Importantly,
the operation is read-only, meaning that even though state is conserved between
function calls, functions still don't have side-effects. This operator was
taken from the delay operator in the faust programming language.
```rust
prev_a = (@ a 1);
```
Stores the previous value of a.

This allows to easily implement integral and differential calculus:
```rust
diff: process     = (x: float) -> float { return (- x (@ x 1)); };
integral: process = (x: float) -> float { return (+ x (@ x 1)); };
```
You might have noticed that the state is bound to the scope where the variable
is accessed, meaning that the variable x is only addressable with the delay
operator within the scope of the lambda, importantly the variable can be
accessed independently by separate calls to the same function, meaning that no
state is leaked between parallel calls to the lambda. The delay operator is
completely blind to whatever happens on a separate event-stream.
## Records (Structs / Static Objects)

## Conditionals

## Iterators (Not Yet Implemented)


# Planned Features
+ clocks
+ modules and imports
+ full type support
+ full file support
+ standard library
+ type casting
+ threaded support
+ callable integer literals (function self-composition)
+ \<number\> template types
# Future Developments
OpenDSPL will forever remain open-source. However a more extensive and robust
language will be made in the future, if funding and interest are available.

A compiler to an IR language should be made.
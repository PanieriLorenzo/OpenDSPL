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
+ `number` (not implemented)
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
1. Variables are immutable.
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

## Plug Operator (Function Composition)
Passing the output of a process into an input of another process can sometimes
be verbose and hard to read, for this reason the plug operator `->` was introduced.
Instead of writing something like this:
```rust
some_variable = foo(bar(baz(some_input)));
```
We can write something like:
```rust
some_variable = some_input -> baz() -> bar() -> foo();
```
Which is considerably more readable. Another advantage of the plug operator is
making signals (that is valued event streams) be visually distinguishable from 
parameters (static values):
````rust
some_input: source;
some_param: int = 10;
...
some_output = some_input -> foo(some_param);
````
Here it is clear that `some_param` is not in the event stream, but rather is used
to modify an event stream. Keep in mind that the above code is semantically
identical to the following:
````rust
...
some_output = foo(some_input, some_param);
````
And in fact, there is no requirement for using plug operators to distinguish
signals and constants. For example in a low pass filter, one might want to
automate a parameter, this would make that parameter an event stream, however
keeping it as an explicit parameter would still clarify that the automation is
somehow subordinated to the audio signal being filtered.

The plug operator shows its power in long effect chains:
````rust
some_out = some_in -> fx1(a,b) -> fx2(c,d) -> fx3(e,f) -> fx4(g, h) -> fx5(i, j); 
````
Which would be quite unwieldy in a more traditional notation:
````rust
some_out = fx5(fx4(fx3(fx2(fx1(some_in, a, b), c, d), e, f), g, h), i, j);
````
### How The Plug Operator Works
The plug operator `->` works by associating a value on the left of it to the
first parameter of the function on the right. In case the right side is an
expression, the plug operator looks for the placeholder identifier: `_`.
Essentially the plug operator is performing substitution. Here the plug operator
is used in an expression:
````rust
some_variable = some_other_variable -> (* _ 2);
````
**(The following is not yet implemented!)**\
Plugging multiple parameters is also quite easy:
````rust
foo: process = (in1: int, in2: int, param: int) -> int {...};
aux = some_in1 -> foo(,2);
some_out = some_in2 -> aux;
````
When a parameter in a process call is left empty, the process returns an expression
where that parameter is left undefined. Then applying the plug operator again
will substitute the undefined parameters left to right (in this case there is
only one). This is essentially an alternative notation for currying.
In case many parameters are left undefined, the expression returned by the process
might look something like this:
````rust
(/(*(+ _ __) 3) ___)
````
Here the placeholders `_, __, ___` are always associated left to right when
adressed with a plug expression.

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

### Support Variable Generation
Normally variables that are not delayed (i.e. they don't carry their value across
scopes) do not need their names changed for disanbiguation, except that an underscore
is pre-pended to their names (why this is necessary will be explained later).

However when synthesizing code for the delay operator `@`, the compiler needs to
create support variables, and in the scenario in which these happen to get the
same names of already existing variables, obscure and hard-to-debug errors might
occur, therefore a robust dynamic naming system is needed.

Firstly we need something that will distinguish ordinary variables from support
variables, this is achieved by prepending delay variables with an underscore and
then some digits, and prepending the normal variables with just an underscore.
This is sufficient because variable names cannot start with a digit.
A variable called `foo` might generate a dynamic variable `_0001foo` when delayed
by 1 sample, so to create a conflict one would have to call another variable
`0001foo` but this is not allowed as the name starts with a digit.

Furthermore we need to take into consideration the case in which the delay variable
is generated within a function's scope. In this case, the variable might conflict
with another delay variable already existing in the parent scope. Therefore we
can use the number to disambiguate between variables from different scopes. In this
case we use the first *n* digits to store a sequential scope counter, which is
increased by 1 whenever entering into a scope, and *not* decreased when leaving,
as to prevent two calls to the same function conflicting. This limits the number
of function calls to whichever maximum integer value the compiler's language, 
supports, this **might create conflicts in some edge-cases** and could be
thought as a **possible exploit entry-point** but for now we won't worry about it
too much, as the language for this compiler (Python 3) has no upper bound to the
size of integers.

Lastly we need to distinguish between different delay depths of the same variable,
here we use the last two digits to represent this, as delays of depth bigger than
31 are stored in a different manner (a deque) and all have a depth counter of 00.

Representing these two integers as base32 characters and prepending with a 0 to
maintain protection against user-made variables allows us to save some characters
and avoid unnecessarily verbose variable names. It also allows to use one digit
for the depth rather thatn 2.

The scheme for generating variable names is the following:

Given an expression: `expr_name @ 1`
+ delay input variable name: `_0aa_expr_name`
+ delay output variable name: `_0ab_expr_name`

The code generated by the compiler will look something like this:

Given a statement: `b: float = (a + 1.0)@1 + 3.0`\
`expr_name` will instead be: `_a_add_1p0` according to the expression naming
scheme (see below)
```Rust
// [..] delay parameter definition
_0ab__a_add_1p0: f32;

// [..] delay parameter initialization
_0ab__a_add_1p0: 0.0;

// [..] main body of code
let _0aa__a_add_1p0: f32 = a + 1.0;
let _b: f32 = this._0ab__a_add_1p0 + 3.0;

// [..] post-processing body of code
this._0ab__a_add_1p0 = _0aa__a_add_1p0;
```

To achieve this, some special care is needed for the part of the semantic analyzer
that handles delay operators. Firstly an additional symbol is added directly to
the symbol table of the compiler, this represents the additional delay variables.
(Using the expression above), the symbol for delay has these generic fields:
+ `expr_name = "_a_add_11p0"` Is the symbolic conversion of the expression before
    the delay operator.
+ `type = DELAY` Marks this as a delay variable, to be handled accordingly by the
    compiler
+ `value = "a + 1.0"` Is the code equivalent of the symbolic representation
+ `is_delay = True` Tells the compiler this is a delay.

Because this is of type `DELAY`, the compiler expects these additional fields:
+ `depth = 1` Is the depth of the delay.
+ `scope_seq = 0` Integer representation of the scope sequence number

Then the `+ 3` expression receives a different symbol, this time it is an ordinary
integer expression symbol:
+ `expr_name = "__a_add_11p0_dly_1"` Expression symbolic representation
+ `type = E_FLOAT`
+ `value = "this._0ab__a_add_11p0 + 3.0"`
+ `is_delay = False`

**TODO:** some of this might have to change when functions are added. Code
generation becomes more complex as delay variables have to be added to funciton
parameters. This can be handled by creating a special function symbol with
additional metadata to aid code generation.

### Expression naming scheme
Expression naming follows this structure:
`_lhs_op_rhs`
Where lhs is the left operand (might be absent in case of unary operations) and
rhs is the right hand side operand. Op is a codeword for the operation.

Expression names are inherited by later expressions, which is why the left-most
underscore is important. It is used to distinguish sequences of operations with
different order of operations:

+ `a*(b + c)` becomes `__a_1mul_b_1add_c`
+ `a*b + c` becomes `_a_1mul_b_1add_c`

The operator codes are the following:
+ `+` becomes `1add`
+ `-` becomes `1sub`
+ `*` becomes `1mul`
+ `/` becomes `1div`
+ `%` becomes `1mod`
+ `@` becomes `1dly`
+ `->` becomes `1plg`
+ TODO: continue this list

Notice the 1 before each code, this is to prevent users for naming a variable the
same as one of these codes.

The obscurity of these code names as well as the naming conventions in the delay
generator have the unintended (but sometimes desirable) side-effect of obfuscating
the output code. This is obviously not the best if one wants to modify the output
code, but it is an advantage if the output is compiled directly to binary to
protect from de-compilation, or as an extra layer of obscurity on top of the
proprietary object files.

In case one of the operands is a literal, these conversions are made: 
+ `3.14` becomes `13p14`
+ `-2` becomes `1m2`
+ `false` becomes `1f`
+ `true` becomes `1t`

## Conditionals
Booleans are callable, this is the preferred method of performing conditional
statements.
```rust
foo: bool = some_boolean_expression;
then: int = some_expression;
else: int = some_other_expression;
result: int = foo(then, else);
```
## Iterators (Not Yet Implemented)
Iterators send out N events for every incoming event. These are not implemented
yet.

## Manifest
The manifest file is used to decide a few parameters in the compilation process.
It follows the `.toml` format:
```toml
[module_info]
name = "test"
inputs = 2
outputs = 2

[ui.<id>]    # sets names to the different ui elements based on id
name = "parameter name"

[options]               # changes the semantic analyzer's behavior
debug = true        # enables debugging in the arpeggio parser and AST
target = "rust_vst" # compile to Rust code with vst framework
fp_precision = "low"   # floating point precision: 32 or 64

[target.<target_name>]    # settings specific for the target <target_name>, for
                          # example, the rust compile:
[target.rust_vst]
partial = false     # if set to true, the generated rust code isn't compiled to
                    # binary
opt_level = 3       # optimization level (passed to Cargo toml)
lto = true          # link-time optimization (passed to Cargo toml)

[target.dspl_object]    # runnable object file

```

## Core Library
The core library is written in Rust with vst framework and isn't compiled, any new 
target in a different language needs to re-implement these. It is kept at a bare
minimum, resembling the Reaktor core atoms for the most part.
```Rust
// prototype:   i_to_f(x: int) -> (y: float)
// description: casts integer to float
x as f32;

// prototype:   f_to_i(x: float) -> (y: int)
// description: casts float to integer
x as i32;

// prototype:   ui_raw(id: int) -> (y: float)
// description: adds a parameter to the user interface, returns x in [0; 1]
// [...] some code omitted
this.params._1.get(); 
// [---] some code omitted

// prototype:   i_abs(x: int) -> (y: int)
// description: returns the absolute value of x
x.abs();

// prototype:   f_abs(x: float) -> (y: float)
// description: returns the absolute value of x
x.abs();

// prototype:   log(x: float, b: float) -> (y: float)
// description: returns the base b log of x
x.log(b);

// prototype:   exp(x: float) -> (y: float)
// description: returns the base e exponential of x
x.exp();

// prototype:   f_pow(a: float, b: float) -> (y: float)
// description: returns a^b
a.powf(b);

// prototype:   i_pow(a: int, b: int) -> (y: int)
// description: returns a^b
a.powi(b);

// prototype:   sqrt(x: f32) -> (y: f32)
// description: returns sqrt(x)
x.sqrt(x);

// you get the gist of the prototypes, here's a bunch
x.sin();
x.cos();
x.asin();
x.acos();
// all other trig and hyp functions can be derived and are not core

// prototype:   i_if(cond: bool, t: int, f: int) -> (x: int)
// description: if statement
if(cond) {
    t
} else {
    f
};

// prototype:   f_if(cond: bool, t: float, f: float) -> (x: float)
// description: if statement
if(cond) {
    t
} else {
    f
};

// prototype:   itr(num: int) -> (idx: int)
// description: for loop, generates num indexes, from zero to num-1
//      feeding it into any expression makes the expression part of the loop
//      e.g:
//      i: int = itr(5);
//      a: [float] = i_to_f(i) -> sin();
for i in 0..num{
    /* some code */
}
```

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

The semantic analyzer creates some Rust code along the way, which makes impossible
to use the code abstractions it produces to generate other languages. Either
find a way to fully abstract everything (expressions as lists of operations in
an IR language) or make a special class that creates the small snippets along
the way, which can be swapped for a different one for another language.

The IR language path seems the best. One can use the IR to represent expressions
but leave as much as possible as an abstraction.

## ExpressIRL
An IR language for representing expressions. Example:
`c*(a + b)` becomes:
```asm
ON $a
ADD $b
MUL $c
```
Whereas the delay expression `(c*(a + b))@1 + 1.0` becomes:

`_c_mul_a_add_b` =
```asm
ON $a
ADD $b
MUL $c
```
Which is used to generate the delay variable, and the rest of the expression
becomes:

`___c_mul_a_add_b_dly_1_add_1p0` =
```asm
ON $_0ab_c_mul_a_add_b
ADD f1.0
```

With this additional form of representation, the entirety of the code can be
saved as a runnable abstraction, which is essentially a table of symbols, of which
some contain nested tables (for functions). All simple symbols would just be
a single string containing some ExpressIRL code, and then it could be written to
a proprietary object file by serializing to json and encrypting.


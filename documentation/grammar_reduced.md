This grammar is a reduced version of the full OpenDSPL specification. This is for
development purposes, it represents the core functionality that should be focussed
on in development.

Some of the removed features include:
+ modules and imports
+ full type support
+ full file support (only supports raw and wave)
+ standard library (only supports core processes)
+ infix notation
+ type casting
+ threaded support
+ callable literals (church encoding of integers)
+ \<number\> template types

## fundamental principles of the grammar
1. Every statement produces or modifies a symbol, no statement can be a raw
expression. At interpretation type, the program is thus converted into a list of
symbols.
2. Pieces of code that do not get executed, do not exist at interpretation time.
3. Pieces of code that do not modify or produce an output do not get executed,
thus, by rule 2, they don't exist.

## Language features
OpenDSPL is a minimalistic semi-functional event-based programming language.

### semi-functionality
What makes DSPL not purely functional is the delay operator "`@`" which allows access to prior states of a variable, but which is importantly read-only (thus preserving some benefits of a purely functional language). Programmers should beware of the fact that even if not using the "`@`" operator, the standard library functions might do; however the core language (that is if no libraries are included) is entirely implemented without the use of this operator, allowing some programmers the possibility of a purely functional experience.

### event-based computing
OpenDSPL makes use of an event system, eliminating the necessity for loops. Iteration is obtained by feeding an event source into a function, thus calling the function as many times as an event is sent out. Events can themselves contain values (and this is in fact how I/O is modelled) which makes them useful for indexing purposes.

The core language does not come with any loop constructs for this reason, however if one might want to make use of more traditional for loops, one can make use of the standard library function `for()`, a functional version of the imperative for statement.

### atomic syntax
The syntax of DSPL is made so as to minimize the amount of keywords the programmer must learn. In fact the list of all keywords is fairly short:
+ `number`
+ `process`
+ `record`
+ `module` (not implemented)
+ `import` (not implemented)
+ `int`
+ `float`
+ `byte`
+ `bool`

Instead, clever use of operators allows for expressive, concise and idiomatic code. For example, without using the standard library, if statements do not exist natively, although it is extremely simple to perform the same functionality:
```rust
if: bool = some_boolean_expression;
then: int = some_expression;
else: int = some_other_expression;
result: int = if(then, else);
```
This makes use of the fact that boolean variables are callable in OpenDSPL. Booleans take two expressions as parameters and returns the first if the value of the boolean is true and returns the second if the value is false.

## Planned features
<!-- TODO: -->


<!-- TODO: this is outdated! -->
```Py
############################
#                          #
#   Lexer / Parser rules   #
#                          #
############################
# Translation of raw code string into AST

# === basic rules ==============================================================
program     = statement*
statement   = (simp_stat / expr) _ ";"
simp_stat   = definition / assignment / init / return / "quit"
expr        = compound_expr / plug_expr

# === simple statements ========================================================
# these statements produce no value (i.e. they are not expressions)
definition  = identifier _ ":" _ type
assignment  = identifier _ "=" _ expr
init        = definition _ "=" _ expr
return      = "return" __ expr

# === expressions ==============================================================
plug_expr   = simp_expr
            / simp_expr _ "->" _ plug_expr
simp_expr   = term
            / unary_op _ term
            / binary_op __ term __ term
term        = literal
            / call
            / record_access
            / list_access
            / simp_expr
            / "(" _ simp_expr _ ")"
compound_expr   = lit_record
                / lit_list
                / lambda

# === types ====================================================================
type        = "int" / "float" / "byte" / "bool" / "record" / list / "process"
list        = "[" _ type _ "]"

# === operators, calls & access ================================================
unary_op    = "not" / "~" / "-"
binary_op   = "and" / "or" / "@" / "&" / "|" / "^" / "+" / "-" / "*" / "/" / "%"
call        = identifier _ "(" _ (plug_expr _ ("," _ plug_expr _ )* ) ")"
record_access   = identifier _ "." _ identifier
                / identifier _ "." _ record_access
list_access     = identifier _ "[" _ simp_expr _ "]"

# === literals =================================================================
literal     = lit_byte / lit_int / lit_float / lit_bool
lit_list    = lit_str
            / "[" _ identifier? _ ("," _ identifier _ )* "]"
lit_record  = "(" _ (definition / init) _ ("," _ (definition / init) _ )* ")"
lit_byte    = r"0[xX][0-9a-fA-F]+" / r"'([^']|\\')?'"
lit_int     = r"-?[0-9]+"
lit_float   = r"-?[0-9]*\.[0-9]+"
lit_bool    = r"true|false"
lit_str     = r'(?<!\\)".*?(?<!\\)"'

# === lambdas ==================================================================
lambda      = lmbda_param _ lmbda_ret? _ lmbda_block
lmbda_param = "(" _ definition? _ ("," _ definition _ )* ")"
lmbda_ret   = "->" _ type
            / "->" _ "(" type? _ ("," _ type)* ")"
lmbda_block = "{" statement* "}"

# === misc =====================================================================
comment     = r"#.*"
__          = r"\s+"   # mandatory whitespace
_           = r"\s*"   # optional whitespace

# === identifiers ==============================================================
identifier  = r"[a-zA-Z_]\w*"
```

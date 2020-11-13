# DSPL Grammar
This grammar is written in a PEG-like syntax.

```R
################################
#                              #
#   atomic lexemes (regexes)   #
#                              #
################################

# === misc =====================================================================
comment     = ~r"#.*"
_           = ~r"\s+"   # whitespace

# === identifier ===============================================================
identifier  = ~r"[a-zA-Z_]\w*"

# === type literals ============================================================
lit_byte    = ~r"0[xX][0-9a-fA-F]+"
lit_i       = ~r"-?[0-9]+"
lit_f       = ~r"?[0-9]*\.[0-9]+"
lit_c       = ~r"'([^']|\\')?'"
lit_bool    = ~r"true|false"
lit_str     = ~r'(?<!\\)".*?(?<!\\)"'


#############################
#                           #
#   abstract syntax rules   #
#                           #
#############################

# === general definitions ======================================================
program     = statement*
module      = "module" identifier block
block       = "{" program "}"
ignore      = comment+ / ws+
statement   = (no_eval / expr / module) ";"
                # no_eval is any statement that doesn't produce
                # a value, even if the value is NULL
no_eval     = simp_stat         # simple statement, like return and import
            / assignment        # variable assignment
            / definition        # variable declaration no assignment
            / init              # variable declaration and assignment
assignment  = identifier "=" (expr / lambda / str_expr / lit_record / lit_list) 
definition  = identifier ":" (identifier / type)    # support custom types
init        = definition "=" (expr / lambda / str_expr / lit_record / lit_list)
type        = number / record / process / list
number      = "number"
            / "byte" 
            / "i16" / "i24" / "i32" / "i64"
            / "u16 "/ "u24" / "u32" / "u64"
            / "f32" / "f64"
bool        = "bool"
simp_stat   = "import" namespace
            / "attach" namespace
            / "return" expr
expr        = bool_expr / math_expr / plug_expr 
namespace   = identifier
            / identifier "." namespace

# === bool expressions =========================================================
bool_expr   = bool_term
            / bool_term "or" bool_expr
bool_term   = bool_factor
            / bool_factor "and" bool_term
bool_factor = bool_cmp          # bool comparison
            / "not" bool_factor
            / lit_bool
            / call
            / list_access
            / record_access
            / identifier
            / "(" bool_expr ")"
bool_cmp    = math_expr ("<" / "<=" / "==" / "!=" / ">=" / ">") math_expr 

# === math expressions =========================================================
math_expr   = math_term
            / math_term ("+" / "-") math_expr
math_term   = math_power
            / math_power ("|" / "^" / "&" / "*" / "/" / "%" / "<<" / ">>") math_term
math_power  = math_factor
            / math_factor "**" math_power
math_factor = lit_number
            / "-" math_factor
            / "~" math_factor
            / call
            / list_access
            / record_access
            / identifier
            / identifier "@" math_expr
            / "(" expr ")"

# === string expression ========================================================
str_expr    = lit_str
            / lit_str '+' str_expr

# === plug expressions =========================================================
plug_expr   = (math_expr / bool_expr) "->" call
            / call "->" call

# === lambda expression ========================================================
lambda      = parameters returns? lambda_block
parameters  = "(" (definition ("," definition)* )? ")"
returns     = "->" type
            / "->" "(" (type ("," type)* )? ")"
lambda_block    = "{" statement* expr? "}"
                / "{" statement* "return" expr? ";" "}"

# === literals =================================================================
lit_number  = lit_byte / lit_i / lit_f / lit_c
lit_list    = 
lit_record  =
call        =
list_access =
record_access   =


######################
#                    #
#   Semantic Rules   #
#                    #
######################

# === predefined record types ==================================================
clock: record =         # used as an event clock, the most basic of sources, if
                        # no clock is used, nothing will execute
raw_source: record =    # reads a file as a stream of bytes, i16, i24 or f32
                        # with big or small endianness at a set sample rate
raw_sink: record =      # writes to a file as a stream of bytes, i16, i24 or f32
                        # with big or small endianness at a set sample rate

# === implicit casting =========================================================
# casting is not implemented, so incompatible types are not allowed
# what follows are examples of statements that are NOT valid
identifier: bool = <math_expr>
identifier: bool = <lambda>
identifier: <number> = <bool_expr>
identifier: <number> = <str_expr>
# and so on, instead only these are allowed:
identifier: bool = <bool_expr>
identifier: <number> = <math_expr>
identifier: process = <lambda>
identifier: list = <lit_list> / <lit_str>
identifier: record = <lit_record>

# === expression behavior ======================================================
# division by zero:
#   ignored by the parser, handled by the interpreter at evaluation time
# arithmetic with non-number variables:
#   not allowed, arithmetic operands must be numbers


```

## Interpreter Implementation
* All variables store expressions until a sink is written to, at which point
the expression is evaluated. The expressions are written in Python "exec" strings
to be executed when evaluated.
* Lambdas are simply expressions with placeholders for the variables, these are
filled in when the lambda is called.
* Delay operators force the interpreter to evaluate the variables and store them
in an array
* Variables accessed by a delay operator are stored as "tape loop" arrays with
size equal to the maximum delay value if this is known before execution, or a
set maximum buffer size set as a compuler flag, or just the maximum indexing
number the OS supports.
* Lambdas that don't return a value, either consume events without returning
them, or they raise an exception or a warning if a specific interpreter flag is
used.
* Delay operator accesses the values of all the previous events produced by a
variable. In this sense DSPL is state-less in a single time frame and state-full
across multuple time frames. I.e. DSPL is stateless across space but state-full
across time. Meaning that nothing in the future or in the present can affect what 
has already been computed, but the previous computations can affect the current 
ones. There are no side-effects across functions and modules, only from the same
functions to their past selves.

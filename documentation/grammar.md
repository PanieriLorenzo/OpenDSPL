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
ws          = ~r"\s+"

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
file        = statement*
module      = "module" identifier "{" (statement / module)* "}"
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
str_expr    =

# === plug expressions =========================================================
plug_expr   = (math_expr / bool_expr) "->" call
            / call "->" call

# === lambda expression ========================================================
lambda      =

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
raw_file: record =      # reads a file as a stream of bytes, i16, i24 or f32
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
```
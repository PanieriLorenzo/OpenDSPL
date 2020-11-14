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
lit_float   = r"?[0-9]*\.[0-9]+"
lit_bool    = r"true|false"
lit_str     = r'(?<!\\)".*?(?<!\\)"'

# === lambdas ==================================================================
lambda      = lmbda_param _ lmbda_ret? _ lmbda_block
lmbda_param = "(" _ definition? _ ("," _ definition _ )* ")"
lmbda_ret   = "->" _ type
            / "->" _ "(" type? _ ("," _ type)* ")"
lmbda_block = "{" statement* "}"

# === misc =====================================================================
comment     = ~r"#.*"
__          = ~r"\s+"   # mandatory whitespace
_           = ~r"\s*"   # optional whitespace

# === identifiers ==============================================================
identifier  = ~r"[a-zA-Z_]\w*"



######################
#                    #
#   Semantic rules   #
#                    #
######################
# semantic rules are implemented during a second pass on the AST produced by the
# parser

# === incompatible types =======================================================


# === undefined symbols ========================================================


# === const lookup table =======================================================


# === signal path definition ===================================================


#########################
#                       #
#   Interpreter rules   #
#                       #
#########################
# interpreter rules are only triggered at run-time

# === arithmetic errors ========================================================
# division by zero
# delay by negative number

# === identifier hash table ====================================================

# === expression stack / queue =================================================
```
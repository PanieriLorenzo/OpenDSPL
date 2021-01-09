"""OpenDSPL types. Used to represent code abstractly"""
__author__ = "Lorenzo Panieri"
__license__ = "MIT"
__version__ = "0.1.0-indev+1"
__status__ = "Development"

from enum import Enum
from typing import List

# type of symbol
# types prefixed with I are immediate values (literals)
# types prefixed with E are expressions returning the value in the type
# types prefixed with T are type specifiers
class Type(Enum):
    I_INT = 0
    I_FLOAT = 1
    I_BOOL = 2
    I_PROCESS = 3
    I_LIST = 4
    
    CODE = 10       # a formattable string containing partially compiled code
    IDENTIFIER = 15
    DELAY = 17

    E_INT = 20
    E_FLOAT = 21
    E_BOOL = 22
    E_PROCESS = 23
    E_LIST = 24

    T_INT = 30
    T_FLOAT = 31
    T_BOOL = 32
    T_PROCESS = 33
    T_LIST = 34

# a symbol is something that is assignable to a variable, or a variable itself
# an unassigned symbol simply has self.name == None
class Symbol:
    def __init__(self, type=None, value=None):
        self.expr_name = ""
        self.type = type
        self.value = value  # value is either literal or identifier name

        # delay parameters, these are only set within a delay operation visitor
        self.is_delay = False
        self.dly_depth = 0
        self.scope_seq = None


# ansi escape codes for coloring output
class CliC:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# operation names for expr_name generation
class ExprNames:
    BIT_NOT     = "1bno"
    MUL         = "1mul"
    DIV         = "1div"
    MOD         = "1mod"
    DELAY       = "1dly"
    ADD         = "1add"
    SUB         = "1sub"
    LSHIFT      = "1lsh"
    RSHIFT      = "1rsh"
    BIT_AND     = "1bnd"
    BIT_XOR     = "1bx"
    BIT_OR      = "1bor"
    LESS        = "1les"
    LEQ         = "1leq"
    GRT         = "1grt"
    GEQ         = "1geq"
    EQ          = "1eq"
    NEQ         = "1neq"
    NOT         = "1not"
    AND         = "1and"
    OR          = "1or"
    PLUG        = "1plg"

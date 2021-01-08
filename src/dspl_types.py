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
        self.type = type
        self.value = value  # value is either literal or identifier name

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


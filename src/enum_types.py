from enum import Enum

# type of symbol, all the types prefixed with I are immediate values
# expressions are trees of operations
# record are record structs
# list are python lists
class Type(Enum):
    I_INT = 0
    I_FLOAT = 1
    I_BOOL = 2
    I_STR = 3
    I_LIST = 10
    OP = 20
    STRUCT = 21
    BLOCK = 23
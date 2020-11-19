"""OpenDSPL types. Used to represent code abstractly"""
__author__ = "Lorenzo Panieri"
__license__ = "MIT"
__version__ = "0.1.0-indev+1"
__status__ = "Development"

from enum import Enum
from typing import List

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

# a symbol is something that is assignable to a variable, or a variable itself
# an unassigned symbol simply has self.name == None
class Symbol:
    def __init__(self, type=None, name=None, value=None):
        self.name = name
        self.type = type
        self.value = value

# an operation specifies how symbols or constants relate to each other
# this constitutes the majority of the nodes that form the expression tree
class Operation:
    def __init__(self, is_bin: bool, lhs: Symbol, rhs: Symbol = None, op=None):
        self.is_bin = is_bin
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
    
    # converts itself into a symbol either containing a numeric value or a 
    # symbol of operator type
    def toSymb(self):
        if self._isComputable():
            if self.is_bin:
                symb = None
                lhs = self.lhs.value
                rhs = self.rhs.value
                l_type = self.lhs.type
                r_type = self.lhs.type
                if l_type == r_type:
                    raise TypeError("Cannot implicitly cast types.")

                # TODO: call different methods for different types
                ret = self._op_exec_bin_math(self.op, self.lhs, self.rhs, l_type)
                if isinstance(ret, int):
                    symb = Symbol(type=Type.I_INT, value=ret)
                elif isinstance(ret, float):
                    symb = Symbol(type=Type.I_FLOAT, value=ret)
                return symb

            else:
                pass
        return Symbol(Type.OP, value=self)

    # true if the lhs and rhs have a value
    def _isComputable(self):
        if self.lhs.type not in (Type.I_INT, 
                                 Type.I_FLOAT, 
                                 Type.I_BOOL, 
                                 Type.I_STR):
            return False
        if self.is_bin and self.rhs.type not in (Type.I_INT, 
                                                 Type.I_FLOAT, 
                                                 Type.I_BOOL, 
                                                 Type.I_STR):
            return False
        return True
    
    def _op_exec_bin_math(op: str, lhs, rhs, type):
        if type == Type.I_INT:
            _lhs = int(lhs)
            _rhs = int(rhs)
        else:
            _lhs = float(lhs)
            _rhs = float(rhs)

        if op == "+":
            return _lhs + _rhs

        elif op == "-":
            pass

        elif op == "*":
            return _lhs * _rhs

        elif op == "/":
            pass

    def op_exec_un_math(op: str, lhs):
        pass

# a struct is simply a special symbol which contains multiple other symbols
# inside of it
class Struct:
    def __init__(self, members: List[Symbol], anonym=True):
        self.members = members
        self.anonym = anonym

# a block is a scoped piece of code. It is entirely self contained.
class Block:
    def __init__(self, statements: List[Symbol]):
        self.statements = statements
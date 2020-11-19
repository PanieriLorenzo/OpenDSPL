# === OPERATION EXECUTER =======================================================
# given an operator and one or two values, compute the return value

from enum_types import Type

def op_exec_bin_math(op: str, lhs, rhs, type):
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

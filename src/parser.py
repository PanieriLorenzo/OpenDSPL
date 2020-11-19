from os import name
from typing import List
from arpeggio import NoMatch, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG
from arpeggio import PTNodeVisitor
from enum import Enum
from dataclasses import dataclass
from op_exec import op_exec_bin_math
from enum_types import Type

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
                ret = op_exec_bin_math(self.op, self.lhs, self.rhs, l_type)
                if isinstance(ret, int):
                    symb = Symbol(type=Type.I_INT, value=ret)
                elif isinstance(ret, float):
                    symb = Symbol(type=Type.I_FLOAT, value=ret)
                return symb

            else:
                pass
        return Symbol(Type.OP, value=self)

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

class Visitor(PTNodeVisitor):
    def visit_program(self, node, children):
        statements = list()
        for child in children:
            statements.append(child[0])
        block = Block(statements)
        return block
    
    def visit_statement(self, node, children):
        return children
    
    def visit_init(self, node, children):
        symb = None
        # if type is a symbol, i.e. a custom type, rhs must be a record literal
        # else it must be some other type
        if isinstance(children[1], Symbol):
            if children[2].type == Type.STRUCT:
                symb = Symbol(type=Type.STRUCT, 
                              name=children[0].name,
                              value=children[2])
            else:
                raise TypeError("RHS is not a record literal")

        # int
        elif children[1] == "int":
            if children[2].type == Type.I_INT:
                symb = Symbol(type=Type.I_INT,
                              name=children[0].name,
                              value=children[2])
        
        else:
            raise TypeError("Unknown Type")

        return symb
    
    def visit_assignment(self, node, children):
        # TODO: handle assignment to records
        symb = Symbol(type=children[1].type, name=children[0].name, value=children[1].value)
        return symb
    
    def visit_identifier(self, node, children):
        symb = Symbol(name=node.value)
        return symb
    
    def visit_lit_int(self, node, children):
        symb = Symbol(type=Type.I_INT, value=int(node.value))
        return symb
    
    def visit_lit_record(self, node, children):
        struct = Struct(children)
        symb = Symbol(type=Type.STRUCT, value=struct)
        return symb
    
    def visit_lit_str(self, node, children):
        symb = Symbol(type=Type.I_STR, value=node.value[1:-1])
        return symb
    
    def visit_record_access(self, node, children):
        struct = Struct([Symbol(name=children[1].name)])
        symb = Symbol(type=Type.STRUCT, name=children[0].name, value=struct)
        return symb
    
    def visit_def_record(self, node, children):
        pass

    def visit_binary_expr(self, node, children):
        op = Operation(True, children[1], children[2], op=children[0])
        return op.toSymb()

with open('grammar_files/grammar_reduced.peg', 'r') as file:
    grammar = file.read() #.replace('\n', '')

with open('grammar_files/grammar_comment.peg', 'r') as file:
    comment = file.read()

with open('test_1.odspl', 'r') as file:
    input = file.read()

parser = ParserPEG(grammar, "program", comment, debug=False, autokwd=True, reduce_tree=True)
try:
    parse_tree = parser.parse(input)
except NoMatch as e:
    print("syntax error at: (Ln {}, Col {})".format(e.line, e.col))
    quit()

res = visit_parse_tree(parse_tree, Visitor(debug = False));
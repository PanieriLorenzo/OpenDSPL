"""OpenDSPL parser. lexes, parses and analyses raw code streams."""
__author__ = "Lorenzo Panieri"
__license__ = "MIT"
__version__ = "0.1.0-indev+1"
__status__ = "Development"

from typing import List
from arpeggio import NoMatch, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG
from arpeggio import PTNodeVisitor
from dspl_types import Type
import dspl_types as tp
import dspl_util as ut


#########################
#                       #
#   SEMANTIC ANALYZER   #
#                       #
#########################
# takes AST from parser, and produces a list of symbols

class Visitor(PTNodeVisitor):
    def __init__(self, **kwargs):
        self.scope_seq = 0
        self.symbol_table = []
        super(Visitor, self).__init__(**kwargs)
        
    
    # === DEFINITION ===========================================================
    def visit_definition(self, node, children):
        # validation: type and expr must have matching types
        pass

    # === DELAY EXPRESSION =====================================================
    # delay expressions are quite complex in terms of code generation, see the
    # documentation for an in-depth explaination of the rationale behind these
    # decisions
    def visit_delay_expr(self, node, children):
        # validation: lhs being constant is useless
        # TODO: check that if lhs is an identifier it has to be defined
        if(children[0].type == Type.I_BOOL
                or children[0].type == Type.I_FLOAT
                or children[0].type == Type.I_INT
                or children[0].type == Type.I_LIST
                or children[0].type == Type.I_PROCESS):
            print(f"{tp.CliC.WARN}Warning: delay operator near:{tp.CliC.ENDC}")
            print("    '... ", node.value, " ...'")
            print(f"{tp.CliC.WARN}does nothing. Consider removing it.{tp.CliC.ENDC}")
        
        # store delay variable
        dly_symb = tp.Symbol(tp.Type.DELAY, value = children[0])
        dly_symb.expr_name = "_0" \
                           + ut.to_base32(self.scope_seq) \
                           + ut.to_base32(0) \
                           + children[0].expr_name
        dly_symb.is_delay = True
        dly_symb.dly_depth = # TODO: depends on type of rhs
        dly_symb.scope_seq = self.scope_seq

        


    # === BITWISE NOT EXPRESSION ===============================================
    def visit_bit_not_expr(self, node, children):
        # validation: operands must be integers
        if(children[1].type != Type.IDENTIFIER 
                and children[1].type != Type.I_INT
                and children[1].type != Type.E_INT):
            print(f"{tp.CliC.FAIL}Semantic error near:{tp.CliC.ENDC}")
            print("    '... ", node.value, " ...'")
            print(f"{tp.CliC.FAIL}can only use '~' on integer operands!{tp.CliC.ENDC}")
            quit()
        
        # if operand is immediate value, calculate the value beforehand
        if(children[1].type == Type.I_INT):
            val = ~children[1].value
            symb = tp.Symbol(type=Type.I_INT, value= val)
            symb.expr_name = "__1"
            if val < 0:
                symb.expr_name += "m"
                val = -val
                symb.expr_name += str(val)
            return symb

        # if operand is identifier, check if identifier is defined, then generate
        # source code
        # TODO: check if undefined and int, then raise a semantic error
        lhs = ""
        rhs = children[1].expr_name
        symb = tp.Symbol(type=Type.E_INT, value= "!" + str(children[1].value) )
        symb.expr_name = ut.expr_name(lhs, rhs, tp.ExprNames.BIT_NOT)
        print(symb.expr_name)
        return symb
    
    # === PARENTHESIZED EXPRESSION =============================================
    # remove parentheses
    """
    def visit_paren_expr(self, node, children):
        if children[0] == '(':
            return children[1]
        return children[0]"""


    # === UNNAMED SYMBOLS (literals) ===========================================
    def visit_lit_int(self, node, children):
        symb = tp.Symbol(type=Type.I_INT, value= int(node.value))
        return symb
    
    def visit_lit_float(self, node, children):
        symb = tp.Symbol(type=Type.I_FLOAT, value= float(node.value))
        return symb

    def visit_true(self, node, children):
        return True
    
    def visit_false(self, node, children):
        return False

    def visit_lit_bool(self, node, children):
        symb = tp.Symbol(type=Type.I_BOOL, value= node.value)
        return symb


    # === NAMED SYMBOLS (identifiers) ==========================================
    # name generation scheme is the following:
    # _identifier_name
    # e.g if we run the following DSPL code:
    #     foo: int = 14;
    # we get the following Rust code:
    #     let _foo: i32 = 14;
    def visit_identifier(self, node, children):
        symb = tp.Symbol(type=Type.IDENTIFIER, value= "_" + node.value)
        symb.expr_name = "_" + node.value
        return symb

    # === RESERVED SYMBOLS =====================================================
    # these identifiers are reserved for core functionality

    # HACK: for now this just returns 1 as an integer for testing purposes
    def visit_dbg_in(self, node, children):
        symb = tp.Symbol(type=Type.I_INT, value= 1)
        return symb
    
    # HACK: for now this takes integers and prints them
    def visit_dbg_out(self, node, children):
        symb = tp.Symbol(type=Type.CODE, value= "println!(\"{{}}\", {});")
        return symb
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


#########################
#                       #
#   SEMANTIC ANALYZER   #
#                       #
#########################
# takes AST from parser, and produces a list of symbols

class Visitor(PTNodeVisitor):
    def __init__(self, **kwargs):
        self.scope_count = 0
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
            symb = tp.Symbol(type=Type.I_INT, value= ~children[1].value)
            return symb

        # if operand is identifier, check if identifier is defined, then generate
        # source code
        # TODO: check if undefined and int, then raise a semantic error
        symb = tp.Symbol(type=Type.E_INT, value= "!" + str(children[1].value) )
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
    # scope_name__identifier_name
    # e.g if we run the following DSPL code inside a function called "foo":
    #     bar: int = 14;
    # we get the following Rust code:
    #     let main__bar: i32 = 14;
    #
    # TODO: dynamically assign scope name
    def visit_identifier(self, node, children):
        symb = tp.Symbol(type=Type.IDENTIFIER, value= "main__" + node.value)
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
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

##########################################
#                                        #
#   LEXER / PARSER / SEMANTIC ANALYSIS   #
#                                        #
##########################################
# contains an instance of ParserPEG from the Arpeggio library and a PTNodeVisitor
# from the Arpeggio library
# produces a list of symbols as an output

class ParserDSPL:
    def __init__(self, grammar, root="program", dbg=False):
        self.parser = ParserPEG(grammar, root, comment_rule_name=None, debug=dbg, reduce_tree=True)
        self.parser.autokwd = True
    
    def parse(self, input: str, dbg=False):
        # === LEXING / PARSING =================================================
        try:
            parse_tree = self.parser.parse(input)
        except NoMatch as e:
            print("syntax error at: (Ln {}, Col {})".format(e.line, e.col))
            quit()
        
        # === SEMANTIC ANALYSIS ================================================
        return visit_parse_tree(parse_tree, Visitor(debug=dbg))


#########################
#                       #
#   SEMANTIC ANALYZER   #
#                       #
#########################
# takes AST from parser, and produces a list of symbols

class Visitor(PTNodeVisitor):

    # === BLOCK ================================================================
    def visit_program(self, node, children):
        statements = list()
        for child in children:
            statements.append(child[0])
        block = tp.Block(statements)
        return block
    
    # === STATEMENT ============================================================
    def visit_statement(self, node, children):
        return children
    
    # === INIT =================================================================
    def visit_init(self, node, children):
        symb = None
        # if type is a symbol, i.e. a custom type, rhs must be a record literal
        # else it must be some other type
        if isinstance(children[1], tp.Symbol):
            if children[2].type == Type.STRUCT:
                symb = tp.Symbol(type=Type.STRUCT, 
                              name=children[0].name,
                              value=children[2])
            else:
                raise TypeError("RHS is not a record literal")

        # int
        elif children[1] == "int":
            if children[2].type == Type.I_INT:
                symb = tp.Symbol(type=Type.I_INT,
                              name=children[0].name,
                              value=children[2])
        
        else:
            raise TypeError("Unknown Type")

        return symb
    
    # === ASSIGNMENT ===========================================================
    def visit_assignment(self, node, children):
        # TODO: handle assignment to records
        symb = tp.Symbol(type=children[1].type, name=children[0].name, value=children[1].value)
        return symb
    
    # === EXPRESSIONS ==========================================================
    def visit_binary_expr(self, node, children):
        op = tp.Operation(True, children[1], children[2], op=children[0])
        return op.toSymb()

    # === NAMED SYMBOL (identifier) ============================================
    def visit_identifier(self, node, children):
        symb = tp.Symbol(name=node.value)
        return symb
    
    def visit_record_access(self, node, children):
        struct = tp.Struct([tp.Symbol(name=children[1].name)])
        symb = tp.Symbol(type=Type.STRUCT, name=children[0].name, value=struct)
        return symb
    
    # === UNNAMED SYMBOLS (literals) ===========================================
    def visit_lit_int(self, node, children):
        symb = tp.Symbol(type=Type.I_INT, value=int(node.value))
        return symb
    
    def visit_lit_record(self, node, children):
        struct = tp.Struct(children)
        symb = tp.Symbol(type=Type.STRUCT, value=struct)
        return symb
    
    def visit_lit_str(self, node, children):
        symb = tp.Symbol(type=Type.I_STR, value=node.value[1:-1])
        return symb

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

######################
#                    #
#   LEXER / PARSER   #
#                    #
######################
# contains an instance of ParserPEG from the Arpeggio library and a PTNodeVisitor
# from the Arpeggio library
# produces a list of symbols as an output

class ParserDSPL:
    # TODO: change root to program and make the program a list of function definitions
    def __init__(self, grammar, root="block", dbg=False):
        self.parser = ParserPEG(grammar, root, comment_rule_name=None, 
            debug=dbg, reduce_tree=True)
        self.parser.autokwd = True
    
    def parse(self, input: str, dbg=False):
        # === LEXING / PARSING =================================================
        try:
            parse_tree = self.parser.parse(input)
        except NoMatch as e:
            print("syntax error at: (Ln {}, Col {})".format(e.line, e.col))
            quit()
        
        return parse_tree
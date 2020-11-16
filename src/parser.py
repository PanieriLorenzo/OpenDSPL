from arpeggio.cleanpeg import ParserPEG

"""input = 
1 -> some_process();
"""

with open('grammar_files/grammar_reduced.peg', 'r') as file:
    grammar = file.read() #.replace('\n', '')

with open('grammar_files/grammar_comment.peg', 'r') as file:
    comment = file.read()

with open('test_0.dsp', 'r') as file:
    input = file.read()

parser = ParserPEG(grammar, "program", comment, debug=False, autokwd=True, reduce_tree=True)
parse_tree = parser.parse(input)
print(parse_tree.tree_str())

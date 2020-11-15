from arpeggio.cleanpeg import ParserPEG

input = """
input: source = ("hello.txt", 32);
output: sink = ("goodbye.txt");
output.write = input.read;
"""

with open('grammar_files/grammar_reduced.peg', 'r') as file:
    grammar = file.read() #.replace('\n', '')

parser = ParserPEG(grammar, "program", debug=False, autokwd=True, reduce_tree=True)
parse_tree = parser.parse(input)
print(parse_tree.tree_str())

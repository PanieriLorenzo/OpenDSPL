import dspl_parser as pr
import dspl_interpret as nt

def main():
    with open('grammar_files/_grammar.peg', 'r') as file:
        grammar = file.read()

    with open('test_1.odspl', 'r') as file:
        input = file.read()
    

    # === PARSER / SEMANTIC ANALYSIS ===========================================
    # takes raw code string, converts it into a list of interdependant symbols
    parser = pr.ParserDSPL(grammar, root="program", dbg=False)
    program = parser.parse(input)


    # === INTERPRETER ==========================================================
    # takes a list of interdependant symbols and returns runnable code abstraction
    abstraction = nt.interpret(program)


    # === OBJECT FILE SERIALIZER ===============================================
    # the output from the interpreter module can be saved as a proprietary 
    # runnable object file. This allows to only interpret a script once, and run
    # the object file in all future executions

    
    # === OBJECT FILE DE-SERIALIZER ============================================
    # reads a runnable object file, turning it back into a runnable code
    # abstraction


    # === RUNNER ===============================================================
    # takes a runnable code abstraction and executes it.
    #runner = rn.RunnerDSPL()
    #runner.run(abstraction)


    # === PYTHON CODE GENERATOR ================================================
    # takes a runnable code abstraction and converts it into Python code


    # === C++ / JUCE CODE GENERATOR ============================================
    # takes a runnable code abstraction and converts it into C++ code with the
    # JUCE framework

if __name__ == "__main__":
    main()
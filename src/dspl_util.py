import dspl_types as tp

# generate a variable name from an expression
def expr_name(lhs: str, rhs: str, op: str):
    return "_" + lhs + "_" + op + rhs

# convert int to base32
def to_base32(x: int):
    # validation: x must be a natural number (including 0)
    if x < 0:
        print(f"{tp.CliC.FAIL}{tp.CliC.BOLD}Compiler Panic: assertion failed{tp.CliC.ENDC}")
        print(f"{tp.CliC.FAIL}Please report this error to the developers:")
        print(f"{tp.CliC.OKCYAN}Negative int in base32 conversion{tp.CliC.ENDC}")
        quit()
    
    dict = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
            'y', 'z', '2', '3', '4', '5', '6', '7']
    digits = []
    res = ""
    
    digits.append(dict[x%32])
    x //= 32
    while x != 0:
        digits.append(dict[x%32])
        x //= 32
    
    for i in range(len(digits)):
        res += digits[-i - 1]
    
    return res
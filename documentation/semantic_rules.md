````py
######################
#                    #
#   Semantic rules   #
#                    #
######################
# semantic rules are implemented during a second pass on the AST produced by the
# parser. This step modifies the AST, without producing any additional external
# data

# === Undefined symbols ========================================================
# before expressions can be evaluated, they have to be checked for undefined
# symbols

# vvv

# === Expression reduction =====================================================
# simple math expressions can be reduced to a single value

# int evaluation
def visit_lit_int(self, node, children):
    return int(node.value)

# float evaluation
def visit_lit_float(self, node, children):
    return float(node.value)

# bool evaluation
def visit_lit_bool(self, node, children):
    if node.value == "true":
        return True
    else:
        return False

# byte evaluation
def visit_lit_byte(self, node, children):
    # TODO:
    pass

# string evaluation
def visit_lit_str(self, node, children):
    return list(node.value)

# vvv

# === Max delay depth ==========================================================
# used to find the maximum delay distance for a variable, or if the delay is
# undefined at compile-time. This is used by the code runner to allocate the
# correct amount of memory.



````
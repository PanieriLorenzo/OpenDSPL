"""OpenDSPL interpreter. Semantic analysis -> Runnable abstraction."""
__author__ = "Lorenzo Panieri"
__license__ = "MIT"
__version__ = "0.1.0-indev+1"
__status__ = "Development"

import dspl_types as tp
from typing import List

def interpret(program: tp.Block):
    program = _blkToMap(program)
    program = _flattenBlock(program)
    program = _compressBlock(program)
    _validateBlock(program)
    sources = _extractSrc(program)
    sinks = _extractSnk(program)
    mainClock = _extractClock(sources)
    return (program, sources, sinks, mainClock)

# === BLOCK TO DICT ============================================================
def _blkToMap(blk: tp.Block):
    dict = {}
    for symb in blk.statements:
        if symb.name not in dict:
            dict[symb.name] = symb
        else:
            # check that RHS is anonymous
            print(symb.value.anonym)
            pass
    print(dict)

# === MERGE ALL LAMBDAS WITH CALLER ============================================
def _flattenBlock(blk):
    return blk

# === COMPACT RECORD ACCESSES ==================================================
def _compressBlock(blk):
    pass

# === VALIDATE PROGRAM =========================================================
def _validateBlock(blk):
    pass

# === EXTRACT SOURCES ==========================================================
def _extractSrc(blk):
    pass

# === EXTRACT SINKS ============================================================
def _extractSnk(blk):
    pass

# === EXTRACT CLOCK ============================================================
def _extractClock(src: List[tp.Symbol]):
    pass
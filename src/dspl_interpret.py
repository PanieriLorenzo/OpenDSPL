"""OpenDSPL interpreter. Semantic analysis -> Runnable abstraction."""
__author__ = "Lorenzo Panieri"
__license__ = "MIT"
__version__ = "0.1.0-indev+1"
__status__ = "Development"

import dspl_types as tp

def interpret(program: tp.Block):
    pass

# === MERGE ALL LAMBDAS WITH CALLER ============================================
def _flattenBlock(blk: tp.Block):
    pass

# === COMPACT RECORD ACCESSES ==================================================
def _compressBlock(blk: tp.Block):
    pass

# === EXTRACT SOURCES ==========================================================
def _extractSrc(blk: tp.Block):
    pass

# === EXTRACT SINKS ============================================================
def _extractSnk(blk: tp.Block):
    pass
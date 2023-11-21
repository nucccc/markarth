'''
testing mod colection functions
'''

import pytest

from markarth.convert.collect.mod_collect import (
    collect_func_defs
)

def test_collect_func_defs(mod3):
    mod_ast, _ = mod3

    func_asts = collect_func_defs(mod_ast = mod_ast)

    assert len(func_asts) == 3
    assert 'f1' in func_asts.keys()
    assert 'f2' in func_asts.keys()
    assert 'f3' in func_asts.keys()
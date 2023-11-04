import pytest

import ast

from markarth.convert.collect import mod_collector

def test_collector1(code1 : tuple[ast.AST, list[str]]):
    mod_ast, codelines = code1
    
    mc = mod_collector.ModCollector(mod_ast=mod_ast, codelines=codelines)

    func_defs, assignments = mc._collect_funcdefs_and_assignments()

    assert len(func_defs) == 3
    assert 'func0' in func_defs.keys()
    assert 'func1' in func_defs.keys()
    assert 'func2' in func_defs.keys()
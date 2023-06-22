import pytest

from markarth.core.utils import toCodelines, process_code, indentation_pattern
from markarth.core.funconv import typeFromCall

import ast

def test_to_tocodelines():
    '''
    this shall test the ToCodelines function
    '''
    code = '''def func() -> int:
    return 7'''
    codelines = toCodelines(code=code)
    assert len(codelines) == 2
    assert codelines[0] == 'def func() -> int:'
    assert codelines[1] == '    return 7'

def ast_call_from_code(code : str) -> ast.Call:
    module = ast.parse(code)
    call = module.body[0].value
    return call

def test_typFromCall():
    code = 'int(75*47)'
    call = ast_call_from_code(code)
    assert typeFromCall(call) == 'int'

    code = 'float(75*47)'
    call = ast_call_from_code(code)
    assert typeFromCall(call) == 'float'

def test_indentation_pattern():
    code = '''def func() -> int:
    return 7'''
    ast_nodes, codelines = process_code(code)
    func_ast = ast_nodes.body[0]
    assert indentation_pattern(func_ast, codelines) == '    '
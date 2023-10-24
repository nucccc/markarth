import pytest

from markarth.core.utils import to_codelines, process_code, indentation_pattern, ASTWithoutBody
from markarth.core.typecollector import type_from_call

import ast

def test_to_to_codelines():
    '''
    this shall test the to_codelines function
    '''
    code = '''def func() -> int:
    return 7'''
    codelines = to_codelines(code=code)
    assert len(codelines) == 2
    assert codelines[0] == 'def func() -> int:'
    assert codelines[1] == '    return 7'

def ast_call_from_code(code : str) -> ast.Call:
    module = ast.parse(code)
    call = module.body[0].value
    return call

def test_type_from_call():
    code = 'int(75*47)'
    call = ast_call_from_code(code)
    assert type_from_call(call) == 'int'

    code = 'float(75*47)'
    call = ast_call_from_code(code)
    assert type_from_call(call) == 'float'

def test_indentation_pattern():
    code = '''def func() -> int:
    return 7'''
    ast_nodes, codelines = process_code(code)
    func_ast = ast_nodes.body[0]
    assert indentation_pattern(func_ast, codelines) == '    '

def test_indentation_pattern_ast_without_body():
    code = '''a = 0'''

    ast_nodes, codelines = process_code(code)
    func_ast = ast_nodes.body[0]

    with pytest.raises(ASTWithoutBody) as ast_without_body:
        indentation_pattern(func_ast, codelines)
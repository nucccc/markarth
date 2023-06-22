from markarth.core.utils import process_code
from markarth.core.funconv import FuncConverter
from markarth.core.funconv import cdef_lines_from_iter

import pytest

def test_cdef_lines_from_iter():
    iter = [
        ('a', 'int'),
        ('b', 'float'),
        ('d', 'int')
    ]
    cdef_lines = cdef_lines_from_iter(iter=iter)
    assert 'cdef int a' in cdef_lines
    assert 'cdef float b' in cdef_lines
    assert 'cdef int d' in cdef_lines 

def test_1():
    code = '''
def stuff(a : int, b : int, c : float = 0.4, d = None) -> int:
    sum = 0
    for i in range(4):
        sum += i
        sum = 5 * 18
    return float(sum)
    '''
    ast_code, codelines = process_code(code)
    func_ast = ast_code.body[0]
    fc = FuncConverter(func_ast, codelines)
    
    input_var_dict = fc._collect_arg_types()
    assert input_var_dict['a'] == 'int'
    assert input_var_dict['b'] == 'int'
    assert input_var_dict['c'] == 'float'
    assert len(input_var_dict) == 3

    def_line = fc._get_func_decl()
    assert def_line == 'def stuff(a : int, b : int, c : float = 0.4, d = None) -> int:'

    r_type = fc._collect_return_type()
    assert r_type == 'int'

def test_2():
    code = '''
def stuff(
    a : int,
    b : int,
    c : float = 0.4,
    d = None
) -> int:
    sum = 0
    for i in range(4):
        sum += i
        sum = 5 * 18
    return float(sum)
    '''
    ast_code, codelines = process_code(code)
    func_ast = ast_code.body[0]
    fc = FuncConverter(func_ast, codelines)
    
    input_var_dict = fc._collect_arg_types()
    assert input_var_dict['a'] == 'int'
    assert input_var_dict['b'] == 'int'
    assert input_var_dict['c'] == 'float'
    assert len(input_var_dict) == 3

    expected_def_line = '''def stuff(
    a : int,
    b : int,
    c : float = 0.4,
    d = None
) -> int:'''
    def_line = fc._get_func_decl()
    assert def_line == expected_def_line
    
    r_type = fc._collect_return_type()
    assert r_type == 'int'

def test_convert():
    code = '''
def stuff(a : int, b : int, c : float = 0.4, d = None) -> int:
    sum = 0
    for i in range(4):
        p = 7
        h = float(64) * p
        sum += i
        sum = 5 * 18
    return float(sum)
'''
    ast_nodes, codelines = process_code(code)
    func_ast = ast_nodes.body[0]
    fc = FuncConverter(func_ast, codelines)
    fc.convert()
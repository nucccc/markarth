import pytest

import ast

from markarth.convert.preprocess import code_process

source_code1 = '''import json

A = 74
B : int = 78

C = "beh"

D = 0.12

def func0(a, b):
    return a + b

def func1(a : int, b : int) -> int:
    return a * b

def func2() -> bool:
    pass'''

@pytest.fixture
def code1() -> tuple[ast.Module, list[str]]:
    #source_code1
    return code_process.process_code(source_code1)

source_statements1 = '''a = 7
b = 5
c = 3
b = 7.12
d, c = 7.1, 2
e = 40
'''

source_code2 = '''import json
import cython

a = 0
b = 7
c = 17
'''

@pytest.fixture
def statements1() -> list[ast.AnnAssign|ast.Assign]:
    parse_result = ast.parse(source_statements1)
    return parse_result.body

source_func1 = '''def f():
    return 7 * 7
'''

@pytest.fixture
def func1() -> tuple[ast.FunctionDef, list[str]]:
    return code_process.process_func_code(source_func1)

source_func2 = '''def f(a : int, b : int) -> int:
    res = a + 2
    b = b * a
    res -= b
    c = res + 7
    return res
'''

@pytest.fixture
def func2() -> tuple[ast.FunctionDef, list[str]]:
    return code_process.process_func_code(source_func2)

source_statements2 ='''a = 3
b = 7
c = a + b
d = a + c'''

@pytest.fixture
def statements2() -> list[ast.AST]:
    parse_result = ast.parse(source_statements2)
    return parse_result.body
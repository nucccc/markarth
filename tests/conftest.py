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
def code1() -> tuple[ast.AST, list[str]]:
    #source_code1
    return code_process.process_code(source_code1)

source_assignments1 = '''a = 7
b = 5
c = 3
b = 7.12
d, c = 7.1, 2
e = 40
'''

@pytest.fixture
def assignments1() -> list[ast.AnnAssign|ast.Assign]:
    parse_result = ast.parse(source_assignments1)
    return parse_result.body
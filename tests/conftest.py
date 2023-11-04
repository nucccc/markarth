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
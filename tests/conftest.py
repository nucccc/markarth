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
    return code_process.process_code(source_code1)

source_mod2 = '''import json
import cython

a = 0
b = 7
c = 17
'''

@pytest.fixture
def mod2() -> tuple[ast.Module, list[str]]:
    return code_process.process_code(source_mod2)

source_mod3 = '''a = 7
b = 3.4

def f1(g : int) -> float:
    res = b * g
    b = res
    return res

def f2() -> int:
    res = 7 * a
    return res

def f3(g : int) -> int:
    c = f2()
    res = c * g
    return res
'''

@pytest.fixture
def code_mod3() -> str:
    return source_mod3

@pytest.fixture
def mod3() -> tuple[ast.Module, list[str]]:
    return code_process.process_code(source_mod3)

source_mod4 = '''
def stuff(a : int, b : int, c : float = 0.4, d = None) -> int:
    sum = 0
    m = 11
    onono = 17.4
    for i in range(4):
        p = 7
        h = float(64) * p
        sum += i
        sum = 5 * 18
    return float(sum)
'''

@pytest.fixture
def code_mod4() -> str:
    return source_mod4

@pytest.fixture
def mod4() -> tuple[ast.Module, list[str]]:
    return code_process.process_code(source_mod4)

# mod5 mostly addresses expressions representing assignments
source_mod5 = '''
a = 7
b = c = d = 5
e, f, g = fake_tuple()
b += 3
b -= 1
c *= 3
c /= 5
'''

@pytest.fixture
def code_mod5() -> str:
    return source_mod5

@pytest.fixture
def mod5() -> tuple[ast.Module, list[str]]:
    return code_process.process_code(source_mod5)


# mod6 regards a module with expressions not exactly being considerable
# as assignments
source_mod6 = '''
import ast

def func() -> bool:
    return True

def other_func(a : int = 4) -> int:
    a *= 5
    return a

class a_class():

    def __init__(self):
        self.a = 6
'''

@pytest.fixture
def code_mod6() -> str:
    return source_mod5

@pytest.fixture
def mod6() -> tuple[ast.Module, list[str]]:
    return code_process.process_code(source_mod6)

source_statements1 = '''a = 7
b = 5
c = 3
b = 7.12
d, c = 7.1, 2
e = 40
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
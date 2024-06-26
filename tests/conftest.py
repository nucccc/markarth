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
def code1() -> tuple[ast.Module, list[str]]: # pragma: no cover
    return code_process.process_code(source_code1)

source_mod2 = '''import json
import cython

a = 0
b = 7
c = 17
'''

@pytest.fixture
def mod2() -> tuple[ast.Module, list[str]]: # pragma: no cover
    return code_process.process_code(source_mod2)

source_mod3 = '''a = 7
b = 3.4

def f1(g : int) -> float:
    global b
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
def code_mod3() -> str: # pragma: no cover
    return source_mod3

@pytest.fixture
def mod3() -> tuple[ast.Module, list[str]]: # pragma: no cover
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
def code_mod4() -> str: # pragma: no cover
    return source_mod4

@pytest.fixture
def mod4() -> tuple[ast.Module, list[str]]: # pragma: no cover
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
h : float = 3.5
'''

@pytest.fixture
def code_mod5() -> str: # pragma: no cover
    return source_mod5

@pytest.fixture
def mod5() -> tuple[ast.Module, list[str]]: # pragma: no cover
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
def code_mod6() -> str: # pragma: no cover
    return source_mod6

@pytest.fixture
def mod6() -> tuple[ast.Module, list[str]]: # pragma: no cover
    return code_process.process_code(source_mod6)


source_mod7 = '''
g_a = 7

def f1() -> float:
    a : float = 4
    b = c = d = 1
    b *= 4.7
    return a
'''

@pytest.fixture
def code_mod7() -> str: # pragma: no cover
    return source_mod7

@pytest.fixture
def mod7() -> tuple[ast.Module, list[str]]: # pragma: no cover
    return code_process.process_code(source_mod7)


source_mod8 = '''
o1 = 1
o2 = 2
o3 = 3
o4 = 4

def f1() -> float:
    global o1, o2
    a : float = 4
    if a >= 2:
        global o3
        o3 += a
    b = c = d = 1
    b *=o4
    return a
'''

@pytest.fixture
def code_mod8() -> str: # pragma: no cover
    return source_mod8

@pytest.fixture
def mod8() -> tuple[ast.Module, list[str]]: # pragma: no cover
    return code_process.process_code(source_mod8)


source_mod9 = '''
def f1() -> float:
    a : float = 0.34
    for i, nf in enumerate([0.16, 1.12, 1.17, 118.0]):
        a = float(i) + a * float(nf)
    return a
'''

@pytest.fixture
def code_mod9() -> str: # pragma: no cover
    return source_mod9

@pytest.fixture
def mod9() -> tuple[ast.Module, list[str]]: # pragma: no cover
    return code_process.process_code(source_mod9)


# this is the same as mod3 but with some docstring
source_mod10 = '''a = 7
b = 3.4

def f1(g : int) -> float:
    """
    this is a docstring
    """
    global b
    res = b * g
    b = res
    return res

def f2() -> int:
    r"""this is another docstring"""
    res = 7 * a
    return res

def f3(g : int) -> int:
    c = f2()
    res = c * g
    return res
'''

@pytest.fixture
def code_mod10() -> str: # pragma: no cover
    return source_mod10

@pytest.fixture
def mod10() -> tuple[ast.Module, list[str]]: # pragma: no cover
    return code_process.process_code(source_mod10)


# this test is for enumerates and containers
source_mod11 = '''
def f1(g : int) -> float:
    l : list[int] = list(range(4,7))
    a = 0
    for i, elem in enumerate(l):
        print(elem)
        (l[i], a) = 3, i
    return sum(l) * 3.4
'''

@pytest.fixture
def code_mod11() -> str: # pragma: no cover
    return source_mod11

@pytest.fixture
def mod11() -> tuple[ast.Module, list[str]]: # pragma: no cover
    return code_process.process_code(source_mod11)


source_statements1 = '''a = 7
b = 5
c = 3
b = 7.12
d, c = 7.1, 2
e = 40
'''

@pytest.fixture
def statements1() -> list[ast.AnnAssign|ast.Assign]: # pragma: no cover
    parse_result = ast.parse(source_statements1)
    return parse_result.body

source_func1 = '''def f():
    return 7 * 7
'''

@pytest.fixture
def func1() -> tuple[ast.FunctionDef, list[str]]: # pragma: no cover
    return code_process.process_func_code(source_func1)

source_func2 = '''def f(a : int, b : int) -> int:
    res = a + 2
    b = b * a
    res -= b
    c = res + 7
    return res
'''

@pytest.fixture
def func2() -> tuple[ast.FunctionDef, list[str]]: # pragma: no cover
    return code_process.process_func_code(source_func2)

# this shall have an enumerate
source_func3 = '''def f1(hl : list) -> float:
    for i, stuff in enumerate(hl):
        pass
    return 0.07
'''

@pytest.fixture
def func3() -> tuple[ast.FunctionDef, list[str]]: # pragma: no cover
    return code_process.process_func_code(source_func3)


source_statements2 ='''a = 3
b = 7
c = a + b
d = a + c'''

@pytest.fixture
def statements2() -> list[ast.AST]: # pragma: no cover
    parse_result = ast.parse(source_statements2)
    return parse_result.body
import sys
sys.path.append('../')

from markarth.markarth import convert_func, InvalidCode

import pytest

def test_func_conv():
    code = '''
def stuff(a : int, b : int, c : float = 0.4, d = None) -> int:
    sum = 0
    for i in range(4):
        sum += i
        sum = 5 * 18
    return sum
    '''

    result = convert_func(code)

def test_invalid_code_exception():
    code = '''
a = 0

def stuff(a : int, b : int, c : float = 0.4, d = None) -> int:
    sum = 0
    for i in range(4):
        sum += i
        sum = 5 * 18
    return sum
    '''

    with pytest.raises(InvalidCode) as ex_invalid_code:
        convert_func(code)

    code = '''
a = 0
    '''

    with pytest.raises(InvalidCode) as ex_invalid_code:
        convert_func(code)
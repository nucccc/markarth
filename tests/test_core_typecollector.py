import ast
from markarth.core.typecollector import get_type_from_iter

def test_get_type_from_iter():
    code = '''for i in range(7):\n\tpass'''
    m = ast.parse(code)
    f = m.body[0]
    assert get_type_from_iter(f.iter) == 'int'
    code = '''for i in range(len([2.3,4.5])):\n\tpass'''
    m = ast.parse(code)
    f = m.body[0]
    assert get_type_from_iter(f.iter) == 'int'
    code = '''for i in boh:\n\tpass'''
    m = ast.parse(code)
    f = m.body[0]
    assert get_type_from_iter(f.iter) is None
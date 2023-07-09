import ast
from markarth.core.typecollector import type_from_constant, type_from_iter, type_from_bin_op

def test_type_from_constant():
    const_code = '7'
    const_mod = ast.parse(const_code)
    const = const_mod.body[0].value

    assert type_from_constant(const) == 'int'

    const_code = 'True'
    const_mod = ast.parse(const_code)
    const = const_mod.body[0].value

    assert type_from_constant(const) == 'bool'

    const_code = '7.0'
    const_mod = ast.parse(const_code)
    const = const_mod.body[0].value

    assert type_from_constant(const) == 'float'

def test_type_from_iter():
    code = '''for i in range(7):\n\tpass'''
    m = ast.parse(code)
    f = m.body[0]
    assert type_from_iter(f.iter) == 'int'
    code = '''for i in range(len([2.3,4.5])):\n\tpass'''
    m = ast.parse(code)
    f = m.body[0]
    assert type_from_iter(f.iter) == 'int'
    code = '''for i in boh:\n\tpass'''
    m = ast.parse(code)
    f = m.body[0]
    assert type_from_iter(f.iter) is None

def test_type_from_bin_op():
    op_code = '6 + 7'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    typ = type_from_bin_op(bin_op)
    assert typ == 'int'

    op_code = '6 + 7.1'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    typ = type_from_bin_op(bin_op)
    assert typ == 'float'

    op_code = '6.8 + 7.1'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    typ = type_from_bin_op(bin_op)
    assert typ == 'float'

    op_code = '8 / 4'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    typ = type_from_bin_op(bin_op)
    assert typ == 'float'

    op_code = '8 / 3'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    typ = type_from_bin_op(bin_op)
    assert typ == 'float'
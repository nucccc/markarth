import ast
from markarth.convert.collect.ast_to_typ.ast_to_typ import (
    typ_from_bin_op,
    typ_from_constant,
    typ_from_iter,
    ast_val_to_typ
)


def test_ast_val_to_typ():
    code = 'a = b'
    mod = ast.parse(code)
    val = mod.body[0].value

    val_typ = ast_val_to_typ(val = val)
    assert val_typ.is_any()


def test_type_from_constant():
    const_code = '7'
    const_mod = ast.parse(const_code)
    const = const_mod.body[0].value

    t = typ_from_constant(const)
    assert t.is_int()

    const_code = 'True'
    const_mod = ast.parse(const_code)
    const = const_mod.body[0].value

    t = typ_from_constant(const)
    assert t.is_bool()

    const_code = '7.0'
    const_mod = ast.parse(const_code)
    const = const_mod.body[0].value

    t = typ_from_constant(const)
    assert t.is_float()

def test_type_from_iter():
    code = '''for i in range(7):\n\tpass'''
    m = ast.parse(code)
    f = m.body[0]
    assert typ_from_iter(f.iter).is_int()
    code = '''for i in range(len([2.3,4.5])):\n\tpass'''
    m = ast.parse(code)
    f = m.body[0]
    assert typ_from_iter(f.iter).is_int()
    code = '''for i in boh:\n\tpass'''
    m = ast.parse(code)
    f = m.body[0]
    assert typ_from_iter(f.iter).is_any()

def test_type_from_bin_op():
    op_code = '6 + 7'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    t = typ_from_bin_op(bin_op)
    assert t.is_int()

    op_code = '6 + 7.1'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    t = typ_from_bin_op(bin_op)
    assert t.is_float()

    op_code = '6.8 + 7.1'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    t = typ_from_bin_op(bin_op)
    assert t.is_float()

    op_code = '8 / 4'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    t = typ_from_bin_op(bin_op)
    assert t.is_float()

    op_code = '8 / 3'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    t = typ_from_bin_op(bin_op)
    assert t.is_float()
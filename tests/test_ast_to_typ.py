import ast


from markarth.convert.collect.ast_to_typ.ast_to_typ import (
    typ_from_bin_op,
    typ_from_constant,
    typ_from_iter,
    typ_from_call,
    ast_val_to_typ,
    eval_op_typ
)
from markarth.convert.typs import typs


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

    const_code = 'b\'abc\''
    const_mod = ast.parse(const_code)
    const = const_mod.body[0].value

    t = typ_from_constant(const)
    assert t.is_any()
    

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

    op_code = 'a - 1'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    t = typ_from_bin_op(bin_op)
    assert t.is_any()

    op_code = '1 - a'
    op_mod = ast.parse(op_code)
    bin_op = op_mod.body[0].value
    t = typ_from_bin_op(bin_op)
    assert t.is_any()


def test_eval_op_typ():
    
    assert eval_op_typ(
        op = ast.Add(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.INT ),
        right_typ = typs.TypAny()
    ).is_any()

    assert eval_op_typ(
        op = ast.Add(),
        left_typ = typs.TypAny(),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.INT )
    ).is_any()

    assert eval_op_typ(
        op = ast.Add(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.INT ),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.INT )
    ).is_int()

    assert eval_op_typ(
        op = ast.Sub(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.INT ),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.INT )
    ).is_int()

    assert eval_op_typ(
        op = ast.Mult(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.INT ),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.INT )
    ).is_int()

    assert eval_op_typ(
        op = ast.Mod(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.INT ),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.INT )
    ).is_int()

    assert eval_op_typ(
        op = ast.Div(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.INT ),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.INT )
    ).is_float()

    assert eval_op_typ(
        op = ast.Add(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.FLOAT ),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.INT )
    ).is_float()

    assert eval_op_typ(
        op = ast.Add(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.INT ),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.FLOAT )
    ).is_float()

    #tests with strings

    assert eval_op_typ(
        op = ast.Add(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.STR ),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.STR )
    ).is_str()

    assert eval_op_typ(
        op = ast.Add(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.INT ),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.STR )
    ).is_any()

    assert eval_op_typ(
        op = ast.Add(),
        left_typ = typs.TypPrimitive( typs.PrimitiveCod.STR ),
        right_typ = typs.TypPrimitive( typs.PrimitiveCod.INT )
    ).is_any()


def test_typ_from_call():
    code = 'a = int(7.0)'
    mod = ast.parse(code)
    call = mod.body[0].value

    print(type(call))

    call_typ = typ_from_call(call = call)
    assert call_typ.is_int()

    code = 'a = float(7)'
    mod = ast.parse(code)
    call = mod.body[0].value

    call_typ = typ_from_call(call = call)
    assert call_typ.is_float()

    code = 'a = bool(7)'
    mod = ast.parse(code)
    call = mod.body[0].value

    call_typ = typ_from_call(call = call)
    assert call_typ.is_bool()

    code = 'a = str(7)'
    mod = ast.parse(code)
    call = mod.body[0].value

    call_typ = typ_from_call(call = call)
    assert call_typ.is_str()

    code = 'a = len([1,2,3])'
    mod = ast.parse(code)
    call = mod.body[0].value

    call_typ = typ_from_call(call = call)
    assert call_typ.is_int()

    code = 'a = np.mean()'
    mod = ast.parse(code)
    call = mod.body[0].value

    call_typ = typ_from_call(call = call)
    assert call_typ.is_any()

    code = 'a = asfasf(7)'
    mod = ast.parse(code)
    call = mod.body[0].value

    call_typ = typ_from_call(call = call)
    assert call_typ.is_any()
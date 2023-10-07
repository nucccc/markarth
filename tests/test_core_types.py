import pytest

from markarth.core.types import types

def test_str_to_prim_cod():
    assert types.str_to_prim_cod('bool') == types.PrimitiveCod.BOOL
    assert types.str_to_prim_cod('float') == types.PrimitiveCod.FLOAT
    assert types.str_to_prim_cod('int') == types.PrimitiveCod.INT
    assert types.str_to_prim_cod('str') == types.PrimitiveCod.STR

    assert types.str_to_prim_cod_or_none('bool') == types.PrimitiveCod.BOOL
    assert types.str_to_prim_cod_or_none('float') == types.PrimitiveCod.FLOAT
    assert types.str_to_prim_cod_or_none('int') == types.PrimitiveCod.INT
    assert types.str_to_prim_cod_or_none('str') == types.PrimitiveCod.STR

    assert types.str_to_prim_cod_or_none('hakahakahaka') is None


def test_prim_cod_to_str():
    assert types.prim_cod_to_str(types.PrimitiveCod.BOOL) == 'bool'
    assert types.prim_cod_to_str(types.PrimitiveCod.FLOAT) == 'float'
    assert types.prim_cod_to_str(types.PrimitiveCod.INT) == 'int'
    assert types.prim_cod_to_str(types.PrimitiveCod.STR) == 'str'


def test_typ_primitive():
    # bool test
    typ = types.TypPrimitive('bool')

    assert typ.is_primitive()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_unkown()

    assert typ.is_bool()
    assert not typ.is_float()
    assert not typ.is_int()
    assert not typ.is_str()

    assert typ.as_string() == 'bool'
    assert typ.get_primitive_cod() == types.PrimitiveCod.BOOL

    # int test
    typ = types.TypPrimitive('int')

    assert typ.is_primitive()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_unkown()

    assert not typ.is_bool()
    assert not typ.is_float()
    assert typ.is_int()
    assert not typ.is_str()

    assert typ.as_string() == 'int'
    assert typ.get_primitive_cod() == types.PrimitiveCod.INT

    # float test
    typ = types.TypPrimitive('float')

    assert typ.is_primitive()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_unkown()

    assert not typ.is_bool()
    assert typ.is_float()
    assert not typ.is_int()
    assert not typ.is_str()

    assert typ.as_string() == 'float'
    assert typ.get_primitive_cod() == types.PrimitiveCod.FLOAT

    # str test
    typ = types.TypPrimitive('str')

    assert typ.is_primitive()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_unkown()

    assert not typ.is_bool()
    assert not typ.is_float()
    assert not typ.is_int()
    assert typ.is_str()

    assert typ.as_string() == 'str'
    assert typ.get_primitive_cod() == types.PrimitiveCod.STR


def test_typ_unknown():
    typ = types.TypUnknown()

    assert typ.is_unkown()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_primitive()

    assert typ.as_string() == 'any'
    

def test_typ_none():
    typ = types.TypNone()

    assert typ.is_none()
    assert not typ.is_container()
    assert not typ.is_primitive()
    assert not typ.is_unkown()

    assert typ.as_string() == 'None'
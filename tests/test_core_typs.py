import pytest

from markarth.convert.typs import typs

def test_str_to_prim_cod():
    assert typs.str_to_prim_cod('bool') == typs.PrimitiveCod.BOOL
    assert typs.str_to_prim_cod('float') == typs.PrimitiveCod.FLOAT
    assert typs.str_to_prim_cod('int') == typs.PrimitiveCod.INT
    assert typs.str_to_prim_cod('str') == typs.PrimitiveCod.STR

    assert typs.str_to_prim_cod_or_none('bool') == typs.PrimitiveCod.BOOL
    assert typs.str_to_prim_cod_or_none('float') == typs.PrimitiveCod.FLOAT
    assert typs.str_to_prim_cod_or_none('int') == typs.PrimitiveCod.INT
    assert typs.str_to_prim_cod_or_none('str') == typs.PrimitiveCod.STR

    assert typs.str_to_prim_cod_or_none('hakahakahaka') is None


def test_prim_cod_to_str():
    assert typs.prim_cod_to_str(typs.PrimitiveCod.BOOL) == 'bool'
    assert typs.prim_cod_to_str(typs.PrimitiveCod.FLOAT) == 'float'
    assert typs.prim_cod_to_str(typs.PrimitiveCod.INT) == 'int'
    assert typs.prim_cod_to_str(typs.PrimitiveCod.STR) == 'str'


def test_typ_primitive():
    # bool test
    typ = typs.TypPrimitive('bool')

    assert typ.is_primitive()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_unkown()

    assert typ.is_bool()
    assert not typ.is_float()
    assert not typ.is_int()
    assert not typ.is_str()

    assert typ.as_string() == 'bool'
    assert typ.get_primitive_cod() == typs.PrimitiveCod.BOOL

    # int test
    typ = typs.TypPrimitive('int')

    assert typ.is_primitive()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_unkown()

    assert not typ.is_bool()
    assert not typ.is_float()
    assert typ.is_int()
    assert not typ.is_str()

    assert typ.as_string() == 'int'
    assert typ.get_primitive_cod() == typs.PrimitiveCod.INT

    # float test
    typ = typs.TypPrimitive('float')

    assert typ.is_primitive()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_unkown()

    assert not typ.is_bool()
    assert typ.is_float()
    assert not typ.is_int()
    assert not typ.is_str()

    assert typ.as_string() == 'float'
    assert typ.get_primitive_cod() == typs.PrimitiveCod.FLOAT

    # str test
    typ = typs.TypPrimitive('str')

    assert typ.is_primitive()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_unkown()

    assert not typ.is_bool()
    assert not typ.is_float()
    assert not typ.is_int()
    assert typ.is_str()

    assert typ.as_string() == 'str'
    assert typ.get_primitive_cod() == typs.PrimitiveCod.STR


def test_typ_unknown():
    typ = typs.TypUnknown()

    assert typ.is_unkown()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_primitive()

    assert typ.as_string() == 'any'
    

def test_typ_none():
    typ = typs.TypNone()

    assert typ.is_none()
    assert not typ.is_container()
    assert not typ.is_primitive()
    assert not typ.is_unkown()

    assert typ.as_string() == 'None'
import pytest

from markarth.convert.typs import typs
from markarth.convert.typs.typs_parse import parse_type_str


def test_typs_parse():
    bool_typ = parse_type_str('bool')
    assert type(bool_typ) == typs.TypPrimitive
    assert bool_typ.get_primitive_cod() == typs.PrimitiveCod.BOOL

    float_typ = parse_type_str('float')
    assert type(float_typ) == typs.TypPrimitive
    assert float_typ.get_primitive_cod() == typs.PrimitiveCod.FLOAT

    int_typ = parse_type_str('int')
    assert type(int_typ) == typs.TypPrimitive
    assert int_typ.get_primitive_cod() == typs.PrimitiveCod.INT

    str_typ = parse_type_str('str')
    assert type(str_typ) == typs.TypPrimitive
    assert str_typ.get_primitive_cod() == typs.PrimitiveCod.STR

    typ = parse_type_str('hakahakahaka')
    assert type(typ) == typs.TypAny
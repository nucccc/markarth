import pytest

from markarth.core.types import types
from markarth.core.types.typs_parse import parse_type_str


def test_typs_parse():
    bool_typ = parse_type_str('bool')
    assert type(bool_typ) == types.TypPrimitive
    assert bool_typ.get_primitive_cod() == types.PrimitiveCod.BOOL

    float_typ = parse_type_str('float')
    assert type(float_typ) == types.TypPrimitive
    assert float_typ.get_primitive_cod() == types.PrimitiveCod.FLOAT

    int_typ = parse_type_str('int')
    assert type(int_typ) == types.TypPrimitive
    assert int_typ.get_primitive_cod() == types.PrimitiveCod.INT

    str_typ = parse_type_str('str')
    assert type(str_typ) == types.TypPrimitive
    assert str_typ.get_primitive_cod() == types.PrimitiveCod.STR

    typ = parse_type_str('hakahakahaka')
    assert type(typ) == types.TypUnknown
import pytest

from markarth.convert.typs import typs

# TODO: wouldn't it be good to test also quelity comparisons

def test_str_to_prim_cod():
    assert typs.str_to_prim_cod('bool') == typs.PrimitiveCod.BOOL
    assert typs.str_to_prim_cod('float') == typs.PrimitiveCod.FLOAT
    assert typs.str_to_prim_cod('int') == typs.PrimitiveCod.INT
    assert typs.str_to_prim_cod('str') == typs.PrimitiveCod.STR

    with pytest.raises(typs.InvalidPrimitiveStr):
        typs.str_to_prim_cod('hakahakahaka')

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


def test_typ():
    typ = typs.Typ()

    with pytest.raises(NotImplementedError):
        typ.as_string()


def test_typ_primitive():
    # bool test
    typ = typs.TypPrimitive('bool')

    assert typ.is_primitive()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_any()

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
    assert not typ.is_any()

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
    assert not typ.is_any()

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
    assert not typ.is_any()

    assert not typ.is_bool()
    assert not typ.is_float()
    assert not typ.is_int()
    assert typ.is_str()

    assert typ.as_string() == 'str'
    assert typ.get_primitive_cod() == typs.PrimitiveCod.STR


def test_typ_unknown():
    typ = typs.TypAny()

    assert typ.is_any()
    assert not typ.is_container()
    assert not typ.is_none()
    assert not typ.is_primitive()

    assert typ.as_string() == 'any'
    

def test_typ_none():
    typ = typs.TypNone()

    assert typ.is_none()
    assert not typ.is_container()
    assert not typ.is_primitive()
    assert not typ.is_any()

    assert typ.as_string() == 'None'


def test_typ_any():
    typ = typs.TypAny()

    assert not typ.is_none()
    assert not typ.is_container()
    assert not typ.is_primitive()
    assert typ.is_any()

    assert typ.as_string() == 'any'


def test_typ_union():
    typ = typs.TypUnion()

    assert typ.is_union()
    assert not typ.is_str()
    assert not typ.is_any()
    assert not typ.is_bool()
    assert not typ.is_container()
    assert not typ.is_float()
    assert not typ.is_int()
    assert not typ.is_none()
    assert not typ.is_primitive()

    t_int1 = typs.TypPrimitive(prim=typs.PrimitiveCod.INT)

    typ.add_typ(t_int1)
    assert len(typ.get_union_types) == 1

    t_int2 = typs.TypPrimitive(prim=typs.PrimitiveCod.INT)

    typ.add_typ(t_int2)
    assert len(typ.get_union_types) == 1

    t_float = typs.TypPrimitive(prim=typs.PrimitiveCod.FLOAT)
    typ.add_typ(t_float)
    assert len(typ.get_union_types) == 2

    # testing now a typ union with another union

    typ2 = typs.TypUnion()

    typ2.add_typ(typs.TypPrimitive(typs.PrimitiveCod.FLOAT))
    typ2.add_typ(typs.TypPrimitive(typs.PrimitiveCod.BOOL))

    typ.add_typ(typ2)

    assert len(typ.get_union_types) == 3
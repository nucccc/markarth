import pytest

from markarth.convert.typs import typs, merge_typs
from markarth.convert.typs.merge_typs import merge_typs


def test_marge_any():
    t_any1 = typs.TypAny()
    t_any2 = typs.TypAny()
    t_bool = typs.TypPrimitive(prim=typs.PrimitiveCod.BOOL)

    merged = merge_typs(t_any1, t_bool)
    assert merged.is_any()

    merged = merge_typs(t_bool, t_any1)
    assert merged.is_any()

    merged = merge_typs(t_any1, t_any2)
    assert merged.is_any()


def test_merge_equal():
    t_bool1 = typs.TypPrimitive(prim=typs.PrimitiveCod.BOOL)
    t_bool2 = typs.TypPrimitive(prim=typs.PrimitiveCod.BOOL)

    t_int1 = typs.TypPrimitive(prim=typs.PrimitiveCod.INT)
    t_int2 = typs.TypPrimitive(prim=typs.PrimitiveCod.INT)

    t_str1 = typs.TypPrimitive(prim=typs.PrimitiveCod.STR)
    t_str2 = typs.TypPrimitive(prim=typs.PrimitiveCod.STR)

    t_float1 = typs.TypPrimitive(prim=typs.PrimitiveCod.FLOAT)
    t_float2 = typs.TypPrimitive(prim=typs.PrimitiveCod.FLOAT)

    merged = merge_typs(t_bool1, t_bool2)
    assert merged.is_bool()

    merged = merge_typs(t_int1, t_int2)
    assert merged.is_int()

    merged = merge_typs(t_str1, t_str2)
    assert merged.is_str()

    merged = merge_typs(t_float1, t_float2)
    assert merged.is_float()

def test_merge_unions():
    t_bool = typs.TypPrimitive(prim=typs.PrimitiveCod.BOOL)

    t_int = typs.TypPrimitive(prim=typs.PrimitiveCod.INT)

    t_str = typs.TypPrimitive(prim=typs.PrimitiveCod.STR)

    t_float = typs.TypPrimitive(prim=typs.PrimitiveCod.FLOAT)

    merged = merge_typs(t_bool, t_int)
    assert merged.is_union()
    assert t_bool in merged.get_union_types
    assert t_int in merged.get_union_types

    merged = merge_typs(t_int, t_bool)
    assert merged.is_union()
    assert t_bool in merged.get_union_types
    assert t_int in merged.get_union_types

    merged = merge_typs(t_bool, t_str)
    assert merged.is_union()
    assert t_bool in merged.get_union_types
    assert t_str in merged.get_union_types
    
    merged = merge_typs(t_str, t_bool)
    assert merged.is_union()
    assert t_bool in merged.get_union_types
    assert t_str in merged.get_union_types

    merged = merge_typs(t_int, t_float)
    assert merged.is_union()
    assert t_float in merged.get_union_types
    assert t_int in merged.get_union_types
    
    merged = merge_typs(t_float, t_int)
    assert merged.is_union()
    assert t_float in merged.get_union_types
    assert t_int in merged.get_union_types

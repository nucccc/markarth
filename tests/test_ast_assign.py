import pytest

import ast

from markarth.convert.collect.ast_to_typ.ast_assign import (
    is_assign,
    assigned_typs,
    _add_target_to_typ_store
)
from markarth.convert.typs.names_to_typs import DictTypStore
from markarth.convert.typs import typs


def test_is_assignment(mod5, mod6):
    ast_mod, _ = mod5

    for expr in ast_mod.body:
        assert is_assign(expr)

    ast_mod, _ = mod6

    for expr in ast_mod.body:
        assert not is_assign(expr)


def test_assigned_typs():
    mod = ast.parse('a = b = c = 7')

    assignment = mod.body[0]

    result = assigned_typs(assignment)

    assert result.annotation is None

    typ_store = result.assigned_typs

    assert len(typ_store) == 3

    a_typ = typ_store.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_int()

    b_typ = typ_store.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_int()

    c_typ = typ_store.get_typ('c')
    assert c_typ is not None
    assert c_typ.is_int()


def test_add_target_to_typ_store():
    typ_store = DictTypStore()

    mod = ast.parse('a = b = c = 7')

    assignment = mod.body[0]

    for target in assignment.targets:
        _add_target_to_typ_store(
            target = target,
            target_store = typ_store,
            val_typ = typs.TypPrimitive(typs.PrimitiveCod.INT)
        )

    assert len(typ_store) == 3

    a_typ = typ_store.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_int()

    b_typ = typ_store.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_int()

    c_typ = typ_store.get_typ('c')
    assert c_typ is not None
    assert c_typ.is_int()
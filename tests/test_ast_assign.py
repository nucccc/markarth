import pytest

import ast

from markarth.convert.collect.ast_to_typ.ast_assign import (
    is_assign,
    assigned_typs,
    _add_target_to_typ_store,
    typ_store_from_target
)
from markarth.convert.collect.vartyp_tracker import VarTypTracker
from markarth.convert.typs.typ_store import DictTypStore
from markarth.convert.typs import typs


def test_is_assignment(mod5, mod6):
    ast_mod, _ = mod5

    for expr in ast_mod.body:
        assert is_assign(expr)

    ast_mod, _ = mod6

    for expr in ast_mod.body:
        assert not is_assign(expr)


def test_assigned_typs():

    # testing an assignment with multiple targets
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

    # testing an annotated assignment
    mod = ast.parse('a : int = 7')

    assignment = mod.body[0]

    result = assigned_typs(assignment)

    assert result.annotation is not None
    assert result.annotation.is_int()

    typ_store = result.assigned_typs

    assert len(typ_store) == 1

    a_typ = typ_store.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_int()

    # testing an augmentation assign without names to typs
    mod = ast.parse('a *= 7')

    assignment = mod.body[0]

    result = assigned_typs(assignment)

    assert result.annotation is None

    typ_store = result.assigned_typs

    assert len(typ_store) == 1

    a_typ = typ_store.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_any()

    # testing an augmentation assign with names to typs with the variable
    var_tracker = VarTypTracker()

    var_tracker.add_local_typ('a', typs.TypPrimitive(typs.PrimitiveCod.FLOAT))

    result = assigned_typs(assignment, var_tracker)

    assert result.annotation is None
    
    typ_store = result.assigned_typs

    assert len(typ_store) == 1

    a_typ = typ_store.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_float()

    # testing an augmentation assign with names to typs without the variable
    var_tracker = VarTypTracker()

    var_tracker.add_local_typ('b', typs.TypPrimitive(typs.PrimitiveCod.FLOAT))

    result = assigned_typs(assignment, var_tracker)

    assert result.annotation is None
    
    typ_store = result.assigned_typs

    assert len(typ_store) == 1

    a_typ = typ_store.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_any()


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


def test_add_target_to_typ_store_tuple():
    typ_store = DictTypStore()

    mod = ast.parse('a, b, c = 7')

    assignment = mod.body[0]

    _add_target_to_typ_store(
        target = assignment.targets[0],
        target_store = typ_store,
        val_typ = typs.TypPrimitive(typs.PrimitiveCod.INT)
    )

    assert len(typ_store) == 3

    a_typ = typ_store.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_any()

    b_typ = typ_store.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_any()

    c_typ = typ_store.get_typ('c')
    assert c_typ is not None
    assert c_typ.is_any()


def test_typ_store_from_target():
    
    mod = ast.parse('a, b, c = 7')

    assignment = mod.body[0]

    typ_store = typ_store_from_target(
        target = assignment.targets[0],
        val_typ = typs.TypPrimitive(typs.PrimitiveCod.INT)
    )

    assert len(typ_store) == 3

    a_typ = typ_store.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_any()

    b_typ = typ_store.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_any()

    c_typ = typ_store.get_typ('c')
    assert c_typ is not None
    assert c_typ.is_any()


    # additionally there should be some tests regarding subscripts
    mod = ast.parse('a[0], b, c = 7')

    assignment = mod.body[0]

    typ_store = typ_store_from_target(
        target = assignment.targets[0],
        val_typ = typs.TypPrimitive(typs.PrimitiveCod.INT)
    )

    assert len(typ_store) == 2

    b_typ = typ_store.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_any()

    c_typ = typ_store.get_typ('c')
    assert c_typ is not None
    assert c_typ.is_any()


    # additionally there should be some tests regarding subscripts
    mod = ast.parse('a[0] += 7')

    assignment = mod.body[0]

    typ_store = typ_store_from_target(
        target = assignment.target,
        val_typ = typs.TypPrimitive(typs.PrimitiveCod.INT)
    )

    assert len(typ_store) == 0
import pytest

import ast

from markarth.convert.collect.func_collect import (
    func_name_from_ast,
    input_typs_from_ast,
    return_typ_from_ast,
    collect_func_globals,
    collect_local_typs,
    collect_from_func_ast,
    _record_vartyp,
    CollisionEnum
)
from markarth.convert.collect.vartyp_tracker import VarTypTracker
from markarth.convert.typs.typ_store import DictTypStore
from markarth.convert.typs.typs import PrimitiveCod, TypPrimitive


def test_func_name_from_ast(func1, func2):
    func_ast1, _ = func1
    assert func_name_from_ast(func_ast1) == 'f'

    func_ast2, _ = func2
    assert func_name_from_ast(func_ast2) == 'f'


def test_return_typ_from_func(func1, func2):
    func_ast1, _ = func1
    assert return_typ_from_ast(func_ast1).is_any()

    func_ast2, _ = func2
    assert return_typ_from_ast(func_ast2).is_int()


def test_input_typs_from_ast(func2):
    func_ast2, _ = func2

    input_typs = input_typs_from_ast(func_ast2)

    assert len(input_typs) == 2
    
    a_typ = input_typs.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_int()

    b_typ = input_typs.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_int()


def test_collect_func_globals(mod8):
    '''
    test_collect_func_globals tests the capability to collect global varnames
    from a function
    '''
    mod_ast, _ = mod8
    func_ast = mod_ast.body[4]

    # this assert does not serve any testing purpose, just asserts that the
    # correct ast node is taken into account
    assert type(func_ast) is ast.FunctionDef

    global_varnames : set[str] = collect_func_globals(func_ast)
    assert global_varnames == {'o1', 'o2', 'o3'}


def test_record_vartyp():

    # TODO: repeat this test with globalvarnames into play

    var_tracker = VarTypTracker()
    var_tracker.add_local_typ('a', TypPrimitive(PrimitiveCod.INT))

    rec_coll = _record_vartyp('a', TypPrimitive(PrimitiveCod.INT), var_tracker)
    assert rec_coll == CollisionEnum.NO_COLLISION

    var_tracker = VarTypTracker()
    var_tracker.add_local_typ('a', TypPrimitive(PrimitiveCod.FLOAT))

    rec_coll = _record_vartyp('a', TypPrimitive(PrimitiveCod.INT), var_tracker)
    assert rec_coll == CollisionEnum.NO_COLLISION

    var_tracker = VarTypTracker(
        input_typs=DictTypStore({'a':TypPrimitive(PrimitiveCod.INT)})
    )

    rec_coll = _record_vartyp('a', TypPrimitive(PrimitiveCod.INT), var_tracker)
    assert rec_coll == CollisionEnum.NO_COLLISION

    var_tracker = VarTypTracker(
        input_typs=DictTypStore({'a':TypPrimitive(PrimitiveCod.FLOAT)})
    )

    rec_coll = _record_vartyp('a', TypPrimitive(PrimitiveCod.INT), var_tracker)
    assert rec_coll == CollisionEnum.INPUT_COLLISION

    var_tracker = VarTypTracker(
        outer_typs=DictTypStore({'a':TypPrimitive(PrimitiveCod.FLOAT)})
    )

    rec_coll = _record_vartyp('a', TypPrimitive(PrimitiveCod.INT), var_tracker)
    assert rec_coll == CollisionEnum.NO_COLLISION


def test_collect_from_ast_body():

    var_tracker = VarTypTracker(
        input_typs = DictTypStore({'a':TypPrimitive(PrimitiveCod.FLOAT)}),
        outer_typs = DictTypStore({'b':TypPrimitive(PrimitiveCod.FLOAT)})
    )

    code = '''
a = 7
b = 7
'''

    colliding_input_varnames : set[str] = set()
    colliding_global_varnames : set[str] = set()

    mod = ast.parse(code)

    body = mod.body

    collect_from_func_ast(
        ast_body = body,
        var_tracker = var_tracker,
        global_varnames = set()
    )

    # TODO: recheck this test

    #assert colliding_input_varnames == {'a'}
    #assert colliding_global_varnames == {'b'}


def test_collect_from_ast_body_with_annotations():
    '''
    test_collect_from_ast_body_with_annotations shall be a dedicated test
    to when code has annotations and i want to see how the typ is taken
    '''
    code = 'a : int = 0.76'
    ast_mod = ast.parse(code)
    ast_body = ast_mod.body

    # first the test is run with ignore assignment annotations
    var_tracker = VarTypTracker()

    colliding_input_varnames : set[str] = set()
    colliding_global_varnames : set[str] = set()

    collect_from_func_ast(
        ast_body = ast_body,
        var_tracker = var_tracker,
        global_varnames = set(),
        ignore_assignment_annotations = False
    )

    assert len(colliding_input_varnames) == 0
    assert len(colliding_global_varnames) == 0

    a_typ = var_tracker.get_vartyp('a')
    assert a_typ is not None
    assert a_typ.is_int()

    # second it is executed ignoring the assignment annotations

    code = 'a : int = 0.76'
    ast_mod = ast.parse(code)
    ast_body = ast_mod.body

    # empty var_tracker
    var_tracker = VarTypTracker()

    colliding_input_varnames : set[str] = set()
    colliding_global_varnames : set[str] = set()

    collect_from_func_ast(
        ast_body = ast_body,
        var_tracker = var_tracker,
        global_varnames = set(),
        ignore_assignment_annotations = True
    )

    assert len(colliding_input_varnames) == 0
    assert len(colliding_global_varnames) == 0

    a_typ = var_tracker.get_vartyp('a')
    assert a_typ is not None
    assert a_typ.is_float()


def test_func_collect1(func1):
    func_ast1, _ = func1

    local_coll = collect_local_typs(
        func_ast = func_ast1
    )

    assert len(local_coll.local_typs) == 0


def test_func_collect2(func2):
    func_ast2, _ = func2

    local_coll = collect_local_typs(
        func_ast = func_ast2
    )

    assert len(local_coll.local_typs) >= 2

    c_typ = local_coll.local_typs.get_typ('c')
    assert c_typ is not None
    assert c_typ.is_int()

    res_typ = local_coll.local_typs.get_typ('res')
    assert res_typ is not None
    assert res_typ.is_int()
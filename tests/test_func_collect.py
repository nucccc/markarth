import pytest

from markarth.convert.collect.func_collect import (
    func_name_from_ast,
    input_typs_from_ast,
    filter_const_candidates_at_func,
    return_typ_from_ast,
    collect_local_typs
)


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
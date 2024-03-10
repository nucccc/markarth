'''
testing mod colection functions
'''

import pytest

from markarth.convert.collect.mod_collect import (
    collect_func_defs,
    FuncDefData,
    collect_func_def_data,
    collect_const_candidates,
    collect_call_typs,
    mod_collect
)


def test_collect_func_defs(mod3):
    mod_ast, _ = mod3

    func_asts = collect_func_defs(mod_ast = mod_ast)

    assert len(func_asts) == 3
    assert 'f1' in func_asts.keys()
    assert 'f2' in func_asts.keys()
    assert 'f3' in func_asts.keys()


def test_collect_func_def_data(mod3):
    mod_ast, _ = mod3

    func_def_data : dict[str, FuncDefData] = collect_func_def_data(mod_ast)

    assert len(func_def_data) == 3

    f_data = func_def_data.get('f1', None)
    assert f_data is not None
    assert f_data.name == 'f1'
    assert f_data.func_ast is mod_ast.body[2]
    assert f_data.global_varnames == {'b'}
    assert f_data.return_typ.is_float()


    f_data = func_def_data.get('f2', None)
    assert f_data is not None
    assert f_data.name == 'f2'
    assert f_data.func_ast is mod_ast.body[3]
    assert f_data.global_varnames == set()
    assert f_data.return_typ.is_int()

    f_data = func_def_data.get('f3', None)
    assert f_data is not None
    assert f_data.name == 'f3'
    assert f_data.func_ast is mod_ast.body[4]
    assert f_data.global_varnames == set()
    assert f_data.return_typ.is_int()


def test_collect_const_candidates(mod3):
    mod_ast, _ = mod3

    const_candidates = collect_const_candidates(
        mod_ast = mod_ast,
        all_global_varnames = set()
    )

    assert len(const_candidates) == 2

    a_typ = const_candidates.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_int()

    b_typ = const_candidates.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_float()


def test_collect_call_typs(mod3):
    mod_ast, _ = mod3

    func_asts = collect_func_defs(mod_ast = mod_ast)

    call_typs = collect_call_typs(func_asts.values())

    assert len(call_typs) == 3

    f1_typ = call_typs.get_typ('f1')
    assert f1_typ is not None
    assert f1_typ.is_float()


    f2_typ = call_typs.get_typ('f2')
    assert f2_typ is not None
    assert f2_typ.is_int()

    f3_typ = call_typs.get_typ('f3')
    assert f3_typ is not None
    assert f3_typ.is_int()


def test_mod_collect(mod3):
    mod_ast, _ = mod3

    mod_coll_result = mod_collect(mod_ast)

    global_typs = mod_coll_result.global_typs
    assert len(global_typs) == 2

    a_typ = global_typs.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_int()

    b_typ = global_typs.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_any()

    func_colls = mod_coll_result.func_colls
    assert len(func_colls) == 3
    assert 'f1' in func_colls.keys()
    assert 'f2' in func_colls.keys()
    assert 'f3' in func_colls.keys()

    f1_typs = func_colls.get('f1').local_typs
    for typ_name , typ in f1_typs.iter_typs():
        print(typ_name)
    assert len(f1_typs) == 1

    f2_typs = func_colls.get('f2').local_typs
    assert len(f2_typs) == 1

    f3_typs = func_colls.get('f3').local_typs
    for typ_name , typ in f3_typs.iter_typs():
        print(typ_name)
    assert len(f3_typs) == 2
'''
testing mod colection functions
'''

import pytest

from markarth.convert.collect.mod_collect import (
    collect_func_defs,
    collect_const_candidates,
    filter_const_candidates
)

def test_collect_func_defs(mod3):
    mod_ast, _ = mod3

    func_asts = collect_func_defs(mod_ast = mod_ast)

    assert len(func_asts) == 3
    assert 'f1' in func_asts.keys()
    assert 'f2' in func_asts.keys()
    assert 'f3' in func_asts.keys()


def test_collect_const_candidates(mod3):
    mod_ast, _ = mod3

    const_candidates = collect_const_candidates(mod_ast = mod_ast)

    assert len(const_candidates) == 2

    a_typ = const_candidates.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_int()

    b_typ = const_candidates.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_float()


def test_filter_const_candidates(mod3):
    mod_ast, _ = mod3

    func_asts = collect_func_defs(mod_ast = mod_ast)

    const_candidates = collect_const_candidates(mod_ast = mod_ast)
    const_candidates = filter_const_candidates(
        const_candidate_names = const_candidates,
        f_colls = func_asts
    )

    assert len(const_candidates) == 1

    a_typ = const_candidates.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_int()

    b_typ = const_candidates.get_typ('b')
    assert b_typ is None
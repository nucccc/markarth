import pytest

from markarth.convert.collect.func_collector import Func
from markarth.convert.typs.names_to_typs import DictTypStore
from markarth.convert.typs import typs

def test_func1(func1):
    func_ast, codelines = func1
    func = Func(func_ast, codelines)

    assert func.name == 'f'
    assert func.return_typ.is_any()

def test_func2(func2):
    func_ast, codelines = func2
    func = Func(func_ast, codelines)

    input_typs = func._collect_input_typs()

    assert len(input_typs) == 2
    
    a_typ = input_typs.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_int()

    b_typ = input_typs.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_int()

def test_filter_const_candidates(func2):
    func_ast, codelines = func2
    func = Func(func_ast, codelines)

    const_candidates = DictTypStore({
        'c' : typs.TypPrimitive(typs.PrimitiveCod.FLOAT),
        'd' : typs.TypPrimitive(typs.PrimitiveCod.FLOAT)
    })

    func.filter_const_candidates(const_candidate_names=const_candidates)

    assert 'c' not in const_candidates
    assert 'd' in const_candidates

    assert len(const_candidates) == 1
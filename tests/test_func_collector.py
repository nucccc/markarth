import pytest

from markarth.convert.collect.func_collector import Func
from markarth.convert.typs.names_to_typs import DictTypStore
from markarth.convert.typs import typs

def test_func1(func1):
    func_ast, codelines = func1
    func = Func(func_ast, codelines)

    assert func.name == 'f'
    assert func.return_typ.is_any()

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
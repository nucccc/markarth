import pytest

from markarth.convert.collect.func_collector import Func, CollisionEnum, _collect_typs, _record_vartyp
from markarth.convert.typs.names_to_typs import DictTypStore, NamesToTyps
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


def test_record_vartyp():
    names_to_typs : NamesToTyps = NamesToTyps(
        local_typs=DictTypStore(),
        input_typs=DictTypStore({'inp1': typs.TypPrimitive(typs.PrimitiveCod.INT)}),
        global_typs=DictTypStore(),
        call_typs=DictTypStore()
    )
    collision : CollisionEnum = _record_vartyp(
        varname='inp1',
        vartyp=typs.TypPrimitive(typs.PrimitiveCod.INT),
        names_to_typs=names_to_typs
    )
    assert collision == CollisionEnum.NO_COLLISION

    collision = _record_vartyp(
        varname='inp1',
        vartyp=typs.TypPrimitive(typs.PrimitiveCod.FLOAT),
        names_to_typs=names_to_typs
    )
    assert collision == CollisionEnum.INPUT_COLLISION
    new_typ = names_to_typs.get_input_varname_typ('inp1')
    assert new_typ.is_union()

    collision = _record_vartyp(
        varname='boh',
        vartyp=typs.TypPrimitive(typs.PrimitiveCod.FLOAT),
        names_to_typs=names_to_typs
    )
    assert collision == CollisionEnum.NO_COLLISION
    new_typ = names_to_typs.get_local_varname_typ('boh')
    assert new_typ.is_float()


def test_collect_typs2(statements2):
    names_to_typs = NamesToTyps(
        local_typs=DictTypStore(),
        input_typs=DictTypStore(),
        global_typs=DictTypStore(),
        call_typs=DictTypStore()
    )
    
    coll_result = _collect_typs(statements=statements2, names_to_typs=names_to_typs)

    assert len(coll_result.collected_typs) == 4
    assert len(coll_result.colliding_input_typs) == 0
    assert len(coll_result.colliding_global_typs) == 0

    a_typ = coll_result.collected_typs.get_typ('a')
    assert a_typ is not None
    assert a_typ.is_int()

    b_typ = coll_result.collected_typs.get_typ('b')
    assert b_typ is not None
    assert b_typ.is_int()

    c_typ = coll_result.collected_typs.get_typ('c')
    assert c_typ is not None
    assert c_typ.is_int()

    d_typ = coll_result.collected_typs.get_typ('d')
    assert d_typ is not None
    assert d_typ.is_int()

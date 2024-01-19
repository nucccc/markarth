import pytest

from markarth.convert.typs import names_to_typs
from markarth.convert.typs.typs import PrimitiveCod, TypPrimitive, TypAny

def test_dict_type_store():
    types_dict = {
        'a' : TypAny(),
        'b' : TypPrimitive(PrimitiveCod.INT),
        'c' : TypPrimitive(PrimitiveCod.FLOAT)
    }

    tp = names_to_typs.DictTypStore(types_dict)

    assert tp.has('a')
    assert tp.has('b')
    assert tp.has('c')
    assert not tp.has('d')

    assert 'a' in tp
    assert 'b' in tp
    assert 'c' in tp
    assert 'd' not in tp

    a_typ = tp.get_typ('a')
    assert a_typ is not None
    assert type(a_typ) == TypAny

    b_typ = tp.get_typ('b')
    assert b_typ is not None
    assert type(b_typ) == TypPrimitive
    assert b_typ.is_int()
    
    c_typ = tp.get_typ('c')
    assert c_typ is not None
    assert type(c_typ) == TypPrimitive
    assert c_typ.is_float()

    d_typ = tp.get_typ('d')
    assert d_typ is None

    assert len(tp) == 3

    tp.delete_name('a')

    a_typ = tp.get_typ('a')
    assert a_typ is None
    
    b_typ = tp.get_typ('b')
    assert b_typ is not None
    assert type(b_typ) == TypPrimitive
    assert b_typ.is_int()
    
    c_typ = tp.get_typ('c')
    assert c_typ is not None
    assert type(c_typ) == TypPrimitive
    assert c_typ.is_float()

    d_typ = tp.get_typ('d')
    assert d_typ is None

    assert len(tp) == 2
    assert tp.size() == 2


def test_repeated_dict_typ_store():
    types_dict = {
        'a' : TypAny(),
        'b' : TypPrimitive(PrimitiveCod.INT),
        'c' : TypPrimitive(PrimitiveCod.FLOAT)
    }

    tp1 = names_to_typs.DictTypStore(types_dict)

    assert tp1.has('a')
    assert tp1.has('b')
    assert tp1.has('c')
    assert not tp1.has('d')

    '''types_dict = {
        'e' : TypAny(),
        'f' : TypPrimitive(PrimitiveCod.INT),
        'g' : TypPrimitive(PrimitiveCod.FLOAT)
    }'''

    types_dict.pop('a')
    types_dict.pop('b')
    types_dict.pop('c')

    types_dict['e'] = TypAny()
    types_dict['f'] = TypPrimitive(PrimitiveCod.INT)
    types_dict['g'] = TypPrimitive(PrimitiveCod.FLOAT)

    tp2 = names_to_typs.DictTypStore(types_dict)

    assert tp2.has('e')
    assert tp2.has('f')
    assert tp2.has('g')
    assert not tp2.has('a')
    assert not tp2.has('b')
    assert not tp2.has('c')
    assert not tp2.has('d')

    assert tp1.has('a')
    assert tp1.has('b')
    assert tp1.has('c')
    assert not tp1.has('d')
    assert not tp1.has('e')
    assert not tp1.has('f')
    assert not tp1.has('g')


def test_names_to_typs():

    v1_types_dict = {
        'a' : TypPrimitive(PrimitiveCod.INT),
        'b' : TypPrimitive(PrimitiveCod.FLOAT),
        'c' : TypPrimitive(PrimitiveCod.FLOAT)
    }

    v1_tp = names_to_typs.DictTypStore(v1_types_dict)

    v2_types_dict = {
        'd' : TypPrimitive(PrimitiveCod.FLOAT),
        'e' : TypPrimitive(PrimitiveCod.INT),
        'f' : TypPrimitive(PrimitiveCod.INT)
    }

    v2_tp = names_to_typs.DictTypStore(v2_types_dict)

    v3_types_dict = {
        'g' : TypPrimitive(PrimitiveCod.FLOAT),
        'h' : TypPrimitive(PrimitiveCod.INT),
        'i' : TypPrimitive(PrimitiveCod.INT)
    }

    v3_tp = names_to_typs.DictTypStore(v3_types_dict)

    cll_types_dict = {
        'j' : TypPrimitive(PrimitiveCod.INT),
        'k' : TypPrimitive(PrimitiveCod.FLOAT),
        'l' : TypPrimitive(PrimitiveCod.FLOAT)
    }

    cll_tp = names_to_typs.DictTypStore(cll_types_dict)

    wtg = names_to_typs.NamesToTyps(
        local_typs=v1_tp,
        input_typs=v2_tp,
        global_typs=v3_tp,
        call_typs=cll_tp
    )

    assert wtg.get_callname_typ('a') is None
    assert wtg.get_callname_typ('b') is None
    assert wtg.get_callname_typ('c') is None
    assert wtg.get_callname_typ('d') is None
    assert wtg.get_callname_typ('e') is None
    assert wtg.get_callname_typ('f') is None
    assert wtg.get_callname_typ('g') is None
    assert wtg.get_callname_typ('h') is None
    assert wtg.get_callname_typ('i') is None

    assert wtg.get_callname_typ('j') is not None
    assert wtg.get_callname_typ('j').is_int()
    assert wtg.get_callname_typ('k') is not None
    assert wtg.get_callname_typ('k').is_float()
    assert wtg.get_callname_typ('l') is not None
    assert wtg.get_callname_typ('l').is_float()

    assert wtg.get_varname_typ('a') is not None
    assert wtg.get_varname_typ('a').is_int()
    assert wtg.get_varname_typ('b') is not None
    assert wtg.get_varname_typ('b').is_float()
    assert wtg.get_varname_typ('c') is not None
    assert wtg.get_varname_typ('c').is_float()
    assert wtg.get_varname_typ('d') is not None
    assert wtg.get_varname_typ('d').is_float()
    assert wtg.get_varname_typ('e') is not None
    assert wtg.get_varname_typ('e').is_int()
    assert wtg.get_varname_typ('f') is not None
    assert wtg.get_varname_typ('f').is_int()
    assert wtg.get_varname_typ('g') is not None
    assert wtg.get_varname_typ('g').is_float()
    assert wtg.get_varname_typ('h') is not None
    assert wtg.get_varname_typ('h').is_int()
    assert wtg.get_varname_typ('i') is not None
    assert wtg.get_varname_typ('i').is_int()

    assert wtg.get_varname_typ('j') is None
    assert wtg.get_varname_typ('k') is None
    assert wtg.get_varname_typ('l') is None

    a_typ = wtg.get_varname_typ(
        varname = 'a',
        source = names_to_typs.VarNameSource.LOCAL
    )
    assert a_typ is not None
    assert a_typ.is_int()

    a_typ = wtg.get_varname_typ(
        varname = 'a',
        source = names_to_typs.VarNameSource.GLOBAL
    )
    assert a_typ is None

    d_typ = wtg.get_varname_typ(
        varname = 'd',
        source = names_to_typs.VarNameSource.INPUT
    )
    assert d_typ is not None
    assert d_typ.is_float()

    d_typ = wtg.get_varname_typ(
        varname = 'd',
        source = names_to_typs.VarNameSource.GLOBAL
    )
    assert d_typ is None

    g_typ = wtg.get_varname_typ(
        varname = 'g',
        source = names_to_typs.VarNameSource.GLOBAL
    )
    assert g_typ is not None
    assert g_typ.is_float()

    g_typ = wtg.get_varname_typ(
        varname = 'g',
        source = names_to_typs.VarNameSource.INPUT
    )
    assert g_typ is None

    wtg._update_varname_no_source('a', TypAny())
    wtg._update_varname_no_source('d', TypAny())
    wtg._update_varname_no_source('g', TypAny())

    assert wtg.get_local_varname_typ('a') is not None
    assert wtg.get_local_varname_typ('a').is_any()

    assert wtg.get_input_varname_typ('d') is not None
    assert wtg.get_input_varname_typ('d').is_any()

    assert wtg.get_global_varname_typ('g') is not None
    assert wtg.get_global_varname_typ('g').is_any()

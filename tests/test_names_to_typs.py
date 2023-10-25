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

    assert wtg.get_callname_typ('a').is_any()
    assert wtg.get_callname_typ('b').is_any()
    assert wtg.get_callname_typ('c').is_any()
    assert wtg.get_callname_typ('d').is_any()
    assert wtg.get_callname_typ('e').is_any()
    assert wtg.get_callname_typ('f').is_any()
    assert wtg.get_callname_typ('g').is_any()
    assert wtg.get_callname_typ('h').is_any()
    assert wtg.get_callname_typ('i').is_any()

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

    assert wtg.get_varname_typ('j').is_any()
    assert wtg.get_varname_typ('k').is_any()
    assert wtg.get_varname_typ('l').is_any()

    #wtg.delete_varname('a')

    #assert wtg.get_varname_type('a') is None

    #v1_tp.delete_name('a')

    #assert wtg.get_varname_type('a') is None
    #assert wtg.get_varname_type('b') == 'float'
    #assert wtg.get_varname_type('c') == 'float'
    #assert wtg.get_varname_type('d') == 'float'
    #assert wtg.get_varname_type('e') == 'int'
    #assert wtg.get_varname_type('f') == 'int' '''

'''def test_py2cy_dict_store():
    origin_type_store=names_to_typs.DictTypStore()
    origin_type_store.add_type('an_int', 'int')
    origin_type_store.add_type('a_float', 'float')
    origin_type_store.add_type('a_whatever', 'whatever')
    origin_type_store.add_type('a_bool', 'bool')

    py2cy_map={
        'int':'long',
        'float':'float',
        'bool':'char',
    }
    new_type_store = names_to_typs.py2cy_dict_store(
        origin_type_store=origin_type_store,
        py2cy_map=py2cy_map
    )
    assert len(new_type_store) == 3
    assert new_type_store.size() == 3
    assert new_type_store.get_type('an_int') == 'long'
    assert new_type_store.get_type('a_float') == 'float'
    assert new_type_store.get_type('a_bool') == 'char'

    py2cy_map={
        'int':'int',
        'float':'double',
        'bool':'char',
    }
    new_type_store = names_to_typs.py2cy_dict_store(
        origin_type_store=origin_type_store,
        py2cy_map=py2cy_map
    )
    assert len(new_type_store) == 3
    assert new_type_store.size() == 3
    assert new_type_store.get_type('an_int') == 'int'
    assert new_type_store.get_type('a_float') == 'double'
    assert new_type_store.get_type('a_bool') == 'char' '''
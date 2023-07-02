#from markarth import typestore

#import sys
#sys.path.append('../')

from markarth.core import typestore

import pytest

def test_dict_type_store():
    types_dict = {
        'a' : 'int',
        'b' : 'float',
        'c' : 'float'
    }

    tp = typestore.DictTypeStore(types_dict)

    assert tp.get_type('a') == 'int'
    assert tp.get_type('b') == 'float'
    assert tp.get_type('c') == 'float'
    assert tp.get_type('d') is None

    assert len(tp) == 3

    tp.delete_name('a')

    assert tp.get_type('a') is None
    assert tp.get_type('b') == 'float'
    assert tp.get_type('c') == 'float'
    assert tp.get_type('d') is None

    assert len(tp) == 2

def test_wrap_type_store():

    v1_types_dict = {
        'a' : 'int',
        'b' : 'float',
        'c' : 'float'
    }

    v1_tp = typestore.DictTypeStore(v1_types_dict)

    v2_types_dict = {
        'd' : 'float',
        'e' : 'int',
        'f' : 'int'
    }

    v2_tp = typestore.DictTypeStore(v2_types_dict)

    cll_types_dict = {
        'g' : 'float',
        'h' : 'int',
        'i' : 'int'
    }

    cll_tp = typestore.DictTypeStore(cll_types_dict)

    wtg = typestore.WrapTypeStore([v1_tp, v2_tp], cll_tp)

    assert wtg.get_callname_type('a') is None
    assert wtg.get_callname_type('b') is None
    assert wtg.get_callname_type('c') is None
    assert wtg.get_callname_type('d') is None
    assert wtg.get_callname_type('e') is None
    assert wtg.get_callname_type('f') is None
    assert wtg.get_callname_type('j') is None

    assert wtg.get_callname_type('g') == 'float'
    assert wtg.get_callname_type('h') == 'int'
    assert wtg.get_callname_type('i') == 'int'

    assert wtg.get_varname_type('a') == 'int'
    assert wtg.get_varname_type('b') == 'float'
    assert wtg.get_varname_type('c') == 'float'
    assert wtg.get_varname_type('d') == 'float'
    assert wtg.get_varname_type('e') == 'int'
    assert wtg.get_varname_type('f') == 'int'
    
    assert wtg.get_varname_type('j') is None

    assert wtg.get_varname_type('g') is None
    assert wtg.get_varname_type('h') is None
    assert wtg.get_varname_type('i') is None

    v1_tp.delete_name('a')

    assert wtg.get_varname_type('a') is None
    assert wtg.get_varname_type('b') == 'float'
    assert wtg.get_varname_type('c') == 'float'
    assert wtg.get_varname_type('d') == 'float'
    assert wtg.get_varname_type('e') == 'int'
    assert wtg.get_varname_type('f') == 'int'

def test_py2cy_dict_store():
    origin_type_store=typestore.DictTypeStore()
    origin_type_store.add_type('an_int', 'int')
    origin_type_store.add_type('a_float', 'float')
    origin_type_store.add_type('a_whatever', 'whatever')
    origin_type_store.add_type('a_bool', 'bool')

    py2cy_map={
        'int':'long',
        'float':'float',
        'bool':'char',
    }
    new_type_store = typestore.py2cy_dict_store(
        origin_type_store=origin_type_store,
        py2cy_map=py2cy_map
    )
    assert len(new_type_store) == 3
    assert new_type_store.get_type('an_int') == 'long'
    assert new_type_store.get_type('a_float') == 'float'
    assert new_type_store.get_type('a_bool') == 'char'

    py2cy_map={
        'int':'int',
        'float':'double',
        'bool':'char',
    }
    new_type_store = typestore.py2cy_dict_store(
        origin_type_store=origin_type_store,
        py2cy_map=py2cy_map
    )
    assert len(new_type_store) == 3
    assert new_type_store.get_type('an_int') == 'int'
    assert new_type_store.get_type('a_float') == 'double'
    assert new_type_store.get_type('a_bool') == 'char'
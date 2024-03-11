import pytest

from markarth.convert.typs.typ_store import DictTypStore
from markarth.convert.typs.typs import PrimitiveCod, TypPrimitive, TypAny

def test_dict_type_store():
    types_dict = {
        'a' : TypAny(),
        'b' : TypPrimitive(PrimitiveCod.INT),
        'c' : TypPrimitive(PrimitiveCod.FLOAT)
    }

    tp = DictTypStore(types_dict)

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

    tp1 = DictTypStore(types_dict)

    assert tp1.has('a')
    assert tp1.has('b')
    assert tp1.has('c')
    assert not tp1.has('d')

    types_dict.pop('a')
    types_dict.pop('b')
    types_dict.pop('c')

    types_dict['e'] = TypAny()
    types_dict['f'] = TypPrimitive(PrimitiveCod.INT)
    types_dict['g'] = TypPrimitive(PrimitiveCod.FLOAT)

    tp2 = DictTypStore(types_dict)

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

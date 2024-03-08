import pytest

from markarth.convert.collect.vartyp_tracker import VarTypTracker, VarOrigin
from markarth.convert.typs.names_to_typs import DictTypStore
from markarth.convert.typs.typs import PrimitiveCod, TypPrimitive, TypAny


def test_vartyp_tracker_add_and_get():
    '''
    test_vartyp_tracker_add_and_get tests an empty VarTypTracker and checks if
    after adding a variable that one is gettable
    '''

    vtt = VarTypTracker()

    a_typ = vtt.get_vartyp('a')
    assert a_typ is None
    a_typ_e_origin = vtt.get_vartyp_and_origin('a')
    assert a_typ_e_origin is None

    vtt.add_local_typ('a', TypPrimitive(PrimitiveCod.INT))

    a_typ = vtt.get_vartyp('a')
    assert a_typ is not None
    assert a_typ.is_int()
    a_typ_e_origin = vtt.get_vartyp_and_origin('a')
    assert a_typ_e_origin is not None
    assert a_typ_e_origin.typ.is_int()
    assert a_typ_e_origin.origin == VarOrigin.LOCAL


def test_vartyp_tracker_get_from_input_and_outer():

    vtt = VarTypTracker(
        input_typs=DictTypStore({
            'i1' : TypPrimitive(PrimitiveCod.INT),
            'i2' : TypPrimitive(PrimitiveCod.FLOAT),
            'i3' : TypPrimitive(PrimitiveCod.INT),
            'i4' : TypPrimitive(PrimitiveCod.BOOL),
        }),
        outer_typs=DictTypStore({
            'o1' : TypPrimitive(PrimitiveCod.INT),
            'o2' : TypPrimitive(PrimitiveCod.FLOAT),
            'o3' : TypPrimitive(PrimitiveCod.STR),
        })
    )

    # checking for input variables
    i1_typ = vtt.get_vartyp('i1')
    assert i1_typ is not None
    assert i1_typ.is_int()
    i1_typ_e_origin = vtt.get_vartyp_and_origin('i1')
    assert i1_typ_e_origin is not None
    assert i1_typ_e_origin.typ.is_int()
    assert i1_typ_e_origin.origin == VarOrigin.INPUT

    i1_typ = vtt.get_vartyp('i2')
    assert i1_typ is not None
    assert i1_typ.is_float()
    i1_typ_e_origin = vtt.get_vartyp_and_origin('i2')
    assert i1_typ_e_origin is not None
    assert i1_typ_e_origin.typ.is_float()
    assert i1_typ_e_origin.origin == VarOrigin.INPUT

    i1_typ = vtt.get_vartyp('i3')
    assert i1_typ is not None
    assert i1_typ.is_int()
    i1_typ_e_origin = vtt.get_vartyp_and_origin('i3')
    assert i1_typ_e_origin is not None
    assert i1_typ_e_origin.typ.is_int()
    assert i1_typ_e_origin.origin == VarOrigin.INPUT

    i1_typ = vtt.get_vartyp('i4')
    assert i1_typ is not None
    assert i1_typ.is_bool()
    i1_typ_e_origin = vtt.get_vartyp_and_origin('i4')
    assert i1_typ_e_origin is not None
    assert i1_typ_e_origin.typ.is_bool()
    assert i1_typ_e_origin.origin == VarOrigin.INPUT


    # checking for outer variables
    i1_typ = vtt.get_vartyp('o1')
    assert i1_typ is not None
    assert i1_typ.is_int()
    i1_typ_e_origin = vtt.get_vartyp_and_origin('o1')
    assert i1_typ_e_origin is not None
    assert i1_typ_e_origin.typ.is_int()
    assert i1_typ_e_origin.origin == VarOrigin.OUTER

    i1_typ = vtt.get_vartyp('o2')
    assert i1_typ is not None
    assert i1_typ.is_float()
    i1_typ_e_origin = vtt.get_vartyp_and_origin('o2')
    assert i1_typ_e_origin is not None
    assert i1_typ_e_origin.typ.is_float()
    assert i1_typ_e_origin.origin == VarOrigin.OUTER

    i1_typ = vtt.get_vartyp('o3')
    assert i1_typ is not None
    assert i1_typ.is_str()
    i1_typ_e_origin = vtt.get_vartyp_and_origin('o3')
    assert i1_typ_e_origin is not None
    assert i1_typ_e_origin.typ.is_str()
    assert i1_typ_e_origin.origin == VarOrigin.OUTER
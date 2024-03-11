import pytest

from markarth.convert.collect.vartyp_tracker import VarTypTracker, VarOrigin
from markarth.convert.typs.typ_store import DictTypStore
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
    '''
    test_vartyp_tracker_get_from_input_and_outer is testing whether input and
    outer variables can be obtained
    '''

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

    i2_typ = vtt.get_vartyp('i2')
    assert i2_typ is not None
    assert i2_typ.is_float()
    i2_typ_e_origin = vtt.get_vartyp_and_origin('i2')
    assert i2_typ_e_origin is not None
    assert i2_typ_e_origin.typ.is_float()
    assert i2_typ_e_origin.origin == VarOrigin.INPUT

    i3_typ = vtt.get_vartyp('i3')
    assert i3_typ is not None
    assert i3_typ.is_int()
    i3_typ_e_origin = vtt.get_vartyp_and_origin('i3')
    assert i3_typ_e_origin is not None
    assert i3_typ_e_origin.typ.is_int()
    assert i3_typ_e_origin.origin == VarOrigin.INPUT

    i4_typ = vtt.get_vartyp('i4')
    assert i4_typ is not None
    assert i4_typ.is_bool()
    i4_typ_e_origin = vtt.get_vartyp_and_origin('i4')
    assert i4_typ_e_origin is not None
    assert i4_typ_e_origin.typ.is_bool()
    assert i4_typ_e_origin.origin == VarOrigin.INPUT


    # checking for outer variables
    o1_typ = vtt.get_vartyp('o1')
    assert o1_typ is not None
    assert o1_typ.is_int()
    o1_typ_e_origin = vtt.get_vartyp_and_origin('o1')
    assert o1_typ_e_origin is not None
    assert o1_typ_e_origin.typ.is_int()
    assert o1_typ_e_origin.origin == VarOrigin.OUTER

    o2_typ = vtt.get_vartyp('o2')
    assert o2_typ is not None
    assert o2_typ.is_float()
    o2_typ_e_origin = vtt.get_vartyp_and_origin('o2')
    assert o2_typ_e_origin is not None
    assert o2_typ_e_origin.typ.is_float()
    assert o2_typ_e_origin.origin == VarOrigin.OUTER

    o3_typ = vtt.get_vartyp('o3')
    assert o3_typ is not None
    assert o3_typ.is_str()
    o3_typ_e_origin = vtt.get_vartyp_and_origin('o3')
    assert o3_typ_e_origin is not None
    assert o3_typ_e_origin.typ.is_str()
    assert o3_typ_e_origin.origin == VarOrigin.OUTER


def test_get_vartyp_and_origin_precedence():
    '''
    shall test whether having a variable with overlapping names between local,
    input and outer shall lead to a precedence
    '''

    vtt = VarTypTracker(
        input_typs=DictTypStore({
            'v1' : TypPrimitive(PrimitiveCod.FLOAT),
            'v2' : TypPrimitive(PrimitiveCod.FLOAT),
            'v4' : TypPrimitive(PrimitiveCod.FLOAT),
        }),
        outer_typs=DictTypStore({
            'v1' : TypPrimitive(PrimitiveCod.BOOL),
            'v3' : TypPrimitive(PrimitiveCod.BOOL),
            'v4' : TypPrimitive(PrimitiveCod.BOOL),
        })
    )

    vtt.add_local_typ('v1', TypPrimitive(PrimitiveCod.INT))
    vtt.add_local_typ('v2', TypPrimitive(PrimitiveCod.INT))
    vtt.add_local_typ('v3', TypPrimitive(PrimitiveCod.INT))


    v_typ = vtt.get_vartyp('v1')
    assert v_typ is not None
    assert v_typ.is_int()
    v_typ_e_origin = vtt.get_vartyp_and_origin('v1')
    assert v_typ_e_origin is not None
    assert v_typ_e_origin.typ.is_int()
    assert v_typ_e_origin.origin == VarOrigin.LOCAL

    v_typ = vtt.get_vartyp('v2')
    assert v_typ is not None
    assert v_typ.is_int()
    v_typ_e_origin = vtt.get_vartyp_and_origin('v2')
    assert v_typ_e_origin is not None
    assert v_typ_e_origin.typ.is_int()
    assert v_typ_e_origin.origin == VarOrigin.LOCAL

    v_typ = vtt.get_vartyp('v3')
    assert v_typ is not None
    assert v_typ.is_int()
    v_typ_e_origin = vtt.get_vartyp_and_origin('v3')
    assert v_typ_e_origin is not None
    assert v_typ_e_origin.typ.is_int()
    assert v_typ_e_origin.origin == VarOrigin.LOCAL

    v_typ = vtt.get_vartyp('v4')
    assert v_typ is not None
    assert v_typ.is_float()
    v_typ_e_origin = vtt.get_vartyp_and_origin('v4')
    assert v_typ_e_origin is not None
    assert v_typ_e_origin.typ.is_float()
    assert v_typ_e_origin.origin == VarOrigin.INPUT


def test_get_call_typ():
    '''
    test_get_call_typ tests the calltyp out of the vartyptracker
    '''
    
    vtt = VarTypTracker(
        call_typs=DictTypStore({
            'f1' : TypPrimitive(PrimitiveCod.INT),
            'f2' : TypPrimitive(PrimitiveCod.FLOAT),
            'f3' : TypPrimitive(PrimitiveCod.BOOL)
        })
    )

    f_typ = vtt.get_call_typ('f1')
    assert f_typ is not None
    assert f_typ.is_int()

    f_typ = vtt.get_call_typ('f2')
    assert f_typ is not None
    assert f_typ.is_float()

    f_typ = vtt.get_call_typ('f3')
    assert f_typ is not None
    assert f_typ.is_bool()

    f_typ = vtt.get_call_typ('f4')
    assert f_typ is None


def test_typ_store_from_origin():

    vtt = VarTypTracker()

    assert vtt._typ_store_from_origin(VarOrigin.LOCAL) is vtt.local_typs
    assert vtt._typ_store_from_origin(VarOrigin.INPUT) is vtt.input_typs
    assert vtt._typ_store_from_origin(VarOrigin.OUTER) is vtt.outer_typs


def test_update_vartyp():
    '''
    test_update_vartyp tests the update method
    '''

    vtt = VarTypTracker(
        input_typs=DictTypStore({
            'i1' : TypPrimitive(PrimitiveCod.INT),
        }),
        outer_typs=DictTypStore({
            'o1' : TypPrimitive(PrimitiveCod.INT),
        })
    )

    vtt.add_local_typ(varname = 'l1', vartyp = TypPrimitive(PrimitiveCod.INT))


    vtt.update_vartyp('l1', TypAny(), VarOrigin.LOCAL)

    v_typ_e_origin = vtt.get_vartyp_and_origin('l1')
    assert v_typ_e_origin is not None
    assert v_typ_e_origin.typ.is_any()
    assert v_typ_e_origin.origin == VarOrigin.LOCAL

    
    vtt.update_vartyp('i1', TypPrimitive(PrimitiveCod.FLOAT), VarOrigin.INPUT)

    v_typ_e_origin = vtt.get_vartyp_and_origin('i1')
    assert v_typ_e_origin is not None
    assert v_typ_e_origin.typ.is_float()
    assert v_typ_e_origin.origin == VarOrigin.INPUT

    vtt.update_vartyp('o1', TypPrimitive(PrimitiveCod.FLOAT), VarOrigin.OUTER)

    v_typ_e_origin = vtt.get_vartyp_and_origin('o1')
    assert v_typ_e_origin is not None
    assert v_typ_e_origin.typ.is_float()
    assert v_typ_e_origin.origin == VarOrigin.OUTER
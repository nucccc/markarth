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
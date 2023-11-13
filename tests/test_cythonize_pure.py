import pytest

from markarth.convert.typs.typs import PrimitiveCod, TypPrimitive
from markarth.convert.typs.names_to_typs import DictTypStore
from markarth.convert.cythonize.cy_typs import CyFloat, CyInt
from markarth.convert.cythonize.pure import cython_imported_already, typ_store_to_varnames

def test_is_cython_imported(code1, mod2):
    mod_ast, _ = code1

    is_cython_imported, alias, line_no = cython_imported_already(mod_ast)
    assert not is_cython_imported

    mod_ast, _ = mod2

    is_cython_imported, alias, line_no = cython_imported_already(mod_ast)
    assert is_cython_imported
    assert alias == 'cython'
    assert line_no == 2


def test_typ_store_to_varnames():
    typ_store = DictTypStore({
        'a' : TypPrimitive(PrimitiveCod.INT),
        'b' : TypPrimitive(PrimitiveCod.FLOAT),
        'c' : TypPrimitive(PrimitiveCod.BOOL),
        'd' : TypPrimitive(PrimitiveCod.STR)
    })

    tuples = set(typ_store_to_varnames(
        typ_store = typ_store,
        default_cy_int=CyInt.INT,
        default_cy_float=CyFloat.FLOAT
    ))

    expected_tuples = {
        ('a', 'int'),
        ('b', 'float'),
        ('c', 'char'),
    }

    assert tuples == expected_tuples
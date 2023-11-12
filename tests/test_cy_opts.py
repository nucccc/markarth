'''
yeah somewhere these pydantic models should be tested
'''

import pytest

from markarth.convert.cythonize.cy_options import ModOpts, FuncOpts
from markarth.convert.cythonize.cy_typs import CyFloat, CyInt

def test_default_func_opts():
    func_opts = FuncOpts(parent_mod=ModOpts())
    
    assert func_opts.internal_default_int_cytyp is None
    assert func_opts.internal_default_float_cytyp is None


def test_default_mod_opts():
    mod_opts = ModOpts()

    assert mod_opts.default_int_cytyp == CyInt.INT
    assert mod_opts.default_float_cytyp == CyFloat.FLOAT

def test_parent_mod():

    mod_opts = ModOpts(
        default_float_cytyp=CyFloat.DOUBLE,
        default_int_cytyp=CyInt.SHORT
    )

    func_opts1 = FuncOpts(
        parent_mod=mod_opts
    )

    assert func_opts1.default_float_cytyp == CyFloat.DOUBLE
    assert func_opts1.default_int_cytyp == CyInt.SHORT

    func_opts2 = FuncOpts(
        parent_mod=mod_opts,
        internal_default_int_cytyp=CyInt.LONG
    )

    assert func_opts2.default_float_cytyp == CyFloat.DOUBLE
    assert func_opts2.default_int_cytyp == CyInt.LONG

    func_opts3 = FuncOpts(
        parent_mod=mod_opts,
        internal_default_float_cytyp=CyFloat.FLOAT
    )

    assert func_opts3.default_float_cytyp == CyFloat.FLOAT
    assert func_opts3.default_int_cytyp == CyInt.SHORT
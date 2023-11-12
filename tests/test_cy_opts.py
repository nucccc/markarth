'''
yeah somewhere these pydantic models should be tested
'''

import pytest

from markarth.convert.cythonize.cy_options import ModOpts, FuncOpts
from markarth.convert.cythonize.cy_typs import CyFloat, CyInt

def test_default_func_opts():
    func_opts = FuncOpts()
    
    assert func_opts.default_int_cytyp is None
    assert func_opts.default_float_cytyp is None


def test_default_mod_opts():
    mod_opts = ModOpts()

    assert mod_opts.default_int_cytyp == CyInt.INT
    assert mod_opts.default_float_cytyp == CyFloat.FLOAT
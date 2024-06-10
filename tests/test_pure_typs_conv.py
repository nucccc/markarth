'''
aimed at testing how cy_typs are converted into cython
'''


from markarth.convert.cythonize.cy_typs import CyFloat, CyInt
from markarth.convert.cythonize.pure_funcs.typs_conv import (
    cy_int_str_pure,
    cy_float_str_pure
)

def test_cy_int_str_pure():
    assert cy_int_str_pure(CyInt.SHORT) == 'short'
    assert cy_int_str_pure(CyInt.INT) == 'int'
    assert cy_int_str_pure(CyInt.LONG) == 'long'
    assert cy_int_str_pure(CyInt.LONGLONG) == 'longlong'

def test_cy_float_str_pure():
    assert cy_float_str_pure(CyFloat.FLOAT) == 'float'
    assert cy_float_str_pure(CyFloat.DOUBLE) == 'double'
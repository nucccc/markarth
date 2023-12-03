import pytest

from markarth.convert.cythonize.cy_typs import (
    cy_int_str,
    cy_float_str,
    CyInt,
    CyFloat
)


def test_cy_int_str():
    assert cy_int_str(CyInt.SHORT) == 'short'
    assert cy_int_str(CyInt.INT) == 'int'
    assert cy_int_str(CyInt.LONG) == 'long'
    assert cy_int_str(CyInt.LONGLONG) == 'longlong'


def test_cy_float_str():
    assert cy_float_str(CyFloat.FLOAT) == 'float'
    assert cy_float_str(CyFloat.DOUBLE) == 'double'
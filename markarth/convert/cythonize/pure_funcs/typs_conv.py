'''
typs_conv has functions to convert typs to cython typs in pure python syntax
'''

from markarth.convert.cythonize.cy_typs import CyFloat, CyInt

CY_BOOL_PURE = 'char'

def cy_int_str_pure(cy_int : CyInt) -> str:
    match cy_int:
        case CyInt.SHORT:
            return 'short'
        case CyInt.INT:
            return 'int'
        case CyInt.LONG:
            return 'long'
        case CyInt.LONGLONG:
            return 'longlong'
        

def cy_float_str_pure(cy_float : CyFloat) -> str:
    match cy_float:
        case CyFloat.FLOAT:
            return 'float'
        case CyFloat.DOUBLE:
            return 'double'
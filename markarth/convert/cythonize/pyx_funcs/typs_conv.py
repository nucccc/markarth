'''
here in typs_conv I want to have functions for typ conversion from typs to cy typs
'''

from markarth.convert.cythonize.cy_typs import CyFloat, CyInt

CY_BOOL_PYX = 'char'

def cy_int_str_pyx(cy_int : CyInt) -> str:
    match cy_int:
        case CyInt.SHORT:
            return 'short int'
        case CyInt.INT:
            return 'int'
        case CyInt.LONG:
            return 'long int'
        case CyInt.LONGLONG:
            return 'long long'
        

def cy_float_str_pyx(cy_float : CyFloat) -> str:
    match cy_float:
        case CyFloat.FLOAT:
            return 'float'
        case CyFloat.DOUBLE:
            return 'double'
'''
yeah there are also cython typs
'''

from enum import Enum

CY_BOOL = 'char'

class CyInt(Enum):
    SHORT = 0
    INT = 1
    LONG = 2
    LONGLONG = 3


class CyFloat(Enum):
    FLOAT = 0
    DOUBLE = 1


def cy_int_str(cy_int : CyInt) -> str:
    match cy_int:
        case CyInt.SHORT:
            return 'short'
        case CyInt.INT:
            return 'int'
        case CyInt.LONG:
            return 'long'
        case CyInt.LONGLONG:
            return 'longlong'
        

def cy_float_str(cy_float : CyFloat) -> str:
    match cy_float:
        case CyFloat.FLOAT:
            return 'float'
        case CyFloat.DOUBLE:
            return 'double'


cy_int_typstrs = {
    CyInt.SHORT : 'short',
    CyInt.INT : 'int',
    CyInt.LONG : 'long',
    CyInt.LONGLONG : 'longlong'
}

cy_int_typstrs = {
    CyInt.SHORT : 'short',
    CyInt.INT : 'int',
    CyInt.LONG : 'long',
    CyInt.LONGLONG : 'longlong'
}

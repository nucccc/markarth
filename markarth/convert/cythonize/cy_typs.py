'''
yeah there are also cython typs
'''

from enum import Enum

class CyInt(Enum):
    SHORT = 0
    INT = 1
    LONG = 2
    LONGLONG = 3

class CyFloat(Enum):
    FLOAT = 0
    DOUBLE = 1

cy_int_types = [
    'int',
    'long',
    'longlong'
]


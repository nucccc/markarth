'''
THIS IS COMPLETELY DEPRECATED

DELETE THIS ONCE EVERYTHING IS A LITTLE BIT MORE TESTED

nobody knows what this is going to contain
'''

from enum import Enum

#class 

class PrimitiveType(Enum):
    NONE = 0
    INT = 1
    FLOAT = 2
    BOOL = 3
    STR = 4
    UNKNOWN = 5

class ValueContainer:
    '''
    this could be some class to represent lists and sets
    '''
    pass

class KeyValueContainer:
    '''
    this could represent dicts
    '''
    pass

class VarTracker:
    '''
    VarTracker shall track variables, checking their types, tracking if they
    have more than one type along the software execution
    '''

    def __init__(self, varname : str):
        self._varname = varname
        #_types_gone shall be a set of the types the variable went through
        self._types_gone = set()

class VarTrackingResult:
    '''
    VarTrackingResult shall represent the result of a var tracking inside
    a function
    '''
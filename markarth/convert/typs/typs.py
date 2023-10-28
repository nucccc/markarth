'''
okay some class for the type could have been useful
'''

from enum import Enum

class InvalidPrimitiveStr(Exception):
    'Raised when primitive type string is not valid'
    pass


class PrimitiveCod(Enum):
    '''
    you know there are a limited amount of primitive types, hopefully this enum
    will do the job
    '''
    BOOL = 0
    FLOAT = 1
    INT = 2
    STR = 3


_prim_str_to_cod : dict[str:PrimitiveCod] = {
    'bool' : PrimitiveCod.BOOL,
    'float' : PrimitiveCod.FLOAT,
    'int' : PrimitiveCod.INT,
    'str' : PrimitiveCod.STR
}


_prim_cod_to_str : dict[PrimitiveCod:str] = {
    prim_cod : prim_str
    for prim_str, prim_cod
    in _prim_str_to_cod.items()
}


def str_to_prim_cod(prim_str : str) -> PrimitiveCod:
    prim = _prim_str_to_cod.get(prim_str, None)
    if prim is None:
        raise InvalidPrimitiveStr
    return prim


def prim_cod_to_str(prim_cod : PrimitiveCod) -> str:
    return _prim_cod_to_str[prim_cod]


def str_to_prim_cod_or_none(primitive_str : str) -> PrimitiveCod | None:
    return _prim_str_to_cod.get(primitive_str, None)


class Typ:
    '''
    i don't even know if this should be abstract at a point, but let's
    start to write it
    '''

    def __init__(self):
        pass

    def __eq__(self, other_typ : 'Typ') -> bool:
        return other_typ.as_string() == self.as_string()

    def is_primitive(self) -> bool:
        # by default i would like to have a typ not being a primitive,
        # atual primitive types shall have this a 
        return False
    
    def is_any(self) -> bool:
        return False

    def is_container(self) -> bool:
        return False
    
    def is_none(self) -> bool:
        return False
    
    def is_bool(self) -> bool:
        return False
    
    def is_float(self) -> bool:
        return False
    
    def is_int(self) -> bool:
        return False
    
    def is_str(self) -> bool:
        return False
    
    def is_union(self) -> bool:
        return False

    def as_string(self) -> str:
        '''
        as_string shall convert the given type to a string
        '''
        raise NotImplementedError


class TypPrimitive(Typ):
    '''
    TypPrimitive shall represent a primitive type
    '''

    def __init__(self, prim : str | PrimitiveCod):
        if type(prim) == str:
            self._prim_str : str = prim
            self._prim_cod : PrimitiveCod = str_to_prim_cod(self._prim_str)
        elif type(prim) == PrimitiveCod:
            self._prim_cod : PrimitiveCod = prim
            self._prim_str : str = prim_cod_to_str(self._prim_cod)

    def is_primitive(self) -> bool:
        return True
    
    def as_string(self) -> str:
        '''
        as_string shall convert the given type to a string
        '''
        return self._prim_str
    
    def get_primitive_cod(self) -> PrimitiveCod:
        return self._prim_cod
    
    def is_bool(self) -> bool:
        return self._prim_cod == PrimitiveCod.BOOL
    
    def is_float(self) -> bool:
        return self._prim_cod == PrimitiveCod.FLOAT
    
    def is_int(self) -> bool:
        return self._prim_cod == PrimitiveCod.INT
    
    def is_str(self) -> bool:
        return self._prim_cod == PrimitiveCod.STR


class TypAny(Typ):
    '''
    TypAny shall describe an any type
    '''

    def __init__(self):
        pass

    def is_any(self) -> bool:
        return True
    
    def as_string(self) -> str:
        return 'any'
    

class TypNone(Typ):
    '''
    TypNone shall describe the None type, especially useful with unions
    '''

    def __init__(self):
        pass

    def is_none(self) -> bool:
        return True
    
    def as_string(self) -> str:
        return 'None'
    
class TypUnion(Typ):
    '''
    TypUnion shall represent a union of types
    '''

    def __init__(self):
        self.union_types :list[Typ] = list()

    def is_union(self) -> bool:
        return True
    
    @property
    def get_union_types(self) -> list[Typ]:
        return self.union_types
    
    def add_typ(self, typ : Typ) -> None:
        if type(typ) == TypUnion:
            for sub_typ in typ.get_union_types:
                self.add_typ(sub_typ)
        else:
            for sub_typ in self.union_types:
                if sub_typ == typ:
                    break
            else:
                self.union_types.append(typ)

    def as_string(self) -> str:
        return '|'.join(typ.as_string() for typ in self.union_types)
    

'''
var_store shall somehow relate variable (and function too) names to their types,
while at the same time allowing for modifications (you know if something happens
to go through)
'''

from copy import deepcopy
from enum import Enum
from typing import Iterator, Protocol

from markarth.core.types.types import Typ, TypUnknown

class TypStore(Protocol):
    '''
    TypStore is a protocol (may be seen as an interface) to something that
    just return a typ
    '''

    def get_typ(self, name : str) -> Typ | None:
        pass # pragma: no cover

    def add_typ(self, name : str, typ : Typ):
        pass # pragma: no cover

    def delete_name(self, name : str) -> bool:
        pass # pragma: no cover

    def iter_typs(self) -> Iterator[ tuple[str, Typ] ]:
        pass # pragma: no cover

    def size(self) -> int:
        pass # pragma: no cover


class DictTypeStore():
    _types_dict : dict[str, str]

    def __init__(self, types_dict : dict[str, Typ] = dict()):
        self._types_dict : dict[str, Typ] = deepcopy(types_dict)

    def get_typ(self, name : str) -> Typ | None:
        return self._types_dict.get(name, None)
    
    def add_typ(self, name : str, typ : Typ):
        self._types_dict[name] = typ
    
    def delete_name(self, name : str) -> bool:
        popped = self._types_dict.pop(name, None)
        return popped is not None

    def iter_typs(self) -> Iterator[ tuple[str, Typ] ]:
        for varname, typ in self._types_dict.items():
            yield (varname, typ)

    def __len__(self):
        return len(self._types_dict)
    
    def size(self) -> int:
        return len(self)


class VarNameSource(Enum):
    '''
    VarNameSource is important because it reprent the three different
    sources for a variable name:
     - local: variable names which are discovered while going through the
        statements of a function
     - input: variable names provided in input to the function, collisions may
        be possible, and it would be good to point them out
     - global: variable names coming from the outer scope of the module, like
        constants, i still need to think if i want for them to conceive
        collisions
    '''
    LOCAL = 0
    INPUT = 1
    GLOBAL = 2


class NamesToTyps():
    '''
    NamesToTyps shall wrap several types getters in order
    to have more than one source for types
    '''

    def __init__(
        self,
        local_typs : TypStore = DictTypeStore(),
        input_typs : TypStore = DictTypeStore(),
        global_typs : TypStore = DictTypeStore(),
        call_typs : TypStore  = DictTypeStore()
    ):
        self._local_typs : TypStore = local_typs
        self._input_typs : TypStore = input_typs
        self._global_typs : TypStore = global_typs
        self._call_typs : TypStore = call_typs

        # for practicality i shall have a quick list of the internal typ stores
        # addressing variable names
        self._var_typ_stores : list[TypStore] = [
            local_typs,
            input_typs,
            global_typs
        ]

        # i would like this to keep track of the times in which i needed
        # to change the type of an input variable (weird stuff in code may be
        # found)
        self._collided_input_varnames : set[str] = set()


    def get_varname_typ(self, varname : str) -> Typ:
        for typ_store in self._var_typ_stores:
            typ = typ_store.get_typ(varname)
            if typ is not None:
                return typ
        return TypUnknown()

    
    def delete_varname(self, varname : str):
        '''
        HERE THIS THING SHALL BE HEAVILY REFACTORED
        '''
        for i, typ_store in enumerate(self._var_typ_stores):
            typ_store.delete_name(varname)

            if i == VarNameSource.INPUT:
                self._collided_input_varnames.add(varname)


    def get_callname_typ(self, call_name : str) -> Typ:
        typ = self._call_typs.get_type(call_name)
        if typ is None:
            typ = TypUnknown()
        return typ

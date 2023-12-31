'''
var_store shall somehow relate variable (and function too) names to their types,
while at the same time allowing for modifications (you know if something happens
to go through)
'''

from copy import deepcopy
from enum import Enum
from typing import Iterator, Protocol

from markarth.convert.typs.typs import Typ
from markarth.convert.typs.merge_typs import merge_typs

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

    def has(self, name : str) -> bool:
        pass # pragma: no cover


class DictTypStore():
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
    
    def __contains__(self, name : str) -> bool:
        return name in self._types_dict.keys()

    def has(self, name : str) -> bool:
        return name in self


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
        local_typs : TypStore = DictTypStore(),
        input_typs : TypStore = DictTypStore(),
        global_typs : TypStore = DictTypStore(),
        call_typs : TypStore  = DictTypStore()
    ):
        self._local_typs : TypStore = local_typs
        self._input_typs : TypStore = input_typs
        self._global_typs : TypStore = global_typs
        self._call_typs : TypStore = call_typs

        # for practicality i shall have a quick list of the internal typ stores
        # addressing variable names
        self._var_typ_stores : list[tuple[TypStore, VarNameSource]] = [
            (local_typs, VarNameSource.LOCAL),
            (input_typs, VarNameSource.INPUT),
            (global_typs, VarNameSource.GLOBAL)
        ]

        # i would like this to keep track of the times in which i needed
        # to change the type of an input variable (weird stuff in code may be
        # found)
        self._collided_input_varnames : set[str] = set()
        self._collided_global_varnames : set[str] = set()

    
    @property
    def local_typs(self) -> TypStore:
        return self._local_typs


    def get_varname_typ(
        self,
        varname : str,
        source : VarNameSource | None = None
    ) -> Typ | None:
        if source is None:
            typ, _ = self.get_varname_typ_and_source(varname)
            return typ
        store = self._get_store(source)
        return store.get_typ(varname)
    

    def get_varname_typ_and_source(self, varname : str) -> tuple[Typ | None, VarNameSource]:
        for typ_store, source in self._var_typ_stores:
            typ = typ_store.get_typ(varname)
            if typ is not None:
                return (typ, source)
        return (None, VarNameSource.LOCAL) # by default in case of none i return local as the source
    

    def get_local_varname_typ(self, varname : str) -> Typ | None:
        return self._local_typs.get_typ(varname)
    

    def get_input_varname_typ(self, varname : str) -> Typ | None:
        return self._input_typs.get_typ(varname)
    

    def get_global_varname_typ(self, varname : str) -> Typ | None:
        return self._global_typs.get_typ(varname)
    
    
    def _get_store(self, source : VarNameSource) -> TypStore:
        match source:
            case VarNameSource.LOCAL:
                return self._local_typs
            case VarNameSource.INPUT:
                return self._input_typs
            case VarNameSource.GLOBAL:
                return self._global_typs
            
    
    
    #def delete_varname(self, varname : str):
    #    '''
    #    HERE THIS THING SHALL BE HEAVILY REFACTORED
    #    '''
    #    for i, typ_store in enumerate(self._var_typ_stores):
    #        typ_store.delete_name(varname)
    #
    #        if i == VarNameSource.INPUT:
    #            self._collided_input_varnames.add(varname)


    def get_callname_typ(self, call_name : str) -> Typ | None:
        return self._call_typs.get_typ(call_name)
    

    def update_varname(
        self,
        varname : str,
        typ : Typ,
        source : VarNameSource | None = None
    ) -> None:
        '''
        this shall be sued somehow when
        '''
        if source is not None:
            self._update_varname_with_source(varname, typ, source)
        else:
            self._update_varname_no_source(varname, typ)
    

    def _update_varname_with_source(
        self,
        varname : str,
        typ : Typ,
        source : VarNameSource
    ) -> None:
        '''
        _update_varname_with_source selects the store given the source in input
        '''
        match source:
            case VarNameSource.LOCAL:
                self._local_typs.add_typ(varname, typ)
            case VarNameSource.INPUT:
                self._input_typs.add_typ(varname, typ)
            case VarNameSource.GLOBAL:
                self._global_typs.add_typ(varname, typ)


    def _update_varname_no_source(self, varname : str, typ : Typ) -> None:
        for typ_store, source in self._var_typ_stores:
            old_typ = typ_store.get_typ(varname)
            if old_typ is not None:
                typ_store.add_typ(varname, typ)
                if source == VarNameSource.INPUT:
                    self._collided_global_varnames.add(varname)
                elif source == VarNameSource.GLOBAL:
                    self._collided_global_varnames.add(varname)
                return


    def put_local_typ(self, varname : str, typ : Typ) -> None:
        '''
        
        '''
        self.local_typs.add_typ(varname, typ)
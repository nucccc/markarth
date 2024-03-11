from dataclasses import dataclass
from enum import Enum

from markarth.convert.typs.typ_store import DictTypStore, TypStore
from markarth.convert.typs.typs import Typ

DEFAULT_TYP_STORE_TYPE = DictTypStore


class VarOrigin(Enum):
    '''
    VarOrigin is important because it reprent the three different
    sources for a variable name:
     - local: variable names which are discovered while going through the
        statements of a function
     - input: variable names provided in input to the function, collisions may
        be possible, and it would be good to point them out
     - outer: variable names coming from the outer scope of the module, like
        constants, i still need to think if i want for them to conceive
        collisions
    '''
    LOCAL = 0
    INPUT = 1
    OUTER = 2


@dataclass
class VarTypEOrigin:
    typ : Typ
    origin : VarOrigin


class VarTypTracker:
    '''
    VarTypTracker shall be used to hold typstores from different sources,
    used to track the type that every variable is going through a function
    '''

    def __init__(
        self,
        input_typs : TypStore | None = None,
        outer_typs : TypStore | None = None,
        call_typs : TypStore | None = None,
        global_narnames : set[str] | None = None
    ):
        self.local_typs : DEFAULT_TYP_STORE_TYPE = DEFAULT_TYP_STORE_TYPE()
        self.input_typs : TypStore = input_typs if input_typs is not None else DEFAULT_TYP_STORE_TYPE()
        self.outer_typs : TypStore = outer_typs if outer_typs is not None else DEFAULT_TYP_STORE_TYPE()
        self.call_typs : TypStore = call_typs if call_typs is not None else DEFAULT_TYP_STORE_TYPE()
        self.global_narnames : set[str] = global_narnames if global_narnames is not None else set()

        self.input_collisions : set[str] = set()

    def get_vartyp_and_origin(self, varname : str) -> VarTypEOrigin | None:
        '''
        get_vartyp_and_origin returns a variable's typ and its origin, otherwise
        None if the variable is unknown
        '''
        # i check one by one the different typ stores, giving precedence to the
        # local one which could contain an eventual local redeclaration of a
        # variable,# independent of the outer scope
        
        # local varnames check
        local_typ = self.local_typs.get_typ(varname)
        if local_typ is not None:
            return VarTypEOrigin(typ=local_typ, origin=VarOrigin.LOCAL)
        
        # input varnames check
        input_typ = self.input_typs.get_typ(varname)
        if input_typ is not None:
            return VarTypEOrigin(typ=input_typ, origin=VarOrigin.INPUT)
        
        # outer varnames check
        outer_typ = self.outer_typs.get_typ(varname)
        if outer_typ is not None:
            return VarTypEOrigin(typ=outer_typ, origin=VarOrigin.OUTER)
        
        # in case of previous failures i return None
        return None
    

    def get_vartyp(self, varname : str) -> Typ | None:
        '''
        get_vartyp
        '''
        vartyp_e_origin = self.get_vartyp_and_origin(varname)
        return vartyp_e_origin.typ if vartyp_e_origin is not None else None
    

    def add_local_typ(self, varname : str, vartyp : Typ):
        '''
        add_local_typ adds a typ to the local typstore
        '''
        self.local_typs.add_typ(name = varname, typ = vartyp)

    
    def _typ_store_from_origin(self, origin : VarOrigin) -> TypStore:
        '''
        _typ_store_from_origin returns a reference to an internal typstore given an
        origin
        '''
        match origin:
            case VarOrigin.LOCAL:
                return self.local_typs
            case VarOrigin.INPUT:
                return self.input_typs
            case VarOrigin.OUTER:
                return self.outer_typs


    def update_vartyp(self, varname : str, vartyp : Typ, origin : VarOrigin):
        '''
        update_vartyp adds a vartyp given its origin, in the sense that the origin
        enum specifies the typstore to be updated, either local, input, or outer
        '''
        # NOTE: should this method ever be invoked with outer as an origin???
        typstore_to_update = self._typ_store_from_origin(origin = origin)
        typstore_to_update.add_typ(name = varname, typ = vartyp)
        # TODO: maybe noticing a collision would be good? or is it an upper level
        # responsibility
        if origin == VarOrigin.INPUT:
            self.input_collisions.add(varname)

    
    def get_call_typ(self, callname : str) -> Typ | None:
        '''
        get_call_typ returns the typ for a given call
        '''
        return self.call_typs.get_typ(callname)
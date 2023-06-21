from typing import Iterator, Protocol

from copy import copy

class TypeStore(Protocol):
    '''
    TypeStore is a protocol (may be seen as an interface) to something that
    just return a string with a type
    '''

    def get_type(self, name : str) -> str | None:
        pass

    def add_type(self, name : str, typename : str):
        pass

    def delete_name(self, name : str) -> bool:
        pass

    def iter_types(self) -> Iterator[ tuple[str, str] ]:
        pass

    def size(self) -> int:
        pass

class DictTypeStore():
    _types_dict : dict[str, str]

    def __init__(self, types_dict : dict[str, str] = dict()):
        self._types_dict = copy(types_dict)

    def get_type(self, name : str) -> str | None:
        return self._types_dict.get(name, None)
    
    def add_type(self, name : str, typename : str):
        self._types_dict[name] = typename
    
    def delete_name(self, name : str) -> bool:
        self._types_dict.pop(name, None)

    def iter_types(self) -> Iterator[ tuple[str, str] ]:
        for varname, typename in self._types_dict.items():
            yield (varname, typename)

    def __len__(self):
        return len(self._types_dict)
    
    def size(self) -> int:
        return len(self)



class WrapTypeStore():
    '''
    WrapTypeStore shall wrap several types getters in order
    to have more than one source for types, which should be:

    - several type getters for var names
    - a type getter for function call names
    '''
    _var_type_store : list[ TypeStore ]
    _call_type_store : TypeStore

    def __init__(
        self,
        var_types_getters : list[ TypeStore ],
        call_types_getter : TypeStore
    ):
        self._var_type_store = var_types_getters
        self._call_type_store = call_types_getter

    def get_varname_type(self, varname : str) -> str | None:
        for type_store in self._var_type_store:
            typename = type_store.get_type(varname)
            if typename is not None:
                return typename
        return None
    
    def delete_varname(self, varname : str):
        for type_store in self._var_type_store:
            type_store.delete_name(varname)

    def get_callname_type(self, call_name : str) -> str | None:
        return self._call_type_store.get_type(call_name)

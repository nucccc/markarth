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

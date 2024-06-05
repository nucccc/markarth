'''
declare_gen shall have code to generate cdef lines for types
'''

from typing import Iterator

from markarth.convert.cythonize.cy_typs import CyFloat, CyInt
from markarth.convert.cythonize.pure_funcs.typs_conv import (
    CY_BOOL_PURE,
    cy_float_str_pure,
    cy_int_str_pure
)
from markarth.convert.typs.typ_store import TypStore

# TODO: a primitive logic of type conversion would be good?

# NOTE: there is a choice to mantain two separate functions for this, as eventually
# one day for pyx there could be some advanced logic to also substitute
def typ_store_to_varnames(
    typ_store : TypStore,
    default_cy_int : CyInt,
    default_cy_float : CyFloat,
    imposed_vars : dict[str, CyInt | CyFloat]
) -> Iterator[tuple[str, str]]:
    '''
    typ_store_to_varnames converts a typstore in an iterable of the varname
    and the c type name
    '''
    for varname, typ in typ_store.iter_typs():
        imposed_typ = imposed_vars.get(varname, None)
        if imposed_typ is not None:
            # TODO: maybe some check on the type would be a good
            # idea to match the found typ and the imposed one
            # are compatible
            if type(imposed_typ) == CyFloat:
                yield (varname, cy_float_str_pure(imposed_typ))
            elif type(imposed_typ) == CyInt:
                yield (varname, cy_int_str_pure(imposed_typ))
            continue
        if typ.is_int():
            yield (varname, cy_int_str_pure(default_cy_int))
        elif typ.is_float():
            yield (varname, cy_float_str_pure(default_cy_float))
        elif typ.is_bool():
            # TODO: this handwritten 'char' shall become a const
            yield (varname, CY_BOOL_PURE)


def typ_store_to_cdeclares(
    typ_store : TypStore,
    default_cy_int : CyInt,
    default_cy_float : CyFloat,
    imposed_vars : dict[str, CyInt | CyFloat],
    cy_alias : str,
    indent_pattern : str = ''
) -> Iterator[str]:
    '''
    typ_store_to_cdeclares converts a typstore into an iterable of
    c declare lines
    '''
    for varname, cy_type in typ_store_to_varnames(
        typ_store=typ_store,
        default_cy_int=default_cy_int,
        default_cy_float=default_cy_float,
        imposed_vars=imposed_vars
    ):
        yield gen_declare_line(
            varname=varname,
            cy_alias=cy_alias,
            cy_typename=cy_type,
            indent_pattern=indent_pattern
        )


def gen_declare_line(
    varname : str,
    cy_typename : str,
    cy_alias : str,
    indent_pattern : str = ''
) -> str:
    '''
    gen_declare_line shall generate a declare line for a given varname
    '''
    return f'{indent_pattern}{varname} = {cy_alias}.declare({cy_alias}.{cy_typename})'
'''
yes someday here there is the dream of a pure python cythonizer
'''

import ast
from dataclasses import dataclass

from typing import Iterator

from markarth.convert.cythonize.cy_typs import (
    CY_BOOL,
    CyFloat,
    CyInt,
    cy_float_str,
    cy_int_str
)

from markarth.convert.typs.names_to_typs import TypStore

@dataclass
class FuncConvertData():
    '''
    should this represent the data needed by a function
    '''
    pass


def is_import_cython(imp_stat : ast.Import) -> tuple[bool, str]:
    '''
    is_import_cython receives an import ast statement in input, and
    returns a tuple with:

     - a boolean, True if cython is actually imported
     - a str
    '''
    for al in imp_stat.names:
        if al.name == 'cython':
            asname = al.asname
            alias_name = asname if asname else 'cython'
            return (True, alias_name)
    return (False, '')


def cython_imported_already(mod_ast : ast.Module) -> tuple[bool, str, int]:
    '''
    this should somehow return true if cython is already installed or not
    '''
    for stat in mod_ast.body:
        if type(stat) == ast.Import:
            check_result = is_import_cython(stat)
            if check_result[0]:
                return (check_result[0], check_result[1], stat.lineno)
    return (False, '', 0)


def typ_to_cy_ctr() -> str:
    pass


def typ_store_to_varnames(
    typ_store : TypStore,
    default_cy_int : CyInt,
    default_cy_float : CyFloat,
    imposed_vars : dict[str, CyInt | CyFloat] = dict()
) -> Iterator[tuple[str, str]]:
    for varname, typ in typ_store.iter_typs():
        imposed_typ = imposed_vars.get(varname, None)
        if imposed_typ is not None:
            # TODO: maybe some check on the type would be a good
            # idea to match the found typ and the imposed one
            # are compatible
            if type(imposed_typ) == CyFloat:
                yield (varname, cy_float_str(imposed_typ))
            elif type(imposed_typ) == CyInt:
                yield (varname, cy_int_str(imposed_typ))
        if typ.is_int():
            yield (varname, cy_int_str(default_cy_int))
        elif typ.is_float():
            yield (varname, cy_float_str(default_cy_float))
        elif typ.is_bool():
            # TODO: this handwritten 'char' shall become a const
            yield (varname, CY_BOOL)


def typ_store_to_cdeclares(
    typ_store : TypStore,
    default_cy_int : CyInt,
    default_cy_float : CyFloat,
    imposed_vars : dict[str, CyInt | CyFloat] = dict(),
    cy_alias : str = 'cython'
) -> Iterator[str]:
    for varname, cy_type in typ_store_to_varnames(
        typ_store=typ_store,
        default_cy_int=default_cy_int,
        default_cy_float=default_cy_float,
        imposed_vars=imposed_vars
    ):
        yield gen_declare_line(varname=varname, cy_alias=cy_alias, cy_typename=cy_type)




def _func_typer(codelines : list[str]):
    '''
    maybe this thing will just modify inplace the codelines and add something
    '''
    pass


def gen_declare_line(varname : str, cy_typename : str, cy_alias : str = 'cython') -> str:
    '''
    gen_declare_line shall generate a declare line for a given varname
    '''
    return f'{varname} = {cy_alias}.declare({cy_alias}.{cy_typename})'


@dataclass
class CyVarType:
    '''
    CyVarType shall just be a pair linking to each variable name a cython type
    '''
    varname : str
    cy_type : str


def store_to_cy_types(store : TypStore) -> list[CyVarType]:
    '''
    store_to_cy_types shall somehow one day convert a typstore to
    the actual pairs of varname

    DEPRECATED
    '''
    result = list()
    for varname, typ in store.iter_typs:
        cy_type = None
        if typ.is_int():
            cy_type = 'int'
        elif typ.is_float():
            cy_type = 'float'
        elif typ.is_bool():
            cy_type = 'char'
        if cy_type is not None:
            result.append(CyVarType(varname=varname, cy_type=cy_type))
    return result


def pure_cythonize(
    mod_ast : ast.Module,
    codelines : list[str],
    consts_typ_store : TypStore
) -> str:
    '''
    yep maybe this should return a portion of code with cythonized stuff, in pure
    python mode for cython 3.0
    '''
    is_cython_imported, alias, codeline_no = cython_imported_already(mod_ast)
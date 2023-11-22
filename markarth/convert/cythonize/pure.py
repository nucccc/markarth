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
from markarth.convert.cythonize.cy_options import FuncOpts, ModOpts
#from markarth.convert.collect.func_collect import Func
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
            continue
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


#class FuncToTypify:
#    '''
#    like yeah this class shall just somehow be used to add its lines to existing codelines
#    '''
#
#    def __init__(self, func_collected : Func, func_opts : FuncOpts):
#        self._c_declares_insertion_point : int = func_collected.func_ast_body[0].lineno
#        self._collected_typs : TypStore = func_collected._local_typs
#
#        self._func_opts : FuncOpts = func_opts
#
#    
#    def add_collected_lines(self, codelines : list[str], cy_alias : str = 'cython'):
#        '''
#        add_collected_lines shall take the lines generated from the collected
#        local typs and add them to the codelines
#        '''        
#        cdeclares = typ_store_to_cdeclares(
#            typ_store = self._collected_typs,
#            default_cy_int = self._func_opts.default_int_cytyp,
#            default_cy_float = self._func_opts.default_float_cytyp,
#            imposed_vars = self._func_opts.imposed_vars,
#            cy_alias = cy_alias
#        )
#        for cdeclare in cdeclares:
#            codelines.insert(self._c_declares_insertion_point, cdeclare)
#
#
#    def __ge__(self, __other_func : 'FuncToTypify') -> bool:
#        return self._c_declares_insertion_point >= __other_func._c_declares_insertion_point
#    
#
#    def __le__(self, __other_func : 'FuncToTypify') -> bool:
#        return self._c_declares_insertion_point <= __other_func._c_declares_insertion_point
#
#
#def funcs_to_tipify_lister(
#    locals_collected : dict[str, TypStore],
#    m_opts : ModOpts
#) -> list[FuncToTypify]:
#    '''
#    wouldn't it be nice to have a function that actually merges what comes
#    from options into what comes
#
#    yeah and it would be nice to have them already sorted
#    '''
#    funcs_to_tipify : list[FuncToTypify] = list()
#    # TODO: this will probably be passed as a ditionary at a point
#
#    for f_name, f_coll in locals_collected.items():
#        funcs_to_tipify.append( FuncToTypify(
#            func_collected = f_coll,
#            func_opts = m_opts.get_f_opt_or_default(f_name)
#        ) )
#
#    funcs_to_tipify.sort(reverse=True)
#
#    return funcs_to_tipify





#def pure_cythonize(
#    mod_ast : ast.Module,
#    codelines : list[str],
#    consts_typ_store : TypStore,
#    funcs_collected : dict[str, Func],
#    m_opts : ModOpts
#) -> str:
#    '''
#    yep maybe this should return a portion of code with cythonized stuff, in pure
#    python mode for cython 3.0
#    '''
    # at first i shall check if cython is imported, and in such case i consider
    # its alias
#    is_cython_imported, alias, codeline_no = cython_imported_already(mod_ast)
#
#    funcs_to_tipify = funcs_to_tipify_lister(funcs_collected, m_opts)
#
#    for func_to_tipify in funcs_to_tipify:
#        func_to_tipify.add_collected_lines(codelines)
#
#    return '\n'.join(codelines)
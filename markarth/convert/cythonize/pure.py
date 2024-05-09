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
from markarth.convert.collect.func_collect import LocalCollectionResult
from markarth.convert.collect.mod_collect import ModCollectionResult
from markarth.convert.typs.typ_store import TypStore
from markarth.convert.preprocess.code_process import indentation_pattern


DEFAULT_CY_ALIAS = 'cython'


def is_import_cython(imp_stat : ast.Import) -> tuple[bool, str]:
    '''
    is_import_cython receives an import ast statement in input, and
    returns a tuple with:

     - a boolean, True if cython is actually imported
     - a str
    '''
    for al in imp_stat.names:
        if al.name == DEFAULT_CY_ALIAS:
            asname = al.asname
            alias_name = asname if asname else DEFAULT_CY_ALIAS
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


def typ_store_to_varnames(
    typ_store : TypStore,
    default_cy_int : CyInt,
    default_cy_float : CyFloat,
    imposed_vars : dict[str, CyInt | CyFloat] = dict()
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
    cy_alias : str = DEFAULT_CY_ALIAS,
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
    cy_alias : str = DEFAULT_CY_ALIAS,
    indent_pattern : str = ''
) -> str:
    '''
    gen_declare_line shall generate a declare line for a given varname
    '''
    return f'{indent_pattern}{varname} = {cy_alias}.declare({cy_alias}.{cy_typename})'


# TODO: this class shall be used in the above methods
@dataclass
class CyVarType:
    '''
    CyVarType shall just be a pair linking to each variable name a cython type
    '''
    varname : str
    cy_type : str


def could_be_docstring(stat : ast.AST) -> bool:
    '''
    could_be_docstring returns True if an ast statement could be seen as a
    docstring
    '''
    if not type(stat) is ast.Expr:
        return False
    #if not hasattr(stat, 'value'):
    #    return False
    if not hasattr(stat.value, 'n'):
        return False
    return type(stat.value.n) is str


def cdeclares_ins_point(func_ast : ast.FunctionDef) -> int:
    '''
    cdeclares_ins_point shall return me the
    '''
    # i loop through all the statements and return the line number of the first
    # one not being a docstring
    for stat in func_ast.body:
        if not could_be_docstring(stat):
            return stat.lineno
    # by default i return the first line
    return func_ast.body[0].lineno


def sort_funcs_by_line(func_asts : dict[str, ast.FunctionDef]) -> list[str]:
    '''
    sort_funcs_by_line returns a list with the names of the functions sorted
    by the order they appear in the code
    '''
    # TODO: the performance of this code could be optimized
    func_names_by_line : dict[int, str] = {
        cdeclares_ins_point(func_ast) : func_name
        for func_name, func_ast in func_asts.items()
    }
    func_lines : list[int] = list(func_names_by_line)
    func_lines.sort()

    return [func_names_by_line[lineno] for lineno in func_lines]


def add_c_lines(
    func_ast : ast.FunctionDef,
    codelines : list[str],
    collect_result : LocalCollectionResult,
    func_opts : FuncOpts,
    cy_alias : str = DEFAULT_CY_ALIAS
) -> list[str]:
    '''
    add_c_lines modifies and returns codelines by adding the cdeclare lines
    for the types of the function's local variables
    '''
    ins_point : int = cdeclares_ins_point(func_ast)
    indent_pattern = indentation_pattern(func_ast, codelines)
    cdeclares = typ_store_to_cdeclares(
        typ_store = collect_result.local_typs,
        default_cy_int = func_opts.default_int_cytyp,
        default_cy_float = func_opts.default_float_cytyp,
        imposed_vars = func_opts.imposed_vars,
        cy_alias = cy_alias,
        indent_pattern = indent_pattern
    )
    for cdeclare in cdeclares:
        codelines.insert(ins_point, cdeclare)
    return codelines


def add_global_c_lines(
    codelines : list[str],
    gloabal_typs : TypStore,
    m_opts : ModOpts,
    cy_alias : str = DEFAULT_CY_ALIAS
) -> list[str]:
    '''
    add_global_c_lines adds at the beginning of the script the cdeclares for
    global variables
    '''
    cdeclares = typ_store_to_cdeclares(
        typ_store = gloabal_typs,
        default_cy_int = m_opts.default_int_cytyp,
        default_cy_float = m_opts.default_float_cytyp,
        imposed_vars = m_opts.imposed_consts,
        cy_alias = cy_alias,
        indent_pattern = ''
    )
    for cdeclare in cdeclares:
        codelines.insert(1, cdeclare)
    return codelines


def add_cython_import(
    codelines : list[str],
    cy_alias : str = DEFAULT_CY_ALIAS
) -> list[str]:
    '''
    add_cython_import imports at the first line a codeline importing cython
    '''
    codelines.insert(1, f'import {cy_alias}')
    return codelines



def pure_cythonize(
    mod_ast : ast.Module,
    codelines : list[str],
    mod_coll : ModCollectionResult,
    m_opts : ModOpts
) -> str:
    '''
    yep maybe this should return a portion of code with cythonized stuff, in pure
    python mode for cython 3.0
    '''
    # at first i shall check if cython is imported, and in such case i consider
    # its alias
    is_cython_imported, alias, codeline_no = cython_imported_already(mod_ast)

    if not is_cython_imported:
        # TODO: also adding an import line at the end of the function
        # shall be done
        alias = DEFAULT_CY_ALIAS

    func_asts : dict[str, ast.FunctionDef] = mod_coll.func_asts
    funcs_collected : dict[str, LocalCollectionResult] = mod_coll.func_colls
    consts_typ_store : TypStore = mod_coll.global_typs

    func_names_sorted : list[str] = sort_funcs_by_line(func_asts)

    for func_name in reversed(func_names_sorted):
        func_ast = func_asts[func_name]
        collect_result = funcs_collected[func_name]
        func_opts = m_opts.get_f_opt_or_default(func_name)
        codelines = add_c_lines(
            func_ast = func_ast,
            codelines = codelines,
            collect_result = collect_result,
            func_opts = func_opts,
            cy_alias = alias
        )

    codelines = add_global_c_lines(
        codelines = codelines,
        gloabal_typs = consts_typ_store,
        m_opts = m_opts,
        cy_alias = alias
    )

    codelines = add_cython_import(codelines = codelines, cy_alias = alias)

    return '\n'.join(codelines)
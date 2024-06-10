import ast

from dataclasses import dataclass
from typing import Callable, Iterator


from markarth.convert.collect.func_collect import LocalCollectionResult
from markarth.convert.collect.mod_collect import ModCollectionResult
from markarth.convert.cythonize._import import (
    add_cython_import,
    cython_imported_already
)
from markarth.convert.cythonize.cy_options import FuncOpts, ModOpts
from markarth.convert.cythonize.cy_typs import CyFloat, CyInt
from markarth.convert.preprocess.code_process import indentation_pattern
from markarth.convert.typs.typ_store import TypStore


DEFAULT_CY_ALIAS = 'cython'

# defining a type for a callable that generates a type declare line
typDeclGen = Callable[[str, str, str, str], str]

typStoreConvFunc = Callable[
    [TypStore, CyInt, CyFloat, dict[str, CyInt | CyFloat], str, str],
    Iterator[str]
]


@dataclass
class CythonifyLogic:
    '''
    CythonifyLogic shall be a collection to be used to characterize
    how a specific conversion shall be done
    '''
    cython_import_needed : bool
    typ_store_to_cdeclares : typStoreConvFunc


def cythonify(
    mod_ast : ast.Module,
    codelines : list[str],
    mod_coll : ModCollectionResult,
    m_opts : ModOpts,
    clogic : CythonifyLogic
) -> str:
    '''
    yep maybe this should return a portion of code with cythonized stuff, in pure
    python mode for cython 3.0
    '''
    # declaring varibles to be used during conversion
    func_asts : dict[str, ast.FunctionDef] = mod_coll.func_asts
    funcs_collected : dict[str, LocalCollectionResult] = mod_coll.func_colls
    consts_typ_store : TypStore = mod_coll.global_typs

    # at first i shall check if cython is imported, and in such case i consider
    # its alias
    alias = '' # TODO: remove this line once you're back pyx tests
    if clogic.cython_import_needed:

        is_cython_imported, alias, codeline_no = cython_imported_already(mod_ast)

        if not is_cython_imported:
            alias = DEFAULT_CY_ALIAS
    # in case the conversion logic does not require me to have a cython import,
    # the alias variable is however set to be passed as a parameter to other functions
    # TODO: decomment below once you have tests for pyx
#    else:
#        alias = ''

    # function names sorted in order of appearance, as it's more practical to modify
    # them from the last to the first, so that last functions to be modified won't have
    # codeline indexes corrupted
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
            typ_store_to_cdeclares = clogic.typ_store_to_cdeclares,
            cy_alias = alias
        )

    codelines = add_global_c_lines(
        codelines = codelines,
        gloabal_typs = consts_typ_store,
        m_opts = m_opts,
        typ_store_to_cdeclares = clogic.typ_store_to_cdeclares,
        cy_alias = alias
    )

    if clogic.cython_import_needed: 
        codelines = add_cython_import(codelines = codelines, cy_alias = alias)

    return '\n'.join(codelines)


def add_c_lines(
    func_ast : ast.FunctionDef,
    codelines : list[str],
    collect_result : LocalCollectionResult,
    func_opts : FuncOpts,
    typ_store_to_cdeclares : typStoreConvFunc,
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
    typ_store_to_cdeclares : typStoreConvFunc,
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
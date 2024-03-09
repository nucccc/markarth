'''
hereby there shall be some utilities to collect stuff out of ast module
'''

import ast

from dataclasses import dataclass
from typing import Iterable

from markarth.ast_utils import iter_func_defs
from markarth.convert.collect.func_collect import (
    func_name_from_ast,
    filter_const_candidates_at_func,
    collect_func_globals,
    collect_local_typs,
    return_typ_from_ast,
    LocalCollectionResult
)
from markarth.convert.typs.typs import Typ
from markarth.convert.typs.names_to_typs import DictTypStore, TypStore
from markarth.convert.cythonize.cy_options import ModOpts, FuncOpts, gen_default_mod_opts
from markarth.convert.collect.ast_to_typ.ast_assign import (
    assigned_typs,
    is_assign
)

@dataclass
class FuncDefData:
    func_ast: ast.FunctionDef
    name : str
    global_varnames : set[str]
    return_typ : Typ


def collect_func_def_data(mod_ast : ast.Module) -> dict[str, FuncDefData]:
    '''
    collect_func_def_data collects various data for functions definitions, it
    returns them 
    '''
    result : dict[str, FuncDefData] = dict()
    for func_ast in iter_func_defs(mod_ast):
        func_name = func_name_from_ast(func_ast)
        global_varnames = collect_func_globals(func_ast)
        return_typ = return_typ_from_ast(func_ast)
        result[func_name] = FuncDefData(
            func_ast=func_ast,
            name=func_name,
            global_varnames=global_varnames,
            return_typ=return_typ
        )
    return result



def collect_func_defs(
    mod_ast : ast.Module
) -> dict[str : ast.FunctionDef]:
    '''
    collect_func_defs returns a dictionary with the function definitions
    contained in an ast module
    '''
    f_colls : dict[str : ast.FunctionDef] = dict()
    for stat in mod_ast.body:
        if type(stat) == ast.FunctionDef:
            f_colls[ func_name_from_ast(stat) ] = stat
    return f_colls

def collect_const_candidates(mod_ast : ast.Module) -> DictTypStore:
    '''
    collect_const_candidates shall collect a dicitonary of const candidates
    '''
    modified_vars : set[str] = set()
    result : DictTypStore = DictTypStore()

    for stat in mod_ast.body:

        if is_assign(ast_expr = stat):

            assign_result = assigned_typs(ast_expr = stat)

            for varname, vartyp in assign_result.assigned_typs.iter_typs():
                if vartyp.is_primitive() and result.get_typ(varname) is None and varname not in modified_vars:
                    result.add_typ(varname, vartyp)
                else:
                    result.delete_name(varname)
                    modified_vars.add(varname)

    return result


def filter_const_candidates(
    const_candidate_names : TypStore,
    f_colls : dict[str, ast.FunctionDef]
) -> TypStore:
    '''
    filter_const_candidates takes in input a dict type store of possible
    candidate constants
    '''
    for func_ast in f_colls.values():
        const_candidate_names = filter_const_candidates_at_func(
            const_candidate_names,
            func_ast
        )
    return const_candidate_names


def collect_call_typs(func_asts : Iterable[ast.FunctionDef]) -> DictTypStore:
    '''
    yeah this shall return me the typstore representing the return types
    related to each function
    '''    
    result = DictTypStore()
    for func_ast in func_asts:
        funcname = func_name_from_ast(func_ast)
        # TODO: maybe some checks shall be done
        return_typ = return_typ_from_ast(func_ast)
        result.add_typ(funcname, return_typ)
    return result


@dataclass
class ModCollectionResult:
    '''
    ModCollectionResult stores the results of a type collection inside a module

    global_typs: the typ store containing the typs of gloabal variables
    func_colls: relates to every function name its collection result
    func_asts: relates to every function name its ast function def

    func_colls and func_asts are expected to have the same keys
    '''
    global_typs : TypStore # these are supposed to be the typs collected from the module, the consts let's say, the global variables
    func_colls : dict[str, LocalCollectionResult]
    func_asts : dict[str, ast.FunctionDef]


def mod_collect(
    mod_ast : ast.Module,
    mod_opts : ModOpts = gen_default_mod_opts()
) -> ModCollectionResult:
    '''
    mod_collect returns the collection from and ast module ast_mod, given some
    optional options mod_opts
    '''
    # okay so now what if i was to rewrite everything in straight procedural way?
    func_asts : dict[str, ast.FunctionDef] = collect_func_defs(mod_ast)

    funcs_data : dict[str, FuncDefData] = collect_func_def_data(mod_ast)

    const_candidates = collect_const_candidates(mod_ast)

    # before filtering stuff from const candidates, i shall save all the
    # keys in order to recall which ones were global variables, and thus
    # shall not be stored as global variables
    global_val_names : set[str] = {
        varname
        for varname, _  in const_candidates.iter_typs()
    }

    const_candidates = filter_const_candidates(const_candidates, func_asts)

    call_typs = collect_call_typs(func_asts.values())

    func_colls : dict[str, TypStore] = dict()
    for func_name, func_ast in func_asts.items():
        # TODO: when i remove a const candidate, then this can be taken into
        # account by the 
        
        func_opts : FuncOpts = mod_opts.get_f_opt_or_default(func_name)
        
        local_coll_res = collect_local_typs(
            func_ast = func_ast,
            global_typs = const_candidates,
            call_typs = call_typs,
            global_varnames = global_val_names,
            ignore_assignment_annotations = func_opts.actual_ignore_assignment_annotations
        )
        func_colls[func_name] = local_coll_res

    return ModCollectionResult(
        global_typs = const_candidates,
        func_colls = func_colls,
        func_asts = func_asts
    )
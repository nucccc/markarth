'''
hereby there shall be some utilities to collect stuff out of ast module
'''

import ast

from dataclasses import dataclass
from typing import Iterable

from markarth.convert.collect.func_collect import (
    func_name_from_ast,
    filter_const_candidates_at_func,
    collect_local_typs,
    return_typ_from_ast
)
from markarth.convert.typs.names_to_typs import DictTypStore, TypStore
from markarth.convert.collect.ast_to_typ.ast_to_typ import ast_val_to_typ, typ_from_constant

# TODO: tests should be written for all of this

def collect_func_defs(
    mod_ast : ast.Module
) -> dict[str : ast.FunctionDef]:
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

        match type(stat):
            case ast.Assign:
                target = stat.targets[0]
                if type(target) == ast.Tuple:
                    # in case i find any targets list which is bigger than one
                    # for now i just ignore them, and consider them as
                    # modified variables
                    for t in target.elts:
                        varname = t.id
                        result.delete_name(varname)
                        modified_vars.add(varname)
                    continue
            case ast.AnnAssign:
                target = stat.target
            case _:
                continue

        #val_typ = ast_val_to_typ(stat.value)
        varname = target.id
        if type(stat.value) == ast.Constant and result.get_typ(varname) is None and varname not in modified_vars:
            result.add_typ(varname, typ_from_constant(stat.value))
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
    global_typs : TypStore # these are supposed to be the typs collected from the module, the consts let's say, the global variables
    func_colls : dict[str, TypStore]


def mod_collect(
    mod_ast : ast.Module
) -> ModCollectionResult:
    '''
    
    '''
    # okay so now what if i was to rewrite everything in straight procedural way?
    func_asts : dict[str, ast.FunctionDef] = collect_func_defs(mod_ast)

    const_candidates = collect_const_candidates(mod_ast)

    const_candidates = filter_const_candidates(const_candidates, func_asts)

    call_typs = collect_call_typs(func_asts.values())

    func_colls : dict[str, TypStore] = dict()
    for func_name, func_ast in func_asts.items():
        local_coll_res = collect_local_typs(
            func_ast = func_ast,
            global_typs = const_candidates,
            call_typs = call_typs
        )
        func_colls[func_name] = local_coll_res.local_typs

    return ModCollectionResult(
        global_typs = const_candidates,
        func_colls = func_colls
    )
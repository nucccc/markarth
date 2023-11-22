'''
this shall be a set of utilities to collect stuff from ast
'''

import ast

from dataclasses import dataclass
from enum import Enum

from markarth.convert.collect.ast_to_typ.ast_to_typ import ast_val_to_typ, typ_from_iter
from markarth.convert.typs.names_to_typs import (
    DictTypStore,
    TypStore,
    NamesToTyps,
    VarNameSource
)
from markarth.convert.typs.typs import Typ, TypAny
from markarth.convert.typs.typs_parse import parse_type_str
from markarth.convert.typs.merge_typs import merge_typs


def func_name_from_ast(func_ast : ast.FunctionDef) -> str:
    '''
    func_name_from_ast returns the function name from its ast function_def
    '''
    return func_ast.name


def return_typ_from_ast(func_ast : ast.FunctionDef) -> Typ:
    '''
    return_typ_from_ast shall collect the type from the function's return
    '''
    if not hasattr(func_ast.returns, 'id'):
        return TypAny()
    return parse_type_str(func_ast.returns.id)


def input_typs_from_ast(func_ast : ast.FunctionDef) -> TypStore:
    '''
    input_typs_from_ast shall collect a typ store holding info regarding
    the input parameters of a function
    '''
    input_typs = DictTypStore()

    arg_types = {
            arg.arg : arg.annotation.id
            for arg in func_ast.args.args
            if hasattr(arg.annotation, 'id')
        }

    for arg_name, arg_type_str in arg_types.items():
        input_typs.add_typ(arg_name, parse_type_str(arg_type_str))

    return input_typs


def filter_const_candidates_at_func(
    const_candidate_names : TypStore,
    func_ast : ast.FunctionDef
) -> TypStore:
    '''
    filter_const_candidates modifies the TypStore provided in input by
    removing const candidates which went through a modification
    '''
    # TODO: check also for variables being set in for loops, who knows
    # walrus operators or something, also aug assign shall be kept into
    # account
    for stat in func_ast.body:
        if type(stat) == ast.Assign:
            for target in stat.targets:
                varname = target.id
                assert type(varname) == str
                const_candidate_names.delete_name(varname)
    return const_candidate_names


class CollisionEnum(Enum):
    '''
    CollisionEnum defines the possible types of collision
    '''
    NO_COLLISION = 0
    INPUT_COLLISION = 1
    GLOBAL_COLLISION = 2


def _record_vartyp(
    varname : str,
    vartyp : Typ,
    names_to_typs : NamesToTyps,
    global_varnames : set[str] = set()
) -> CollisionEnum:
    '''
    _record_vartyp shall handle a new vartyp to the existing names_to_typs
    '''
    already_typ, source = names_to_typs.get_varname_typ_and_source(varname)
    if already_typ is None:
        if varname not in global_varnames:
            names_to_typs.put_local_typ(varname, vartyp)
        return CollisionEnum.NO_COLLISION
    elif already_typ != vartyp:
        new_typ = merge_typs(already_typ, vartyp)
        names_to_typs.update_varname(varname, new_typ, source)
        match source:
            case VarNameSource.LOCAL:
                return CollisionEnum.NO_COLLISION
            case VarNameSource.INPUT:
                return CollisionEnum.INPUT_COLLISION
            case VarNameSource.GLOBAL:
                return CollisionEnum.GLOBAL_COLLISION
    else:
        return CollisionEnum.NO_COLLISION


@dataclass
class LocalCollectionResult:
    local_typs : TypStore
    colliding_input_varnames : set[str]
    colliding_global_varnames : set[str]


def collect_local_typs(
    func_ast : ast.FunctionDef,
    global_typs : TypStore = DictTypStore(),
    call_typs : TypStore = DictTypStore(),
    global_varnames : set[str] = set()
) -> LocalCollectionResult:
    '''
    collect_local_typs
    '''
    local_typs = DictTypStore()

    input_typs = input_typs_from_ast(func_ast)

    colliding_input_varnames : set[str] = set()
    colliding_global_varnames : set[str] = set()

    # TODO: maybe a copy of
    names_to_typs = NamesToTyps(
        local_typs=local_typs,
        input_typs=input_typs,
        global_typs=global_typs,
        call_typs=call_typs
    )

    for stat in func_ast.body:
        if type(stat) == ast.Assign:
            varname = stat.targets[0].id # i hypothetize the assignment to be
            vartyp = ast_val_to_typ(stat.value, names_to_typs)
            # here i colelct the vartype found
            coll = _record_vartyp(varname, vartyp, names_to_typs, global_varnames)
        elif type(stat) == ast.For:
            # TODO: here some code should be place to verify that this thing actually has a name
            varname = stat.target.id
            vartyp = typ_from_iter(stat.iter)
            # here i collect the vartype found
            coll = _record_vartyp(varname, vartyp, names_to_typs, global_varnames)
        else:
            varname = ''
            coll = CollisionEnum.NO_COLLISION
        
        match coll:
            case CollisionEnum.INPUT_COLLISION:
                colliding_input_varnames.add(varname)
            case CollisionEnum.GLOBAL_COLLISION:
                colliding_global_varnames.add(varname)

        if hasattr(stat, 'body'):
            collect_local_typs(stat.body, names_to_typs)

    return LocalCollectionResult(
        local_typs = local_typs,
        colliding_input_varnames = colliding_input_varnames,
        colliding_global_varnames = colliding_global_varnames
    )
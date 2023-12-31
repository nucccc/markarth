'''
this shall be a set of utilities to collect stuff from ast
'''

import ast

from dataclasses import dataclass
from enum import Enum

from markarth.convert.collect.ast_to_typ.ast_assign import (
    assigned_typs,
    is_assign
)
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
    

def _record_collision(
    varname : str,
    collision_enum : CollisionEnum,
    colliding_input_varnames : set[str],
    colliding_global_varnames : set[str]
) -> None:
    '''
    _record_collision evaluates the collision enum and accordingly eventually
    add it to some sets
    '''
    match collision_enum:
        case CollisionEnum.INPUT_COLLISION:
            colliding_input_varnames.add(varname)
        case CollisionEnum.GLOBAL_COLLISION:
            colliding_global_varnames.add(varname)


@dataclass
class LocalCollectionResult:
    local_typs : TypStore
    colliding_input_varnames : set[str]
    colliding_global_varnames : set[str]


def collect_from_ast_body(
    ast_body : list[ast.AST],
    names_to_typs : NamesToTyps,
    colliding_input_varnames : set[str],
    colliding_global_varnames : set[str],
    global_varnames : set[str],
    ignore_assignment_annotations : bool = False
):
    for stat in ast_body:

        if is_assign(ast_expr = stat):
            assign_result = assigned_typs(ast_expr = stat, name_typs = names_to_typs)

            # handling the annotation by selectively setting the var_name var_typ
            # generator according to ignoring the annotations
            if ignore_assignment_annotations or assign_result.annotation is None:
                # in case i'm set to ignore the annotation or no annotation
                # was retrieved in the assignemnt, the generator corresponding
                # is just going to be the varnames and the vartyps in the
                # returned typstore
                varname_vartyp_gen = (
                    (varname, vartyp)
                    for varname, vartyp
                    in assign_result.assigned_typs.iter_typs()
                )
            else:
                # in case i can use annotations and i have an annotation
                # i just scroll through the variables (there should be only one
                # actually) and relate them to the annotated typ
                varname_vartyp_gen = (
                    (varname, assign_result.annotation)
                    for varname, _
                    in assign_result.assigned_typs.iter_typs()
                )

            for varname, vartyp in varname_vartyp_gen:

                coll = _record_vartyp(varname, vartyp, names_to_typs, global_varnames)
                _record_collision(
                    varname = varname,
                    collision_enum = coll,
                    colliding_input_varnames = colliding_input_varnames,
                    colliding_global_varnames = colliding_global_varnames
                )
                
        elif type(stat) == ast.For:
            # TODO: here some code should be place to verify that this thing actually has a name
            varname = stat.target.id
            vartyp = typ_from_iter(stat.iter)
            # here i collect the vartype found
            coll = _record_vartyp(varname, vartyp, names_to_typs, global_varnames)
            _record_collision(
                varname = varname,
                collision_enum = coll,
                colliding_input_varnames = colliding_input_varnames,
                colliding_global_varnames = colliding_global_varnames
            )

        if hasattr(stat, 'body'):
            collect_from_ast_body(
                ast_body = stat.body,
                names_to_typs = names_to_typs,
                colliding_input_varnames = colliding_input_varnames,
                colliding_global_varnames = colliding_global_varnames,
                global_varnames = global_varnames
            )


def collect_local_typs(
    func_ast : ast.FunctionDef,
    global_typs : TypStore = DictTypStore(),
    call_typs : TypStore = DictTypStore(),
    global_varnames : set[str] = set(),
    ignore_assignment_annotations : bool = False
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

    collect_from_ast_body(
        ast_body = func_ast.body,
        names_to_typs = names_to_typs,
        colliding_input_varnames = colliding_input_varnames,
        colliding_global_varnames = colliding_global_varnames,
        global_varnames = global_varnames,
        ignore_assignment_annotations = ignore_assignment_annotations
    )

    return LocalCollectionResult(
        local_typs = local_typs,
        colliding_input_varnames = colliding_input_varnames,
        colliding_global_varnames = colliding_global_varnames
    )
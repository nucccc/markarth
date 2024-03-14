'''
this shall be a set of utilities to collect stuff from ast
'''

import ast

from dataclasses import dataclass
from enum import Enum

from markarth.ast_utils.ast_utils import unnest_ast_statements, unnest_ast_body
from markarth.convert.collect.ast_to_typ.ast_assign import (
    assigned_typs,
    is_assign,
    typ_store_from_target
)
from markarth.convert.collect.ast_to_typ.ast_to_typ import ast_val_to_typ, typ_from_iter
from markarth.convert.typs.typ_store import (
    DictTypStore,
    TypStore
)
from markarth.convert.collect.vartyp_tracker import (
    VarOrigin,
    VarTypEOrigin,
    VarTypTracker,
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


def collect_func_globals(func_ast : ast.FunctionDef) -> set[str]:
    '''
    collect_func_globals collects global variables in a function
    '''
    result : set[str] = set()
    for stat in unnest_ast_statements(ast_node=func_ast):
        if type(stat) == ast.Global:
            for varname in stat.names:
                result.add(varname)
    return result


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
    var_tracker : VarTypTracker,
    global_varnames : set[str] = set()
) -> CollisionEnum:
    '''
    _record_vartyp shall handle a new vartyp to the existing var_tracker
    '''
    typ_e_origin : VarTypEOrigin = var_tracker.get_vartyp_and_origin(varname) #names_to_typs.get_varname_typ_and_source(varname)
    if typ_e_origin is None:
        if varname not in global_varnames:
            var_tracker.add_local_typ(varname, vartyp)
        # TODO: else there could be an error when running the python code
        return CollisionEnum.NO_COLLISION
    already_typ = typ_e_origin.typ
    var_origin = typ_e_origin.origin

    # TODO: here there should be something to actually check if it's not global

    if varname not in global_varnames and var_origin == VarOrigin.OUTER:
        # here i should still handle this as if it was a local variable, as this
        # is a local variable
        var_tracker.add_local_typ(varname, vartyp)
        return CollisionEnum.NO_COLLISION

    elif already_typ != vartyp:
        new_typ = merge_typs(already_typ, vartyp)
        var_tracker.update_vartyp(varname, new_typ, var_origin)
        match var_origin:
            case VarOrigin.LOCAL:
                return CollisionEnum.NO_COLLISION
            case VarOrigin.INPUT:
                return CollisionEnum.INPUT_COLLISION
            case VarOrigin.OUTER:
                return CollisionEnum.GLOBAL_COLLISION
    else:
        return CollisionEnum.NO_COLLISION


def collect_from_func_ast(
    ast_body : list[ast.AST],
    var_tracker : VarTypTracker,
    global_varnames : set[str],
    ignore_assignment_annotations : bool = False
):
    '''
    collect_from_ast_body recursively checks inside a function body (which is
    a list o ast nodes) to check its types

    it is recursive in the sense that every element in a function that has
    another body inside of it "like for example" a for loop

    the function does not return anything specifically, but modifies inplace
    the var_tracker provided in input
    '''
    for stat in unnest_ast_body(ast_body):

        if is_assign(ast_expr = stat):
            assign_result = assigned_typs(ast_expr = stat, var_tracker = var_tracker)

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
                coll = _record_vartyp(varname, vartyp, var_tracker, global_varnames)

        elif type(stat) == ast.For:
            # TODO: here some code should be place to verify that this thing actually has a name
            vartyp = typ_from_iter(stat.iter)

            loop_typs = typ_store_from_target(target = stat.target, val_typ = vartyp)

            for varname, vartyp in loop_typs.iter_typs():
                # here i collect the vartype found
                coll = _record_vartyp(varname, vartyp, var_tracker, global_varnames)

@dataclass
class LocalCollectionResult:
    '''
    LocalCollectionResult is the aggregation of results to be returned
    from the collection of typs in a function

    local_typs : the typstore of typs of local variables
    colliding_input_varnames : set of function input varnames which "collided"
    colliding_global_varnames : set of global variables which "collided" (it is
        expected to be empty as such collisions should have been already handled
        before when global constants were checked)
    '''
    local_typs : TypStore
    colliding_input_varnames : set[str]
    colliding_global_varnames : set[str]


def collect_local_typs(
    func_ast : ast.FunctionDef,
    global_typs : TypStore = DictTypStore(),
    call_typs : TypStore = DictTypStore(),
    global_varnames : set[str] = set(),
    ignore_assignment_annotations : bool = False
) -> LocalCollectionResult:
    '''
    collect_local_typs collects the typs from a function
    '''

    input_typs = input_typs_from_ast(func_ast)

    colliding_input_varnames : set[str] = set()
    colliding_global_varnames : set[str] = set()

    var_tracker = VarTypTracker(
        input_typs=input_typs,
        outer_typs=global_typs,
        call_typs=call_typs
    )

    collect_from_func_ast(
        ast_body = func_ast.body,
        var_tracker = var_tracker,
        global_varnames = global_varnames,
        ignore_assignment_annotations = ignore_assignment_annotations
    )

    return LocalCollectionResult(
        local_typs = var_tracker.local_typs,
        colliding_input_varnames = colliding_input_varnames,
        colliding_global_varnames = colliding_global_varnames
    )
'''
maybe one day this could be a set of stuff to elegantly handle assignments

this shall assume that no weird stuff with the same variable coming up
and out with the same name among different targets like:

a = b = a, c, d = 3, 4, 5
'''

import ast

from dataclasses import dataclass

from markarth.convert.collect.ast_to_typ.ast_to_typ import (
    ast_val_to_typ,
    eval_op_typ
)
from markarth.convert.collect.vartyp_tracker import VarTypTracker
from markarth.convert.typs import typs
from markarth.convert.typs.typs_parse import parse_type_str
from markarth.convert.typs.typ_store import (
    TypStore,
    DictTypStore,
)

ASSIGN_TYPES = frozenset({
    ast.AnnAssign,
    ast.Assign,
    ast.AugAssign,
})


def is_assign(ast_expr : ast.AST) -> bool:
    '''
    is_assign returns True if the ast expression represents what can be
    considered an assignment
    '''
    return type(ast_expr) in ASSIGN_TYPES


@dataclass
class AssignTypRes:
    '''
    AssignTypRes represents the result of an assignment evaluation

    it will have a TypStore relating variable names to the typs being assigned to
    them, and an option annotation typ to let the above layer if an imposed
    typ was found in annotation
    '''
    assigned_typs : TypStore
    annotation : typs.Typ | None = None


def assigned_typs(
    ast_expr : ast.Assign | ast.AnnAssign | ast.AugAssign,
    var_tracker : VarTypTracker | None = None
) -> AssignTypRes:
    '''
    assigned_typs return an AssignTypRes from an assignment expression
    '''
    # obtaining the annotation I'm going to return, being none in case
    # my assignment is not being annotated
    # TODO: I need a more general function to obtain the annotation from
    # an object (not every annotation object has an "id" attribute)
    annotation = parse_type_str(ast_expr.annotation.id) if type(ast_expr) == ast.AnnAssign and hasattr(ast_expr.annotation, 'id') else None

    val_typ = ast_val_to_typ(ast_expr.value, var_tracker)

    assigned_typs : TypStore = DictTypStore()

    if type(ast_expr) == ast.AnnAssign:
        target = ast_expr.target
        _add_target_to_typ_store(
            target = target,
            target_store = assigned_typs,
            val_typ = val_typ
        )
    elif type(ast_expr) == ast.Assign:
        for target in ast_expr.targets:
            _add_target_to_typ_store(
                target = target,
                target_store = assigned_typs,
                val_typ = val_typ
            )
    elif type(ast_expr) == ast.AugAssign:
        # in such case it seems it is illegal for the target to be of
        # tuple type, it will be of type name
        target = ast_expr.target
        
        left_typ = ast_val_to_typ(target, var_tracker)
        right_typ = ast_val_to_typ(ast_expr.value, var_tracker)

        val_typ = eval_op_typ(
            op = ast_expr.op,
            left_typ = left_typ,
            right_typ = right_typ
        )

        _add_target_to_typ_store(
            target = target,
            target_store = assigned_typs,
            val_typ = val_typ
        )
    
    return AssignTypRes(
        assigned_typs = assigned_typs,
        annotation = annotation
    )


def _add_target_to_typ_store(
    target : ast.Name | ast.Tuple,
    target_store : TypStore,
    val_typ : typs.Typ
) -> TypStore:
    '''
    _add_target_to_typ_store gets varnames out of a target and inserts
    their types in a given typstore
    '''
    if type(target) == ast.Name:
        var_name = target.id
        target_store.add_typ(var_name, val_typ)
    elif type(target) == ast.Tuple:
        if val_typ.is_tuple() and len(val_typ.inner_typs) == len(target.elts):
            for elt, tup_typ in zip(target.elts, val_typ.inner_typs):
                if type(elt) is not ast.Name:
                    continue
                var_name = elt.id
                target_store.add_typ(var_name, tup_typ)
        else:
            for elt in target.elts:
                if type(elt) is not ast.Name:
                    continue
                var_name = elt.id
                target_store.add_typ(var_name, typs.TypAny())
    return target_store


def typ_store_from_target(
    target : ast.Name | ast.Tuple,
    val_typ : typs.Typ
) -> TypStore:
    '''
    typ_store_from_target gets varnames out of a target and returns a typstore
    with such variables
    '''
    assigned_typs : TypStore = DictTypStore()

    _add_target_to_typ_store(
        target = target,
        target_store = assigned_typs,
        val_typ = val_typ
    )

    return assigned_typs


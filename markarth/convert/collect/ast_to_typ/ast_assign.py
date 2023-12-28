'''
maybe one day this could be a set of stuff to elegantly handle assignments

this shall assume that no weird stuff with the same variable coming up
and out with the same name among different targets like:

a = b = a, c, d = 3, 4, 5
'''

import ast

from dataclasses import dataclass

from markarth.convert.collect.ast_to_typ.ast_to_typ import ast_val_to_typ
from markarth.convert.typs import typs
from markarth.convert.typs.merge_typs import merge_typs
from markarth.convert.typs.names_to_typs import (
    TypStore,
    DictTypStore,
    NamesToTyps
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
    name_typs : NamesToTyps | None = None
) -> AssignTypRes:
    '''
    assigned_typs return an AssignTypRes from an assignment expression
    '''
    # obtaining the annotation I'm going to return, being none in case
    # my assignment is not being annotated
    annotation = merge_typs(ast_expr.annotation.id) if type(ast_expr) == ast.AnnAssign else None

    val_typ = ast_val_to_typ(ast_expr.value, name_typs)

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
        target = ast_expr.target
        # in such case it seems it is illegal for the target to be of
        # tuple type, it will be of type name
    
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
    _add_target_to_typ_store
    '''
    if type(target) == ast.Name:
        var_name = target.id
        target_store.add_typ(var_name, val_typ)
    elif type(target) == ast.Tuple:
        for elt in target.elts:
            var_name = elt.id
            # TODO: in case of a tuple at the moment i just put an any as the
            # typ, in the future a check on eventual container typs maybe shall
            # be done
            target_store.add_typ(var_name, typs.TypAny())
    return target_store
'''
maybe one day this could be a set of stuff to elegantly handle assignments
'''

import ast

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
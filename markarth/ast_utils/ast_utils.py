'''
a generic collection of utilities to work with ast classes
'''

import ast

from typing import Iterable


def unnest_ast_statements(ast_node : ast.AST) -> Iterable[ast.AST]:
    '''
    unnest_ast_statements shall yield all statements within an
    ast_node's body, recursively unnesting eventual internal bodies
    of statements

    in practice this is allows to iterate sequentially through ast
    statements without worrying about the nested bodies, as they
    are going to be unnested by this function
    '''
    if hasattr(ast_node, 'body'):        
        for child in ast_node.body:
            yield child
            if hasattr(child, 'body'):
                for gran_child in unnest_ast_statements(child):
                    yield gran_child


def unnest_ast_body(ast_body : list[ast.AST]) -> Iterable[ast.AST]:
    for stat in ast_body:
        yield stat
        if hasattr(stat, 'body'):
            for child_stat in unnest_ast_body(stat.body):
                yield child_stat


def iter_func_defs(mod_ast : ast.Module) -> Iterable[ast.FunctionDef]:
    '''
    iter_func_defs iterates through all function defs in an ast module
    '''
    for stat in mod_ast.body:
        if type(stat) == ast.FunctionDef:
            yield stat
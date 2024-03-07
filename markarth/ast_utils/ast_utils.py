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
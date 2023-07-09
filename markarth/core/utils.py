'''
this shall contain utilities for splitting code into codelines at the moment
'''

import ast

class ASTWithoutBody(Exception):
    'Raised when the AST provided does not have a body'
    pass

class InvalidIndentation(Exception):
    'Raised when the indentation level is incorrect'
    pass

def to_codelines(code : str) -> list[str]:
    return code.split('\n')

def to_ast_codelines(code : str) -> list[str]:
    return [''] + to_codelines(code=code)

def process_code(code : str) -> tuple[ast.AST, list[str]]:
    '''
    process_code takes in input a string and returns a tuple 
    '''
    return (ast.parse(code), to_ast_codelines(code))

def process_func_code(code : str) -> tuple[ast.AST, list[str]]:
    '''
    process_func_code
    '''
    ast_code, codelines = process_code(code)
    func_ast = ast_code.body[0]
    return (func_ast, codelines)

def indentation_pattern(
        ast_with_body : ast.AST,
        codelines : list[str],
        indent_level : int = 1
    ) -> str:
    '''
    indentation_pattern returns the type of string that may represent
    the indentation
    '''
    if not hasattr(ast_with_body, 'body'):
        raise ASTWithoutBody
    first_expr = ast_with_body.body[0]
    codeline = codelines[first_expr.lineno]
    indentation = codeline[:first_expr.col_offset]
    if len(indentation) % indent_level != 0:
        raise InvalidIndentation
    n_indent_chars = int(len(indentation) / indent_level)
    return indentation[:n_indent_chars]

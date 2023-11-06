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
    '''
    to_ast_codelines takes in input a code string and 
    '''
    return [''] + to_codelines(code=code)

def process_code(code : str) -> tuple[ast.Module, list[str]]:
    '''
    process_code takes in input a string and returns a tuple 
    '''
    return (ast.parse(code), to_ast_codelines(code))

def process_func_code(code : str) -> tuple[ast.FunctionDef, list[str]]:
    '''
    process_func_code
    '''
    ast_code, codelines = process_code(code)
    func_ast = ast_code.body[0]
    return (func_ast, codelines)

def process_file(filepath : str) -> tuple[ast.Module, list[str]]:
    '''
    process_file opens a python code file, returns its code being processed
    '''
    with open(filepath, 'r') as f:
        return process_code(f.read())
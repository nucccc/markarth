'''
this shall contain utilities for splitting code into codelines at the moment
'''

import ast

def toCodelines(code : str) -> list[str]:
    return code.split('\n')

def toASTCodelines(code : str) -> list[str]:
    return [''] + toCodelines(code=code)

def process_code(code : str) -> tuple[ast.AST, list[str]]:
    '''
    process_code takes in input a string and returns a tuple 
    '''
    return (ast.parse(code), toASTCodelines(code))
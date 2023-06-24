'''
now in this file here some usage functions shall be introduced
'''

import ast

from .core.utils import process_code
from .core.funconv import FuncConverter

class InvalidCode(Exception):
    'Raised when the code provided is invalid'
    pass

def convert_func(func_code : str) -> str:
    '''
    convert_func converts the code of a function

    :param str func_code:: the code to be converted
    :return: the code converted to cython
    :rtype: str
    :raises InvalidCode: if the code provided doesn't just contain a single
        function definition
    '''

    ast_nodes, codelines = process_code(func_code)
    
    if len(ast_nodes.body) != 1:
        raise InvalidCode
    
    func_ast = ast_nodes.body[0]
    
    if type(func_ast) != ast.FunctionDef:
        raise InvalidCode
    
    fc = FuncConverter(func_ast, codelines)
    cy_func_code = fc.convert()
    return cy_func_code
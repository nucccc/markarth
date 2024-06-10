'''
_import shall be a library with functions to check if cython is actually
imported, and eventually import it
'''

import ast


CYTHON_MODULE_NAME = 'cython'


def is_import_cython(imp_stat : ast.Import) -> tuple[bool, str]:
    '''
    is_import_cython receives an import ast statement in input, and
    returns a tuple with:

     - a boolean, True if cython is actually imported
     - a str
    '''
    for al in imp_stat.names:
        if al.name == CYTHON_MODULE_NAME:
            asname = al.asname
            alias_name = asname if asname else CYTHON_MODULE_NAME
            return (True, alias_name)
    return (False, '')


def cython_imported_already(mod_ast : ast.Module) -> tuple[bool, str, int]:
    '''
    this should somehow return true if cython is already installed or not
    '''
    for stat in mod_ast.body:
        if type(stat) == ast.Import:
            check_result = is_import_cython(stat)
            if check_result[0]:
                return (check_result[0], check_result[1], stat.lineno)
    return (False, '', 0)


def gen_import_line(cy_alias : str | None = None) -> str:
    '''
    gen_import_line generates an import cython line
    '''
    if cy_alias is None or cy_alias == CYTHON_MODULE_NAME:
        return f'import {CYTHON_MODULE_NAME}'
    return f'import {CYTHON_MODULE_NAME} as {cy_alias}'

def add_cython_import(
    codelines : list[str],
    cy_alias : str | None
) -> list[str]:
    '''
    add_cython_import imports at the first line a codeline importing cython
    '''
    imp_line = gen_import_line(cy_alias)
    codelines.insert(1, imp_line)
    return codelines
'''
yes someday here there is the dream of a pure python cythonizer
'''

import ast
from dataclasses import dataclass

from markarth.convert.typs.names_to_typs import TypStore

@dataclass
class FuncConvertData():
    '''
    should this represent the data needed by a function
    '''
    pass


def is_import_cython(imp_stat : ast.Import) -> tuple[bool, str]:
    '''
    is_import_cython receives an import ast statement in input, and
    returns a tuple with:

     - a boolean, True if cython is actually imported
     - a str
    '''
    for al in imp_stat.names:
        if al.name == 'cython':
            asname = al.asname
            alias_name = asname if asname else 'cython'
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


def pure_cythonize(
    mod_ast : ast.Module,
    codelines : list[str],
    consts_typ_store : TypStore
) -> str:
    '''
    yep maybe this should return a portion of code with cythonized stuff, in pure
    python mode for cython 3.0
    '''
    is_cython_imported, alias, codeline_no = cython_imported_already(mod_ast)
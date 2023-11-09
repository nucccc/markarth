import pytest

from markarth.convert.cythonize.pure import cython_imported_already

def is_cython_imported(mod1, mod2):
    mod_ast, _ = mod1

    is_cython_imported, alias, line_no = cython_imported_already(mod_ast)
    assert not is_cython_imported

    mod_ast, _ = mod2

    is_cython_imported, alias, line_no = cython_imported_already(mod_ast)
    assert is_cython_imported
    assert alias == 'cython'
    assert line_no == 2
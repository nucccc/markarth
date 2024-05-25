import pytest

import ast

from markarth.convert.typs.typs import PrimitiveCod, TypPrimitive
from markarth.convert.typs.typ_store import DictTypStore
from markarth.convert.collect.mod_collect import (
    collect_func_defs
)
from markarth.convert.cythonize.cy_typs import CyFloat, CyInt
from markarth.convert.cythonize.pure import (
    cython_imported_already,
    typ_store_to_varnames,
    typ_store_to_cdeclares,
    gen_declare_line,
    could_be_docstring,
    cdeclares_ins_point,
    sort_funcs_by_line
)

def test_is_cython_imported(code1, mod2):
    mod_ast, _ = code1

    is_cython_imported, alias, line_no = cython_imported_already(mod_ast)
    assert not is_cython_imported

    mod_ast, _ = mod2

    is_cython_imported, alias, line_no = cython_imported_already(mod_ast)
    assert is_cython_imported
    assert alias == 'cython'
    assert line_no == 2


def test_typ_store_to_varnames():
    typ_store = DictTypStore({
        'a' : TypPrimitive(PrimitiveCod.INT),
        'b' : TypPrimitive(PrimitiveCod.FLOAT),
        'c' : TypPrimitive(PrimitiveCod.BOOL),
        'd' : TypPrimitive(PrimitiveCod.STR)
    })

    tuples = set(typ_store_to_varnames(
        typ_store = typ_store,
        default_cy_int=CyInt.INT,
        default_cy_float=CyFloat.FLOAT
    ))

    expected_tuples = {
        ('a', 'int'),
        ('b', 'float'),
        ('c', 'char'),
    }

    assert tuples == expected_tuples


def test_typ_store_to_varnames_imposed_vars():
    typ_store = DictTypStore({
        'a' : TypPrimitive(PrimitiveCod.INT),
        'b' : TypPrimitive(PrimitiveCod.FLOAT),
        'c' : TypPrimitive(PrimitiveCod.BOOL),
        'd' : TypPrimitive(PrimitiveCod.STR)
    })

    tuples = set(typ_store_to_varnames(
        typ_store = typ_store,
        default_cy_int=CyInt.INT,
        default_cy_float=CyFloat.FLOAT,
        imposed_vars={'a':CyInt.LONG, 'b':CyFloat.DOUBLE}
    ))

    expected_tuples = {
        ('a', 'long'),
        ('b', 'double'),
        ('c', 'char'),
    }

    assert tuples == expected_tuples


def test_typ_store_to_cdeclares():
    typ_store = DictTypStore({
        'a' : TypPrimitive(PrimitiveCod.INT),
        'b' : TypPrimitive(PrimitiveCod.FLOAT),
        'c' : TypPrimitive(PrimitiveCod.BOOL),
        'd' : TypPrimitive(PrimitiveCod.STR)
    })

    lines =  set(
        typ_store_to_cdeclares(
            typ_store = typ_store,
            default_cy_int=CyInt.INT,
            default_cy_float=CyFloat.FLOAT
        )
    )

    expected_lines = {
        'a = cython.declare(cython.int)',
        'b = cython.declare(cython.float)',
        'c = cython.declare(cython.char)'
    }

    assert lines == expected_lines


def test_typ_store_to_cdeclares_imposed_vars():
    typ_store = DictTypStore({
        'a' : TypPrimitive(PrimitiveCod.INT),
        'b' : TypPrimitive(PrimitiveCod.FLOAT),
        'c' : TypPrimitive(PrimitiveCod.BOOL),
        'd' : TypPrimitive(PrimitiveCod.STR)
    })

    lines =  set(
        typ_store_to_cdeclares(
            typ_store = typ_store,
            default_cy_int=CyInt.INT,
            default_cy_float=CyFloat.FLOAT,
            imposed_vars={'a':CyInt.LONG}
        )
    )

    expected_lines = {
        'a = cython.declare(cython.long)',
        'b = cython.declare(cython.float)',
        'c = cython.declare(cython.char)'
    }

    assert lines == expected_lines


def test_gen_declare_line():
    assert gen_declare_line(
        varname='vvv',
        cy_alias='cy',
        cy_typename='long'
    ) == 'vvv = cy.declare(cy.long)'

    assert gen_declare_line(
        varname='vv',
        cy_typename='float'
    ) == 'vv = cython.declare(cython.float)'


def test_could_be_docstring():
    m = ast.parse('a = 3')
    assert not could_be_docstring(m.body[0])

    m = ast.parse('3')
    assert not could_be_docstring(m.body[0])

    m = ast.parse('[i for i in range(4)]')
    assert not could_be_docstring(m.body[0])

    m = ast.parse('len([i for i in range(4)])')
    assert not could_be_docstring(m.body[0])

    m = ast.parse('"""beh"""')
    assert could_be_docstring(m.body[0])

    m = ast.parse('"string"')
    assert could_be_docstring(m.body[0])


def test_cdeclares_ins_point(mod3, mod10):
    mod_ast, _ = mod3

    func_asts = collect_func_defs(mod_ast)

    assert cdeclares_ins_point(func_asts['f1']) == 5
    assert cdeclares_ins_point(func_asts['f2']) == 11
    assert cdeclares_ins_point(func_asts['f3']) == 15

    # then a test with a code module modified to have some docstrings
    mod_ast, _ = mod10

    func_asts = collect_func_defs(mod_ast)

    assert cdeclares_ins_point(func_asts['f1']) == 8
    assert cdeclares_ins_point(func_asts['f2']) == 15
    assert cdeclares_ins_point(func_asts['f3']) == 19

    # testing the case of a docstring as the only element of a code section
    cod = """def func():\n\t'''a docstring'''"""
    mod_ast = ast.parse(cod)
    func_asts = collect_func_defs(mod_ast)

    assert cdeclares_ins_point(func_asts['func']) == 2



def test_sort_funcs_by_line(mod3):
    mod_ast, _ = mod3

    func_asts = collect_func_defs(mod_ast)
    
    funcs_names_ordered = sort_funcs_by_line(func_asts)
    assert len(funcs_names_ordered) == 3
    assert funcs_names_ordered[0] == 'f1'
    assert funcs_names_ordered[1] == 'f2'
    assert funcs_names_ordered[2] == 'f3'


def test_pure(mod3):
    pass
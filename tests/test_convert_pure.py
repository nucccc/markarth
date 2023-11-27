import pytest

from markarth.convert.convert_pure import convert_code

from markarth.convert.collect.mod_collect import collect_func_defs
from markarth.convert.preprocess.code_process import (
    func_codelines,
    process_code
)

def test_convert_pure3(code_mod3):
    converted_code = convert_code(code_mod3)

    converted_ast , converted_codelines = process_code(converted_code)

    func_asts = collect_func_defs(converted_ast)

    f2_codelines = func_codelines(
        func_ast = func_asts['f2'],
        codelines = converted_codelines
    )

    assert '    res = cython.declare(cython.int)' in f2_codelines

    f3_codelines = func_codelines(
        func_ast = func_asts['f3'],
        codelines = converted_codelines
    )

    assert '    res = cython.declare(cython.int)' in f3_codelines
    assert '    c = cython.declare(cython.int)' in f3_codelines


def test_convert_pure4(code_mod4):
    converted_code = convert_code(code_mod4)

    converted_ast , converted_codelines = process_code(converted_code)

    func_asts = collect_func_defs(converted_ast)

    stuff_codelines = func_codelines(
        func_ast = func_asts['stuff'],
        codelines = converted_codelines
    )

    assert '    h = cython.declare(cython.float)' in stuff_codelines
    assert '    p = cython.declare(cython.int)' in stuff_codelines
    assert '    i = cython.declare(cython.int)' in stuff_codelines
    assert '    onono = cython.declare(cython.float)' in stuff_codelines
    assert '    m = cython.declare(cython.int)' in stuff_codelines
    assert '    sum = cython.declare(cython.int)' in stuff_codelines
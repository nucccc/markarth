'''
some code should be written to actually run tests on the code process
'''

from markarth.convert.preprocess.code_process import func_codelines
from markarth.convert.collect.mod_collect import collect_func_defs


def test_func_codelines(mod3):
    mod_ast, codelines = mod3

    funcs_asts = collect_func_defs(mod_ast)

    f1_codelines = func_codelines(
        func_ast = funcs_asts['f1'],
        codelines = codelines
    )

    assert len(f1_codelines) == 3
    assert f1_codelines == [
        '    res = b * g',
        '    b = res',
        '    return res'
    ]

    f2_codelines = func_codelines(
        func_ast = funcs_asts['f2'],
        codelines = codelines
    )

    assert len(f2_codelines) == 2
    assert f2_codelines == [
        '    res = 7 * a',
        '    return res'
    ]

    f3_codelines = func_codelines(
        func_ast = funcs_asts['f3'],
        codelines = codelines
    )

    assert len(f3_codelines) == 3
    assert f3_codelines == [
        '    c = f2()',
        '    res = c * g',
        '    return res'
    ]
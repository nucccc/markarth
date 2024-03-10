import pytest

import ast

from markarth.ast_utils import unnest_ast_statements, unnest_ast_body, iter_func_defs

def test_unnest_ast_statements(mod4):
    ast_mod, _ = mod4

    statements = list(unnest_ast_statements(ast_node = ast_mod))

    assert statements[0] is ast_mod.body[0]
    assert statements[1] is ast_mod.body[0].body[0]
    assert statements[2] is ast_mod.body[0].body[1]
    assert statements[3] is ast_mod.body[0].body[2]
    assert statements[4] is ast_mod.body[0].body[3]
    assert statements[5] is ast_mod.body[0].body[3].body[0]
    assert statements[6] is ast_mod.body[0].body[3].body[1]
    assert statements[7] is ast_mod.body[0].body[3].body[2]
    assert statements[8] is ast_mod.body[0].body[3].body[3]
    assert statements[9] is ast_mod.body[0].body[4]


def test_unnest_ast_body(mod4):
    ast_mod, _ = mod4

    statements = list(unnest_ast_body(ast_body = ast_mod.body))

    assert statements[0] is ast_mod.body[0]
    assert statements[1] is ast_mod.body[0].body[0]
    assert statements[2] is ast_mod.body[0].body[1]
    assert statements[3] is ast_mod.body[0].body[2]
    assert statements[4] is ast_mod.body[0].body[3]
    assert statements[5] is ast_mod.body[0].body[3].body[0]
    assert statements[6] is ast_mod.body[0].body[3].body[1]
    assert statements[7] is ast_mod.body[0].body[3].body[2]
    assert statements[8] is ast_mod.body[0].body[3].body[3]
    assert statements[9] is ast_mod.body[0].body[4]


def test_iter_func_defs(mod3):

    mod_ast, _ = mod3

    func_defs = list(iter_func_defs(mod_ast))

    assert len(func_defs) == 3

    assert func_defs[0].name == 'f1'
    assert type(func_defs[0]) is ast.FunctionDef
    assert func_defs[1].name == 'f2'
    assert type(func_defs[1]) is ast.FunctionDef
    assert func_defs[2].name == 'f3'
    assert type(func_defs[2]) is ast.FunctionDef
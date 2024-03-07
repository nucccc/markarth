import pytest

from markarth.ast_utils import unnest_ast_statements

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
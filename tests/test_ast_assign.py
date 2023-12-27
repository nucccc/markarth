import pytest

from markarth.convert.collect.ast_to_typ.ast_assign import is_assign

def test_is_assignment(mod5, mod6):
    ast_mod, _ = mod5

    for expr in ast_mod.body:
        assert is_assign(expr)

    ast_mod, _ = mod6

    for expr in ast_mod.body:
        assert not is_assign(expr)
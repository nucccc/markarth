import pytest

import ast

from markarth.convert.collect import mod_collector

def test_collector1(code1 : tuple[ast.AST, list[str]]):
    mod_ast, codelines = code1
    
    mc = mod_collector.ModCollector(mod_ast=mod_ast, codelines=codelines)

    func_defs, assignments = mc._collect_funcdefs_and_assignments()

    assert len(func_defs) == 3
    assert 'func0' in func_defs.keys()
    assert 'func1' in func_defs.keys()
    assert 'func2' in func_defs.keys()

    assert len(assignments) == 4

    expected_assignment_varnames : set[str] = {
        'A', 'B', 'C', 'D'
    }

    found_assignment_varnames : set[str] = set()

    for assignment in assignments:
        match type(assignment):
            case ast.Assign:
                for target in assignment.targets:
                    found_assignment_varnames.add(target.id)
            case ast.AnnAssign:
                found_assignment_varnames.add(assignment.target.id)
    
    assert expected_assignment_varnames == found_assignment_varnames

def test_const_assignments1(assignments1):
    const_candidates = mod_collector.const_candidates_from_assignments(assignments=assignments1)

    assert len(const_candidates) == 2

    assert 'a' in const_candidates
    assert 'b' not in const_candidates
    assert 'c' not in const_candidates
    assert 'd' not in const_candidates
    assert 'e' in const_candidates
    
    
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

    print(assignments)
    for ass in assignments:
        print(ass.value)

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
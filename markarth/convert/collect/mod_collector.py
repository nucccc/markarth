import ast
from typing import Iterable

from markarth.convert.collect.func_collector import assignments_from_body, Func
from markarth.convert.typs.typs_parse import parse_type_str
from markarth.convert.typs.names_to_typs import DictTypStore
from markarth.convert.collect.ast_to_typ.ast_to_typ import ast_val_to_typ, typ_from_constant


def const_candidates_from_assignments(assignments : list[ast.Assign]) -> DictTypStore:
    '''
    const_candidates_from_assignments takes some assignments and checks if
    anything comes out as a target only once, in such case that is a candidate
    for being a constant
    '''
    modified_vars : set[str] = set()
    result : DictTypStore = DictTypStore()

    for assign in assignments:
        # i consider a const candidate only if it is from a single
        # assignment for now
        if len(assign.targets) == 1:
            val_typ = ast_val_to_typ(assign.value)

            target = assign.targets[0]
            varname = target.id
            if type(assign.value) == ast.Constant and result.get_typ(varname) is not None and varname not in modified_vars:
                result.add_typ(varname, typ_from_constant(assign.value))
            else:
                result.delete_name(varname)
                modified_vars.add(varname)
        # if the assignments are the result of a multiple assignment, then
        # for simplicity i do not consider as const candidates
        else:
            for target in assign.targets:
                varname = target.id
                result.delete_name(varname)
                modified_vars.add(varname)

    return result


class ModCollector:
    '''
    ModCollector shall collect stuff from an ast.Module object
    '''

    def __init__(self, mod_ast : ast.Module, codelines : list[str]):
        self._mod_ast : ast.Module =  mod_ast
        self._codelines : list[str] = codelines

        func_defs, assignments = self._collect_funcdefs_and_assignments()

        self._func_defs : dict[str:Func] = func_defs

        #setting the global typs, actually conceived as consts (they shall be
        # filtered in order to remove variables which vary at the moment)
        self.global_typs : DictTypStore = const_candidates_from_assignments(assignments)
        self.global_typs = self.filter_const_candidates(self.global_typs)

        # setting the call typs for the module to be executed
        self.call_typs : DictTypStore = self._collect_call_typs(self._func_defs.values())
        

    def collect(self) -> None:
        '''
        i would like collect to just not collect the single statements, but also
        recursively the function definitions' types
        '''
        pass


    def _collect_funcdefs_and_assignments(self) -> tuple[ dict[str:Func], list[ast.Assign] ]:
        '''
        _collect_funcdefs_and_assignments returns a tuple with:
         - a dictionary relating to function names the func obhect related to such def
         - a list of ast assignments
        '''
        func_defs : dict[str:Func] = dict()
        assignments : list[ast.Assign] = list()
        for stat in self._mod_ast.body:
            if type(stat) == ast.FunctionDef:
                func = Func(stat, self._codelines)
                func_defs[func.name] = func
            elif type(stat) == ast.Assign:
                assignments.append(stat)
        return (func_defs, assignments)


    def _collect_const_candidates_names(self) -> set[str]:
        '''
        _collect_const_candidates_names shall return a set of variable names
        '''
        return const_candidates_from_assignments(self._mod_assignments)
    

    def filter_const_candidates(self, const_candidate_names : DictTypStore) -> DictTypStore:
        '''
        filter_const_candidates takes in input a dict type store of possible
        candidate constants
        '''
        for func in self._func_defs.values():
            const_candidate_names = func.filter_const_candidates(const_candidate_names)
        return const_candidate_names

    
    def _collect_call_typs(self, funcs : Iterable[Func]) -> DictTypStore:
        result = DictTypStore()
        for func in funcs:
            funcname = func.name
            return_typ = func.return_typ
            result.add_typ(funcname, return_typ)
        return result
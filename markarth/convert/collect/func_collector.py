import ast

from markarth.convert.typs.names_to_typs import DictTypStore, TypStore, NamesToTyps
from markarth.convert.typs.typs_parse import parse_type_str
from markarth.convert.typs.typs import Typ, TypNone


def assignments_from_body(
        func_ast_body : list[ast.AST],
        result : list[ast.Assign] | None = None,
        recursive : bool = True
    ) -> list[ast.Assign]:
    '''
    assignments_from_body shall collect all assignments out of a function body
    '''
    if result is None:
        result : list[ast.Assign] = list()
    for ast_node in func_ast_body:
        if type(ast_node) == ast.Assign:
            result.append(ast_node)
        elif hasattr(ast_node, 'body') and recursive:
            assignments_from_body(ast_node.body, result)
    return result


class Func:
    '''
    func shall somehow represent a function, which will need to be parsed
    and so on
    '''

    def __init__(self, func_ast : ast.FunctionDef, codelines : list[str]):
        self._func_ast : ast.FunctionDef = func_ast
        self._codelines : list[str] = codelines

        # _outer_global_store shall at certain point be assigned with a
        # typestore from the module above, containing types related to const
        # variable names
        self._outer_global_store : TypStore | None = None
        # _outer_call_store shall at certain point be assigned with a
        # typestore from the module above, containing types related to other
        # functions in the module
        self._outer_call_store : TypStore | None = None


    @property
    def func_ast_body(self) -> list[ast.AST]:
        return self._func_ast.body


    @property
    def name(self) -> str:
        return self._func_ast.name
    

    def set_global_store(self, global_store : TypStore) -> None:
        self._outer_global_store = global_store

    
    def set_call_store(self, call_store : TypStore) -> None:
        self._outer_call_store = call_store


    def _collect_assignments(self) -> list[ast.AST]:
        self._assignments = assignments_from_body(self._func_ast.body)


    def filter_const_candidates(
            self,
            const_candidate_names : TypStore
        ) -> TypStore:
        '''
        filter_const_candidates modifies the TypStore provided in input by
        removing const candidates which went through a modification
        '''
        # TODO: check also for variables being set in for loops
        for assign in self._assignments:
            for target in assign.targets:
                varname = target.id
                assert type(varname) == str
                const_candidate_names.delete_name(varname)
        return const_candidate_names


    def _collect_input_typs(self) -> TypStore:
        input_types = DictTypStore()

        arg_types = {
            arg.arg : arg.annotation.id
            for arg in self.func_ast.args.args
            if hasattr(arg.annotation, 'id')
        }

        for arg_name, arg_type_str in arg_types:
            input_types.add_typ(arg_name, parse_type_str(arg_type_str))

        return input_types
    

    @property
    def return_typ(self) -> Typ:
        '''
        _collect_return_typ shall collect the type from the function's return
        '''
        if not hasattr(self.func_ast.returns, 'id'):
            return TypNone
        return parse_type_str(self.func_ast.returns.id)


    def _collect_typs(self) -> TypStore:
        pass
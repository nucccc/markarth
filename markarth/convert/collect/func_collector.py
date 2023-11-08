import ast

from enum import Enum

from dataclasses import dataclass

from markarth.convert.collect.ast_to_typ.ast_to_typ import ast_val_to_typ, typ_from_iter
from markarth.convert.typs.names_to_typs import DictTypStore, TypStore, NamesToTyps, VarNameSource
from markarth.convert.typs.typs_parse import parse_type_str
from markarth.convert.typs.typs import Typ, TypAny
from markarth.convert.typs.merge_typs import merge_typs


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


class CollisionEnum(Enum):
    '''
    CollisionEnum defines the possible types of collision
    '''
    NO_COLLISION = 0
    INPUT_COLLISION = 1
    GLOBAL_COLLISION = 2


def _record_vartyp(
    varname : str,
    vartyp : Typ,
    names_to_typs : NamesToTyps
) -> CollisionEnum:
    '''
    _record_vartyp shall handle a new vartyp to the existing names_to_typs
    '''
    already_typ, source = names_to_typs.get_varname_typ_and_source(varname)
    if already_typ is None:
        names_to_typs.put_local_typ(varname, vartyp)
        return CollisionEnum.NO_COLLISION
    elif already_typ != vartyp:
        new_typ = merge_typs(already_typ, vartyp)
        names_to_typs.update_varname_typ(varname, new_typ)
        match source:
            case VarNameSource.LOCAL:
                return CollisionEnum.NO_COLLISION
            case VarNameSource.INPUT:
                return CollisionEnum.INPUT_COLLISION
            case VarNameSource.GLOBAL:
                return CollisionEnum.GLOBAL_COLLISION


@dataclass
class CollectionResult:
    collected_typs : TypStore
    colliding_input_typs : set[str]
    colliding_global_typs : set[str]


def _collect_typs(
    statements : list[ast.AST],
    names_to_typs : NamesToTyps
) -> CollectionResult:
    '''
    so maybe this shall scan the actual code and then return
    the types that were collected (which at a certain point
    i would like to type)
    '''
    result : CollectionResult = CollectionResult(
        collected_typs = names_to_typs.local_typs,
        colliding_input_typs = set(),
        colliding_global_typs = set()
    )
    for stat in statements:
        if type(stat) == ast.Assign:
            varname = stat.targets[0].id # i hypothetize the assignment to be
            vartyp = ast_val_to_typ(stat.value, names_to_typs)
            # here i colelct the vartype found
            coll = _record_vartyp(varname, vartyp, names_to_typs)
        elif type(stat) == ast.For:
            # TODO: here some code should be place to verify that this thing actually has a name
            varname = stat.target.id
            vartyp = typ_from_iter(stat.iter)
            # here i collect the vartype found
            coll = _record_vartyp(varname, vartyp, names_to_typs)
        else:
            varname = ''
            coll = CollisionEnum.NO_COLLISION
        
        match coll:
            case CollisionEnum.INPUT_COLLISION:
                result.colliding_input_typs.add(varname)
            case CollisionEnum.GLOBAL_COLLISION:
                result.colliding_global_typs.add(varname)

        if hasattr(stat, 'body'):
            _collect_typs(stat.body, names_to_typs)

    return result


class Func:
    '''
    func shall somehow represent a function, which will need to be parsed
    and so on
    '''

    def __init__(self, func_ast : ast.FunctionDef, codelines : list[str]):
        self._func_ast : ast.FunctionDef = func_ast
        self._codelines : list[str] = codelines

        self._local_typs : TypStore | None = None

        self._collect_assignments()


    @property
    def func_ast_body(self) -> list[ast.AST]:
        return self._func_ast.body
    

    @property
    def collection_happened(self) -> bool:
        return self._local_typs is not None


    @property
    def name(self) -> str:
        return self._func_ast.name


    def _collect_assignments(self) -> list[ast.AST]:
        '''
        this is actually useful to obtain some assignments from a body
        and reuse to filter const candidates... in reality at certain point
        this should take into account also walrus operators and thus this
        function shall be discarded and deprecated
        '''
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
        '''
        _collect_input_typs shall collect a typ store holding info regarding
        the input parameters of a function
        '''
        input_types = DictTypStore()

        arg_types = {
            arg.arg : arg.annotation.id
            for arg in self._func_ast.args.args
            if hasattr(arg.annotation, 'id')
        }

        for arg_name, arg_type_str in arg_types.items():
            input_types.add_typ(arg_name, parse_type_str(arg_type_str))

        return input_types
    

    @property
    def return_typ(self) -> Typ:
        '''
        _collect_return_typ shall collect the type from the function's return
        '''
        if not hasattr(self._func_ast.returns, 'id'):
            return TypAny()
        return parse_type_str(self._func_ast.returns.id)
    

    def collect_typs(
        self,
        global_typs : TypStore = DictTypStore(),
        call_typs : TypStore = DictTypStore(),
    ) -> TypStore:
        '''
        TODO: READAPT THIS

        collect_types shall run (eventually recurvively) taking bodies and
        collecting types from statements
        '''
        input_typs = self._collect_input_typs()
        names_to_typs = NamesToTyps(
            local_typs = DictTypStore(),
            input_typs = input_typs,
            global_typs = global_typs,
            call_typs = call_typs
        )

        # maybe here in the middle some state variables shall be modified
        collection : CollectionResult = _collect_typs(
            statements=self._func_ast_body,
            names_to_typs=names_to_typs
        )

        self._local_typs = collection.collected_typs



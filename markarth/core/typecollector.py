import ast

from markarth.core.typestore import DictTypeStore, WrapTypeStore

VALID_CTYPES = {
    'int',
    'float'
}

def is_valid_ctype(ctype : str) -> bool:
    return ctype in VALID_CTYPES

def get_value_type(
        val : ast.AST,
        types_getter : WrapTypeStore | None = None
    ) -> str | None:
    '''
    get_value_type shall take in input the value
    '''
    if type(val) == ast.Constant:
        return type_from_constant(val)
    if type(val) == ast.BinOp:
        return type_from_bin_op(val, types_getter)
    if types_getter is not None:
        if type(val) == ast.Name:
            return types_getter.get_varname_type( val.id ) #vars_dict.get( val.id )
        if type(val) == ast.Call:
            return type_from_call(val, types_getter)#types_getter.get_callname_type( val.func.id )
    return None
        
def type_from_constant(const : ast.Constant) -> str | None:
    '''
    type_from_constant returns the type of a constant
    '''
    typ = type(const.n).__name__
    match typ:
        case 'int':
            return typ
        case 'float':
            return typ
    return None

def type_from_bin_op(
        binop : ast.BinOp,
        types_getter : WrapTypeStore | None = None
    ) -> str | None:
    '''
    type_from_bin_op shall return a string out of some binary operation
    '''
    left_type = get_value_type(binop.left, types_getter)
    if left_type is None:
        return None
    right_type = get_value_type(binop.right, types_getter)
    if right_type is None:
        return None
    if left_type == 'float' or right_type == 'float' or binop.op == ast.Div:
        return 'float'
    return 'int'

def type_from_call(
        call : ast.Call,
        types_getter : WrapTypeStore | None = None
    ) -> str | None:
    '''
    type_from_call shall return the type from a function call - basically
    checks if that func is an explicit call of 
    '''
    call_id = call.func.id if (hasattr(call, 'func') and hasattr(call.func, 'id')) else None
    if call_id is None:
        return None
    match call_id:
        case 'int':
            return 'int'
        case 'float':
            return 'float'
    if types_getter is not None:
        call_type = types_getter.get_callname_type(call_id)
        if call_type is not None:
            return call_type
    return None

def type_from_iter(iter_stat : ast.AST) -> str | None:
    '''
    type_from_iter shall get the type of a variable "extracted"
    out of an iterable statement
    '''
    if type(iter_stat) == ast.Call:
        if iter_stat.func.id == 'range':
            return 'int'
    return None


class TypesCollector:
    '''
    TypesCollector shall actually be invoked in order to collect
    types from some AST statements, ideally from some function body,
    actually no nested function declarations are considered
    '''
    _collected_types : DictTypeStore = DictTypeStore()
    _mutating_types_varnames : set[str] = set()
    _deep_coll : bool = True

    def __init__(
            self,
            statements : list[ast.AST],
            arg_types : dict[str, str] = dict(),
            outer_lever_var_types : dict[str, str] = dict(),
            func_return_types : dict[str, str] = dict(),
            deep_coll : bool = True
        ):
        '''
        TypesCollector constructor

        :param list[ast.AST] statements: ast statements
        :param dict[str, str] arg_types: types of input variables
        :param dict[str, str] outer_lever_var_types: types of outer level variables, something like globals or constants
        :param dict[str, str] func_return_types: known return types of functions
        '''
        self._statements = statements

        # tg stands for types getter
        self._input_var_tg = DictTypeStore(arg_types)
        self._n_original_input_types = len(self._input_var_tg)
        self._outer_lever_var_tg = DictTypeStore(outer_lever_var_types)
        self._n_original_outer_types = len(self._outer_lever_var_tg)
        self._func_return_tg = DictTypeStore(func_return_types)

        self._deep_coll = deep_coll

        var_types_tgs = [
            self._collected_types,
            self._input_var_tg,
            self._outer_lever_var_tg
        ]

        self._wrap_tg = WrapTypeStore(var_types_tgs, self._func_return_tg)

    def run(self) -> dict[str, str]:
        if len(self._collected_types) == 0:
            return self._run()
        else:
            return self._collected_types

    def _run(self) -> dict[str, str]:
        '''
        _run shall be internally exectued in order to fetch types
        '''
        self.collect_types(self._statements)
        return self._collected_types

    def collect_types(self, statements : list[ast.AST]):
        '''
        collect_types shall run (eventually recurvively) taking bodies and
        collecting types from statements
        '''
        for stat in statements:
            if type(stat) == ast.Assign:
                varname = stat.targets[0].id # i hypothetize the assignment to be
                if varname not in self._mutating_types_varnames:
                    vartype = get_value_type(stat.value, self._wrap_tg)
                    # here i colelct the vartype found
                    self._collect_vartype(varname, vartype)
            elif type(stat) == ast.For:
                varname = stat.target
                if varname not in self._mutating_types_varnames:
                    vartype = type_from_iter(stat.iter)
                    # here i colelct the vartype found
                    self._collect_vartype(varname, vartype)
            if hasattr(stat, 'body') and self._deep_coll:
                self.collect_types(stat.body)

    def _collect_vartype(self, varname : str, vartype: str | None) -> None:
        '''
        _collect_vartype shall add an eventual vartype to the collected
        variables, while eventually checking for collisions and stuff

        it also checks if the vartype is not None
        '''
        if vartype is not None:
            old_vartype = self._wrap_tg.get_varname_type(varname)
            if old_vartype is None:
                self._collected_types.add_type(varname, vartype)
            elif vartype != old_vartype:
                self._handle_type_mutation(varname)

    def collision_input_type(self) -> bool:
        '''
        collision_input_type shall return True in case at least one input variable changed
        type across funtion execution
        '''
        return self._n_original_input_types != len(self._input_var_tg)
    
    def collision_outer_type(self) -> bool:
        '''
        collision_outer_type shall return True in case at least one outer variable changed
        type across funtion execution
        '''
        return self._n_original_outer_types != len(self._outer_lever_var_tg)
    
    def get_input_var_tg(self) -> DictTypeStore:
        '''
        get_input_var_tg shall return the args type store
        '''
        return self._input_var_tg
    
    def get_collected_tg(self) -> DictTypeStore:
        '''
        get_collected_tg shall return the 
        '''
        return self._collected_types

    def _handle_type_mutation(self, varname : str) -> None:
        self._wrap_tg.delete_varname(varname)
        self._mutating_types_varnames.add(varname)

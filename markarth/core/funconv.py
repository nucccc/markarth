'''
func_conv shall account for converting a function to cython - nobody knows how, and either why
'''

import ast

from typing import Iterator

from markarth.core.utils import toASTCodelines
from markarth.core.typestore import TypeStore, DictTypeStore, WrapTypeStore

VALID_CTYPES = {
    'int',
    'float'
}

def code_portion(ast_node : ast.AST, codelines : list[str]) -> str:
    '''
    code_portion takes in input a node, some codelins, and returns as a string
    the code portion of interest
    '''
    portion_codelines = codelines[ast_node.lineno:ast_node.end_lineno+1]
    portion_codelines[-1] = portion_codelines[-1][:ast_node.end_col_offset]
    portion_codelines[0] = portion_codelines[0][ast_node.col_offset:]
    return '\n'.join(portion_codelines)

def cdef_lines_from_iter(
        iter : Iterator[ tuple[str, str] ],
        indent_level : int = 0,
        indent_pattern : str = '\t'
    ) -> list[str]:
    '''
    cdef_lines_from_iter shall take in input an iterator of (varname, vartype)
    and turn it inot a list of cdef lines with a given indent_level
    '''
    cdef_str = ( indent_pattern * indent_level ) + 'cdef {vartype} {varname}'
    return [
        cdef_str.format(varname=varname, vartype=vartype)
        for varname, vartype in iter
    ]

def cdef_lines_from_tg(
        tg : TypeStore,
        indent_level : int = 0,
        indent_pattern : str = '\t'
    ) -> list[str]:
    '''
    cdef_lines_from_tg takes in input a type getter, and returns as an output
    a list of cdef codelines declaring with a type the vars indicated,
    '''
    return cdef_lines_from_iter(
        iter=tg.iter_types(),
        indent_level=indent_level,
        indent_pattern=indent_pattern
    )


class FuncConverter():
    '''
    FuncConverter shall take care of converting a function from python to cython
    
    some documentation about the attributes may be a good idea
    '''
    func_ast : ast.FunctionDef
    codelines : list[str]
    statements : list[ast.AST]
    call_types : dict[str, str] = dict()
    func_decl : str # the string containing the function declaration (that line with function name, arguments and so on)
    arg_types : dict[str, str] = dict()
    return_type : str | None = None
    cdef_lines : list[str] = list()

    def __init__(self, func_ast : ast.FunctionDef, codelines : list[str]):
        self.func_ast = func_ast
        self.statements = self.func_ast.body
        self.codelines = codelines

    def convert(self) -> str:
        '''
        convert shall actually execute the app conversion
        '''
        self._collect_start_attributes()

        # then i shall actually collect the types
        self._collect_types()
        self._add_ctypes_to_args()
        self.func_decl = self._get_func_decl()
        self.func_decl = self._regen_def_line()
        new_codelines = [self.func_decl] + self.cdef_lines + self.codelines[self.func_ast.body[0].lineno:self.func_ast.body[-1].end_lineno+1]
        return '\n'.join(new_codelines)

    def _collect_start_attributes(self) -> None:
        '''
        _collect_start_attributes shall collect all that can be taken at the
        beginning (function arguments, their types, return type and stuff)
        '''
        self.arg_types = self._collect_arg_types()
        self.return_type = self._collect_return_type()

    def _collect_types(self):
        '''
        _collect_types just launches a types collector
        '''
        tc = TypesCollector(
            statements=self.statements,
            arg_types=self.arg_types
        )
        tc.run()
        if tc.collision_input_type():
            # in case of input type collision i shall have a new dictionary for
            # input arguments types
            self.arg_types = {
                varname : typename
                for varname, typename in tc.get_input_var_tg().iter_types()
            }
        #this could be better something coming out directly as a result from types collector, or a dedicated function
        self.cdef_lines = cdef_lines_from_tg(tg = tc.get_collected_tg(), indent_level= 1)

    def _regen_def_line(self) -> str:
        '''
        _regen_def_line shall return a def line with types and so on possibly
        '''
        new_def_line = 'cp' + self.func_decl
        if self.return_type is not None:
            first_line = new_def_line.split(' ')
            first_line.insert(1, self.return_type)
            new_def_line = ' '.join(first_line)
        return new_def_line
    
    def _add_ctypes_to_args(self) -> list[str]:
        line_inc = dict()
        for arg in self.func_ast.args.args:
            argname = arg.arg
            argtype = self.arg_types.get(argname, None)
            if argtype is not None:
                lineno = arg.lineno
                line = self.codelines[lineno]
                ins_pos = arg.col_offset + line_inc.get(lineno, 0)
                line = line[:ins_pos] + argtype + ' ' + line[ins_pos:]
                self.codelines[arg.lineno] = line
                if lineno in line_inc.keys():
                    line_inc[lineno] += 1 + len(argtype)
                else:
                    line_inc[lineno] = 1 + len(argtype)
    
    def _get_func_decl(self) -> str:
        return '\n'.join(self.codelines[self.func_ast.lineno:self.func_ast.body[0].lineno])
    
    def _collect_arg_types(self) -> dict[str, str]:
        arg_types = {
            arg.arg : arg.annotation.id
            for arg in self.func_ast.args.args
            if hasattr(arg.annotation, 'id') and (arg.annotation.id == 'int' or arg.annotation.id == 'float')
        }
        return arg_types
    
    def _collect_return_type(self) -> str | None:
        return self.func_ast.returns.id \
            if hasattr(self.func_ast.returns, 'id') else None


def isValidCType(ctype : str) -> bool:
    return ctype in VALID_CTYPES

def test_funcConv(func_code : str) -> str:
    '''
    just a function to quickly test funcConv
    '''
    func_ast = ast.parse(func_code).body[0]
    func_codelines = toASTCodelines(func_code)
    return funcConv(func_ast, func_codelines)

def funcReturnTypeFromAST(func_ast : ast.FunctionDef) -> str:
    '''
    funcReturnTypeFromAST shall extrapolate the return type of a function from its parsing
    '''
    return func_ast.returns.id if hasattr(func_ast.returns, 'id') else ''

def funcConv(func_ast : ast.FunctionDef, codelines : list[str]) -> str:
    #at first i should modify the name of the function
    
    return_type = funcReturnTypeFromAST( func_ast )

    first_line = '\n'.join(codelines[func_ast.lineno:func_ast.body[0].lineno])
    first_line = 'cp' + first_line
    if return_type != '':
        first_line = first_line.split(' ')
        first_line.insert(1, return_type)
        first_line = ' '.join(first_line)

    types_by_var = defTypes(func_ast.body)

    def_lines = [ '\tcdef {vartype} {varname}'.format(varname=varname, vartype=vartype) for varname, vartype in types_by_var.items() ]

    #SEVERAL THINGS IN THE MIDDLE TO BE DONE

    cy_func_code = [first_line] + def_lines + codelines[func_ast.lineno+1:func_ast.end_lineno + 1]

    cy_func_code ='\n'.join( cy_func_code )

    return cy_func_code

def getValueType(
        val : ast.AST,
        types_getter : WrapTypeStore | None = None
    ) -> str | None:
    '''
    getValueType shall take in input the value
    '''
    if type(val) == ast.Constant:
        return typeFromConstant(val)
    if type(val) == ast.BinOp:
        return typeFromBinOp(val, types_getter)
    if types_getter is not None:
        if type(val) == ast.Name:
            return types_getter.get_varname_type( val.id ) #vars_dict.get( val.id )
        if type(val) == ast.Call:
            return typeFromCall(val, types_getter)#types_getter.get_callname_type( val.func.id )
    return None
        
def typeFromConstant(const : ast.Constant) -> str | None:
    typ = type(const.n).__name__
    match typ:
        case 'int':
            return typ
        case 'float':
            return typ
    return None

def typeFromBinOp(
        binop : ast.BinOp,
        types_getter : WrapTypeStore | None = None
    ) -> str | None:
    '''
    typeFromBinOp shall return a string out of some binary operation
    '''
    left_type = getValueType(binop.left, types_getter)
    if left_type is None:
        return None
    right_type = getValueType(binop.right, types_getter)
    if right_type is None:
        return None
    if left_type == 'float' or right_type == 'float' or binop.op == ast.Div:
        return 'float'
    return 'int'

def typeFromCall(
        call : ast.Call,
        types_getter : WrapTypeStore | None = None
    ) -> str | None:
    '''
    typeFromCall shall return the type from a function call - basically
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



def defTypes(statements : list[ast.AST]) -> dict[str, str]:
    '''
    defTypes shall take statements and return types out of them
    '''
    types_by_var = dict()
    for stat in statements:
        if type(stat) == ast.Assign:
            varname = stat.targets[0].id # i hypothetize the assignment to be
            vartype = getValueType(stat.value)
            if vartype is not None:
                types_by_var[varname] = vartype
        elif hasattr(stat, 'body'):
            types_by_var.update( defTypes(stat.body ) )
    return types_by_var

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
        self.collectTypes(self._statements)
        return self._collected_types

    def collectTypes(self, statements : list[ast.AST]):
        for stat in statements:
            if type(stat) == ast.Assign:
                varname = stat.targets[0].id # i hypothetize the assignment to be
                if varname not in self._mutating_types_varnames:
                    vartype = getValueType(stat.value, self._wrap_tg)
                    # here i should also check if i have something
                    if vartype is not None:
                        old_vartype = self._wrap_tg.get_varname_type(varname)
                        if old_vartype is None:
                            self._collected_types.add_type(varname, vartype)
                        elif vartype != old_vartype:
                            self._handle_type_mutation(varname)
            elif hasattr(stat, 'body') and self._deep_coll:
                self.collectTypes(stat.body)

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
        return self._input_var_tg
    
    def get_collected_tg(self) -> DictTypeStore:
        return self._collected_types

    

    def _handle_type_mutation(self, varname : str):
        self._wrap_tg.delete_varname(varname)
        self._mutating_types_varnames.add(varname)
    
    def fetchTypeFromName(self, var_name : str) -> str | None:
        '''
        DEPRECATED
        '''
        pass

        var_type = None
        for var_type_source in self._var_types_sources:
            var_type = var_type_source.get(var_name, None)
            if var_type is not None:
                return var_type
        return var_type

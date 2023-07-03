'''
func_conv shall account for converting a function to cython - nobody knows how, and either why
'''

import ast

from typing import Iterator

from.conv_opts import ConvOpts, default_convopts
from .utils import indentation_pattern
from .typestore import DictTypeStore, TypeStore, py2cy_dict_store
from .typecollector import TypesCollector

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
    indent_pattern : str
    # i also save the types stores as i'm going to use them for unit testing
    collected_ptypes : DictTypeStore
    collected_ctypes : DictTypeStore

    def __init__(self, func_ast : ast.FunctionDef, codelines : list[str], conversion_options : ConvOpts = default_convopts()):
        self.func_ast = func_ast
        self.statements = self.func_ast.body
        self.codelines = codelines
        self.convertion_options = conversion_options

    def convert(self) -> str:
        '''
        convert shall actually execute the app conversion
        '''
        self._collect_start_attributes()

        # then i shall actually collect the types
        self._collect_types()
        #self._add_ctypes_to_args()
        
        return self._regen_code()
        
    
    def _regen_code(self) -> str:
        '''
        _regen_code returns the newly generated function code
        '''
        self._remove_return_annotation()
        self.func_decl = self._get_func_decl()
        self.func_decl = self._regen_def_line()
        new_codelines = [self.func_decl] + self.cdef_lines + self.codelines[self.func_ast.body[0].lineno:self.func_ast.body[-1].end_lineno+1]
        return '\n'.join(new_codelines)

    def _collect_start_attributes(self) -> None:
        '''
        _collect_start_attributes shall collect all that can be taken at the
        beginning (function arguments, their types, return type and stuff)
        '''
        self.indent_pattern = indentation_pattern(self.func_ast, self.codelines)
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
        # i check whether or not there was a type collision with an input type
        if tc.collision_input_type():
            # in case of input type collision i shall have a new dictionary for
            # input arguments types
            self.arg_types = {
                varname : typename
                for varname, typename in tc.get_input_var_tg().iter_types()
            }
        self.collected_ptypes = tc.get_collected_tg()
        # before actually generating the cdef lines i shall regen the type store in order for it to contain
        # the actual c types
        self.collected_ctypes = py2cy_dict_store(self.collected_ptypes, self.convertion_options.py2cy_typemap())
        #this could be better something coming out directly as a result from types collector, or a dedicated function
        self.cdef_lines = cdef_lines_from_tg(
            tg = self.collected_ctypes,
            indent_level= 1,
            indent_pattern=self.indent_pattern
        )

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
        arg_types_tg = DictTypeStore(self.arg_types)
        arg_types_tg = py2cy_dict_store(arg_types_tg, self.convertion_options.py2cy_typemap())
        for arg in self.func_ast.args.args:
            argname = arg.arg
            argtype = arg_types_tg.get_type(argname)
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
        return_type = self.func_ast.returns.id \
            if hasattr(self.func_ast.returns, 'id') else None
        return_type = self.convertion_options.py2cy_typemap().get(return_type, None)
        return return_type
    
    def _remove_return_annotation(self) -> None:
        '''
        _remove_return_annotation shall remove the annotation regarding
        the return type (as this will go in the cpdef definition)
        
        this assumes the return annotation is going to be on just one line
        '''
        if self.return_type is not None:
            return_lineno = self.func_ast.returns.lineno
            start_pos = self.func_ast.returns.col_offset
            end_pos = self.func_ast.returns.end_col_offset
            return_line = self.codelines[ return_lineno ]
            # now i need to search for the first parenthes to modify the statement
            while return_line[start_pos-1] != ')':
                start_pos -= 1
            new_def = return_line[:start_pos] + return_line[end_pos:]
            print(new_def)
            self.codelines[ return_lineno ] = new_def

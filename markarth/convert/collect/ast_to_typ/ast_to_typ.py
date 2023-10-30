'''
ok, a long time ago there were functionalities to read in ast assignments
and obtain strings representing types out of them 
'''

import ast

from markarth.convert.typs import typs
from markarth.convert.typs.names_to_typs import NamesToTyps

# TODO: just decide if these things can return a None or typ unknown

def ast_val_to_typ(
        val : ast.AST,
        name_typs : NamesToTyps | None = None
    ) -> typs.Typ:
    '''
    get_value_type shall take in input the value
    '''
    if type(val) == ast.Constant:
        return typ_from_constant(val)
    if type(val) == ast.BinOp:
        return typ_from_bin_op(val, name_typs)
    if name_typs is not None:
        if type(val) == ast.Name:
            supposed_typ = name_typs.get_varname_typ( val.id )
            # i check if a value was actually present by checking for none
            # to be returned by the typstore, in such case i just return
            # any
            if supposed_typ is None:
                return typs.TypAny() 
            return supposed_typ
        if type(val) == ast.Call:
            return typ_from_call(val, name_typs)#name_typs.get_callname_type( val.func.id )
    return None


def typ_from_constant(const : ast.Constant) -> typs.TypPrimitive | typs.TypAny:
    '''
    typ_from_constant returns the type of a constant
    '''
    typ_str = type(const.n).__name__
    prim_cod = typs.str_to_prim_cod_or_none(typ_str)
    if prim_cod is None:
        return typs.TypAny()
    return typs.TypPrimitive(prim_cod)


def typ_from_bin_op(
        binop : ast.BinOp,
        name_typs : NamesToTyps | None = None
    ) -> typs.Typ:
    '''
    typ_from_bin_op shall return a string out of some binary operation
    '''
    left_type = ast_val_to_typ(binop.left, name_typs)
    if not left_type.is_primitive():
        return typs.TypAny()
    right_type = ast_val_to_typ(binop.right, name_typs)
    if not right_type.is_primitive():
        return typs.TypAny()
    # at this stage both types should be primitives
    left_prim : typs.TypPrimitive = left_type
    right_prim : typs.TypPrimitive = right_type
    if left_prim.is_float() or right_prim.is_float() or type(binop.op) == ast.Div:
        return typs.TypPrimitive( typs.PrimitiveCod.FLOAT )
    return typs.TypPrimitive( typs.PrimitiveCod.INT )


def typ_from_call(
        call : ast.Call,
        name_typs : NamesToTyps | None = None
    ) -> typs.Typ:
    '''
    typ_from_call shall return the type from a function call - basically
    checks if that func is an explicit call of 
    '''
    call_id = call.func.id if (hasattr(call, 'func') and hasattr(call.func, 'id')) else None
    if call_id is None:
        return None
    # TODO: this could become a dictionary with several entries for each built-in
    # function with call names
    match call_id:
        case 'int':
            return typs.TypPrimitive(typs.PrimitiveCod.INT)
        case 'float':
            return typs.TypPrimitive(typs.PrimitiveCod.FLOAT)
        case 'bool':
            return typs.TypPrimitive(typs.PrimitiveCod.BOOL)
    if name_typs is not None:
        call_type = name_typs.get_callname_typ(call_id)
        if call_type is not None:
            return call_type
    return typs.TypAny()

def typ_from_iter(iter_stat : ast.AST) -> typs.Typ:
    '''
    type_from_iter shall get the type of a variable "extracted"
    out of an iterable statement
    '''
    if type(iter_stat) == ast.Call:
        if iter_stat.func.id == 'range':
            return typs.TypPrimitive(typs.PrimitiveCod.INT)
    return typs.TypAny()

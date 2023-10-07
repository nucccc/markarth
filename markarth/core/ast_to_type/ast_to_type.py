'''
ok, a long time ago there were functionalities to read in ast assignments
and obtain strings representing types out of them 
'''

import ast

from markarth.core.types import types
from markarth.core.names_to_typs.names_to_typs import NamesToTyps

def ast_val_to_typ(
        val : ast.AST,
        types_getter : WrapTypeStore | None = None
    ) -> types.Typ:
    '''
    get_value_type shall take in input the value
    '''
    if type(val) == ast.Constant:
        return typ_from_constant(val)
    if type(val) == ast.BinOp:
        return typ_from_bin_op(val, types_getter)
    if types_getter is not None:
        if type(val) == ast.Name:
            # here some more code could be placed to handle a none and see if
            # returning known or unknown
            return types_getter.get_varname_type( val.id ) #vars_dict.get( val.id )
        if type(val) == ast.Call:
            return typ_from_call(val, types_getter)#types_getter.get_callname_type( val.func.id )
    return None


def typ_from_constant(const : ast.Constant) -> types.TypPrimitive | types.TypUnknown:
    '''
    typ_from_constant returns the type of a constant
    '''
    typ_str = type(const.n).__name__
    prim_cod = types.str_to_primitive_cod_or_none(typ_str)
    if prim_cod is None:
        return types.TypUnknown()
    return types.TypPrimitive(prim_cod)


def typ_from_bin_op(
        binop : ast.BinOp,
        types_getter : WrapTypeStore | None = None
    ) -> str | None:
    '''
    typ_from_bin_op shall return a string out of some binary operation
    '''
    left_type = ast_val_to_typ(binop.left, types_getter)
    if not left_type.is_primitive():
        return types.TypUnknown()
    right_type = ast_val_to_typ(binop.right, types_getter)
    if not right_type.is_primitive():
        return types.TypUnknown()
    # at this stage both types should be primitives
    left_prim : types.TypPrimitive = left_type
    right_prim : types.TypPrimitive = right_type
    if left_prim.is_float() or right_prim.is_float() or type(binop.op) == ast.Div:
        return types.TypPrimitive( types.PrimitiveCod.FLOAT )
    return types.TypPrimitive( types.PrimitiveCod.INT )


def typ_from_call(
        call : ast.Call,
        typs_getter : WrapTypeStore | None = None
    ) -> str | None:
    '''
    typ_from_call shall return the type from a function call - basically
    checks if that func is an explicit call of 
    '''
    call_id = call.func.id if (hasattr(call, 'func') and hasattr(call.func, 'id')) else None
    if call_id is None:
        return None
    match call_id:
        case 'int':
            return types.TypPrimitive(types.PrimitiveCod.INT)
        case 'float':
            return types.TypPrimitive(types.PrimitiveCod.FLOAT)
        case 'bool':
            return types.TypPrimitive(types.PrimitiveCod.BOOL)
    if typs_getter is not None:
        call_type = typs_getter.get_callname_typ(call_id)
        if call_type is not None:
            return call_type
    return None
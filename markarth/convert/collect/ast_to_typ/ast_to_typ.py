'''
ok, a long time ago there were functionalities to read in ast assignments
and obtain strings representing types out of them 
'''

import ast

from markarth.convert.collect.vartyp_tracker import VarTypTracker
from markarth.convert.typs import typs

# TODO: just decide if these things can return a None or typ unknown


def ast_val_to_typ(
        val : ast.AST,
        var_tracker : VarTypTracker | None = None
    ) -> typs.Typ:
    '''
    get_value_type shall take in input the value
    '''
    if type(val) == ast.Constant:
        return typ_from_constant(val)
    if type(val) == ast.BinOp:
        return typ_from_bin_op(val, var_tracker)
    if var_tracker is not None:
        if type(val) == ast.Name:
            supposed_typ = var_tracker.get_vartyp( val.id )
            # i check if a value was actually present by checking for none
            # to be returned by the typstore, in such case i just return
            # any
            if supposed_typ is None:
                return typs.TypAny() 
            return supposed_typ
        if type(val) == ast.Call:
            return typ_from_call(val, var_tracker)#var_tracker.get_callname_type( val.func.id )
    return typs.TypAny()


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
        var_tracker : VarTypTracker | None = None
    ) -> typs.Typ:
    '''
    typ_from_bin_op shall return a string out of some binary operation
    '''

    left_typ = ast_val_to_typ(binop.left, var_tracker)
    right_typ = ast_val_to_typ(binop.right, var_tracker)

    op = binop.op

    return eval_op_typ(
        op = op,
        left_typ = left_typ,
        right_typ = right_typ
    )


def eval_op_typ(
    op : ast.Add | ast.Sub | ast.Mult | ast.Mult | ast.Div,
    left_typ : typs.Typ,
    right_typ : typs.Typ
) -> typs.Typ:
    '''
    eval_op_typ shall return a typ from an ast op and two operands
    '''
    if not (left_typ.is_primitive() and right_typ.is_primitive()):
        return typs.TypAny()
    
    if left_typ.is_str() and right_typ.is_str():
        return typs.TypPrimitive( typs.PrimitiveCod.STR )
    elif left_typ.is_str() or right_typ.is_str():
        return typs.TypAny()
    
    if left_typ.is_float() or right_typ.is_float() or type(op) == ast.Div:
        return typs.TypPrimitive( typs.PrimitiveCod.FLOAT )
    return typs.TypPrimitive( typs.PrimitiveCod.INT )


def typ_from_call(
        call : ast.Call,
        var_tracker : VarTypTracker | None = None
    ) -> typs.Typ:
    '''
    typ_from_call shall return the type from a function call - basically
    checks if that func is an explicit call of 
    '''
    # in case the function call is a method, this is a way to exclude it from
    # processing until a way to obtain its name is developed
    if not hasattr(call.func, 'id'):
        return typs.TypAny()
    call_id = call.func.id
    #call_id = call.func.id if (hasattr(call, 'func') and hasattr(call.func, 'id')) else None
    #if call_id is None:
    #    return None
    # TODO: this could become a dictionary with several entries for each built-in
    # function with call names
    match call_id:
        case 'int':
            return typs.TypPrimitive(typs.PrimitiveCod.INT)
        case 'float':
            return typs.TypPrimitive(typs.PrimitiveCod.FLOAT)
        case 'bool':
            return typs.TypPrimitive(typs.PrimitiveCod.BOOL)
        case 'str':
            return typs.TypPrimitive(typs.PrimitiveCod.STR)
        case 'len':
            return typs.TypPrimitive(typs.PrimitiveCod.INT)
    if var_tracker is not None:
        call_type = var_tracker.get_call_typ(call_id)
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

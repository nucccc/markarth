'''
is a module parsing a string annotation going to be useful?

maybe so
'''

from markarth.convert.typs import typs


def parse_type_str(type_str : str) -> typs.Typ:
    '''
    parse_type_str shall be HEAVILY DEVELOPED
    '''
    prim_cod_trial = typs.str_to_prim_cod_or_none(type_str)
    if prim_cod_trial is not None:
        return typs.TypPrimitive(prim_cod_trial)
    
    # TODO: a lot
    
    return typs.TypAny()



'''
is a module parsing a string annotation going to be useful?

maybe so
'''

from markarth.core.types import types


def parse_type_str(type_str : str) -> types.Typ:
    '''
    parse_type_str shall be HEAVILY DEVELOPED
    '''
    prim_cod_trial = types.str_to_prim_cod_or_none(type_str)
    if prim_cod_trial is not None:
        return types.TypPrimitive(prim_cod_trial)
    
    return types.TypUnknown()



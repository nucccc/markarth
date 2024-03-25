'''
is a module parsing a string annotation going to be useful?

maybe so
'''

from markarth.convert.typs import typs

# TODO: exception in case the string type is invalid

# TODO: maybe a preprocessing to remove spaces and other unuseful chars


def parse_type_str(type_str : str) -> typs.Typ:
    '''
    parse_type_str shall be HEAVILY DEVELOPED
    '''
    prim_cod_trial = typs.str_to_prim_cod_or_none(type_str)
    if prim_cod_trial is not None:
        return typs.TypPrimitive(prim_cod_trial)
    
    # this shall now parse None
    if type_str == 'None':
        return typs.TypNone()
    
    # checking if it is a list
    if type_str[0:4] == 'list':
        if len(type_str) == 4:
            # in such case this is just a list with no inner type expression
            return typs.TypList()
        if len(type_str) > 6 and type_str[4] == '[' and type_str[-1] == ']':
            inner_typ = parse_type_str(type_str[5:-1])
            return typs.TypList(inner_typ = inner_typ)
        # TODO: something should be done to point out a malformed string, not?
    
    return typs.TypAny()



'''
in here there should be the function
'''

from markarth.convert.typs import typs

def merge_typs(t1 : typs.Typ, t2 : typs.Typ) -> typs.Typ:
    '''
    okay so you may have two different typs, maybe you'll want a type that
    handles both
    '''
    # at first i shall check if both are any, in case any is the result
    if t1.is_any():
        return t1
    if t2.is_any():
        return t2
    # then just check if they're equal!
    if t1 == t2:
        return t1
    # okay, in such case probably the result shall be a union, but i shall
    # somehow check if any of these is actually a union
    if t1.is_union():
        union_typ : typs.TypUnion = t1
        other_typ = t2
    elif t2.is_union():
        union_typ : typs.TypUnion = t2
        other_typ = t1
    else:
        union_typ = None
        other_typ = None
    
    if union_typ is None:
        result = typs.TypUnion()
        result.add_typ(t1)
        result.add_typ(t2)
        return result
    
    if other_typ.is_union():
        other_union : typs.TypUnion = other_typ
        for t in other_union.get_union_types:
            union_typ.add_typ(t)
    else:
        union_typ.add_typ(other_typ)
    
    return union_typ
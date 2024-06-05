'''
here in declare gen there is code to generate type declare code for pyx syntax
'''

# TODO: wouldn't it be nice if in the code here there was something very
# pragmatic to express that gen_declare_line_pyx is supposed to have a very well defined
# interface to be used then and passed around as an argument

def gen_declare_line_pyx(
    varname : str,
    cy_typename : str,
    cy_alias : str,
    indent_pattern : str = ''
) -> str:
    '''
    gen_declare_line shall generate a declare line for a given varname
    '''
    return f'{indent_pattern}cdef {varname} {cy_typename}'
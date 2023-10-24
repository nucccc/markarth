'''
conv_opts shall provide options to perform conversion
'''

class ConvOpts():
    '''
    ConvOpts shall contain options for a function conversion
    '''
    float_to_double : bool = False
    int_to_long : bool = False

    def __init__(self):
        pass

    def py2cy_typemap(self) -> dict[str, str]:
        '''
        py2cy_typemap returns a dictionary with the required mapping from
        python types to c ones
        '''
        return {
            'bool':'char',
            'float':'double' if self.float_to_double else 'float',
            'int':'long' if self.int_to_long else 'int'
        }
    
def default_convopts() -> ConvOpts:
    '''
    default_convopts returns a default object of class ConvOpts
    '''
    return ConvOpts()
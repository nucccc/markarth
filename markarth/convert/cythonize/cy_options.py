'''
yeah someone should begin giving us some options on the stuff, like
really with pydantic
'''

from markarth.convert.cythonize.cy_typs import CyInt, CyFloat

from pydantic import BaseModel, Field

from typing import Dict

# yeah fields may be all optional, with default stuff and so on
class FuncOpts(BaseModel):
    default_int_cytyp : CyInt | None = Field(default = None, description='default c type to be used for integers')
    default_float_cytyp : CyFloat | None = Field(default = None, description='default c type to be used for integers')


class ModOpts(BaseModel):
    default_int_cytyp : CyInt = Field(default = CyInt.INT, description='default c type to be used for integers')
    default_float_cytyp : CyFloat = Field(default = CyFloat.FLOAT, description='default c type to be used for integers')
    imposed_consts : dict[str, CyInt | CyFloat] = Field(default=dict())
    funcs_opts : dict[str, FuncOpts] = Field(default=dict())


    def cascade(self):
        '''
        let's see if such a method can be used to propagate options from
        the module level
        '''
        for func_opts in self.funcs_opts.values():
            if func_opts.default_int_cytyp is None:
                func_opts.default_int_cytyp= self.default_int_cytyp
            if func_opts.default_float_cytyp is None:
                func_opts.default_float_cytyp= self.default_float_cytyp
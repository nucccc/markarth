'''
yeah someone should begin giving us some options on the stuff, like
really with pydantic
'''

from markarth.convert.cythonize.cy_typs import CyInt, CyFloat

from pydantic import BaseModel, Field

from typing import Dict

# yeah fields may be all optional, with default stuff and so on
class FuncOpts(BaseModel):
    internal_default_int_cytyp : CyInt | None = Field(default = None, description='default c type to be used for integers')
    internal_default_float_cytyp : CyFloat | None = Field(default = None, description='default c type to be used for integers')
    parent_mod : "ModOpts"
    imposed_vars : dict[str, CyInt | CyFloat] = Field(default=dict())
    ignore_assignment_annotations : bool | None = Field(default = None, description='used to indicate if annotations in assignment need to be ignored')


    @property
    def default_int_cytyp(self) -> CyInt:
        if self.internal_default_int_cytyp is None:
            return self.parent_mod.default_int_cytyp
        return self.internal_default_int_cytyp


    @property
    def default_float_cytyp(self) -> CyFloat:
        if self.internal_default_float_cytyp is None:
            return self.parent_mod.default_float_cytyp
        return self.internal_default_float_cytyp
    

    @property
    def actual_ignore_assignment_annotations(self) -> bool:
        '''
        since the field ignore_assignment_annotations could be none, this
        property method shall be used to obtain an actual value
        '''
        if self.ignore_assignment_annotations is None:
            return self.parent_mod.ignore_assignment_annotations
        return self.ignore_assignment_annotations


class ModOpts(BaseModel):
    default_int_cytyp : CyInt = Field(default = CyInt.INT, description='default c type to be used for integers')
    default_float_cytyp : CyFloat = Field(default = CyFloat.FLOAT, description='default c type to be used for integers')
    imposed_consts : dict[str, CyInt | CyFloat] = Field(default=dict())
    funcs_opts : dict[str, FuncOpts] = Field(default=dict())
    ignore_assignment_annotations : bool = Field(default = False, description='used to indicate if annotations in assignment need to be ignored')


    def gen_default_func_opt(self) -> FuncOpts:
        '''
        yeah at times there is this thing that i need, a default option for
        any function without options
        '''
        # NOTE: yeah i know actually passing the default types to the new func
        # opt doesn't seem to be useful
        return FuncOpts(
            internal_default_float_cytyp=self.default_float_cytyp,
            internal_default_int_cytyp=self.default_int_cytyp,
            parent_mod=self
        )

    def get_f_opt_or_default(self, f_name : str) -> FuncOpts:
        '''
        get_f_opt_or_default returns func opts of a function, if function has
        no specific opts then a default opt is generated
        '''
        return self.funcs_opts.get(f_name, self.gen_default_func_opt())
    
def gen_default_mod_opts() -> ModOpts:
    '''
    to return a default module option for when nobody wants to parse anything
    '''
    return ModOpts()
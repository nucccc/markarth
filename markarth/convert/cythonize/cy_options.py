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


class ModOpts(BaseModel):
    default_int_cytyp : CyInt = Field(default = CyInt.INT, description='default c type to be used for integers')
    default_float_cytyp : CyFloat = Field(default = CyFloat.FLOAT, description='default c type to be used for integers')
    imposed_consts : dict[str, CyInt | CyFloat] = Field(default=dict())
    funcs_opts : dict[str, FuncOpts] = Field(default=dict())
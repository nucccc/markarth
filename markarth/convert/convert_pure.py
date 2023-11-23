'''
yeah let's play with stuff
'''

from markarth.convert.preprocess import code_process
from markarth.convert.collect.mod_collect import mod_collect
from markarth.convert.cythonize.cy_options import ModOpts, gen_default_mod_opts
from markarth.convert.cythonize.pure import pure_cythonize

def convert_code(code : str) -> str:
    ast_mod, codelines = code_process.process_code(code)
    
    mod_collect_res = mod_collect(ast_mod)

    m_opts : ModOpts = gen_default_mod_opts()

    new_code = pure_cythonize(
        mod_ast = ast_mod,
        codelines = codelines,
        consts_typ_store = mod_collect_res.global_typs,
        funcs_collected = mod_collect_res.func_colls,
        m_opts = m_opts
    )

    return new_code

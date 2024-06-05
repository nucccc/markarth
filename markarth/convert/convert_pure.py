'''
yeah let's play with stuff
'''

from markarth.convert.preprocess import code_process
from markarth.convert.collect.mod_collect import mod_collect
from markarth.convert.cythonize.cy_options import ModOpts, gen_default_mod_opts
from markarth.convert.cythonize.pure import cythonify_pure


def convert_code(
    code : str,
    m_opts : ModOpts | None = None
) -> str:
    ast_mod, codelines = code_process.process_code(code)

    if m_opts is None:
        m_opts : ModOpts = gen_default_mod_opts()

    mod_collect_res = mod_collect(ast_mod, m_opts)

    new_code = cythonify_pure(
        mod_ast = ast_mod,
        codelines = codelines,
        mod_coll = mod_collect_res,
        m_opts = m_opts
    )

    return new_code

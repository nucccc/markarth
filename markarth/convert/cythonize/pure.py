import ast

from markarth.convert.collect.mod_collect import ModCollectionResult
from markarth.convert.cythonize.base import cythonify, CythonifyLogic
from markarth.convert.cythonize.cy_options import ModOpts
from markarth.convert.cythonize.pure_funcs.declare_gen import typ_store_to_cdeclares


pure_logic = CythonifyLogic(
    cython_import_needed=True,
    typ_store_to_cdeclares=typ_store_to_cdeclares
)


def cythonify_pure(
    mod_ast : ast.Module,
    codelines : list[str],
    mod_coll : ModCollectionResult,
    m_opts : ModOpts,
) -> str:
    return cythonify(
        mod_ast=mod_ast,
        codelines=codelines,
        mod_coll=mod_coll,
        m_opts=m_opts,
        clogic=pure_logic
    )
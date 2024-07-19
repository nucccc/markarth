from pathlib import Path
import subprocess
import tempfile

from markarth.convert.convert_pure import convert_code

def test_sample0(tmp_path):
    fname = 'sample1.py'

    with open(Path('tests')/ 'samples' / fname, 'r') as f:
        code = f.read()

    converted_code = convert_code(code)

    fdest = tmp_path / fname
    with open(fdest, 'w') as f:
        f.write(converted_code)

    setup_body = f'''
from setuptools import setup
from Cython.Build import cythonize

import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

setup(
	name='fibonacci',
	ext_modules=cythonize(
        ['{fdest}'],
        annotate=True,
        compiler_directives={{'language_level' : '3'}}
    )
)
'''
    with open(tmp_path / 'setup.py', 'w') as f:
        f.write(setup_body)

    proc = subprocess.Popen(
        ['python3', 'setup.py', 'build_ext', '--inplace'],
        cwd=tmp_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = proc.communicate()

    print(stdout.decode())
    print(stderr.decode())

    assert len(stderr) == 0
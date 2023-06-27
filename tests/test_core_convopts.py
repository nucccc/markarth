from markarth.core import conv_opts

import pytest

def test_default_convopts():
    def_convopts = conv_opts.default_convopts()

    assert def_convopts.int_to_long == False
    assert def_convopts.float_to_double == False

def test_py2cy_typemap():
    co = conv_opts.ConvOpts()

    co.int_to_long = False
    co.float_to_double = False
    tm = co.py2cy_typemap()
    assert len(tm) == 3
    assert tm.get('bool', None) == 'char'
    assert tm.get('float', None) == 'float'
    assert tm.get('int', None) == 'int'

    co.int_to_long = True
    co.float_to_double = False
    tm = co.py2cy_typemap()
    assert len(tm) == 3
    assert tm.get('bool', None) == 'char'
    assert tm.get('float', None) == 'float'
    assert tm.get('int', None) == 'long'

    co.int_to_long = False
    co.float_to_double = True
    tm = co.py2cy_typemap()
    assert len(tm) == 3
    assert tm.get('bool', None) == 'char'
    assert tm.get('float', None) == 'double'
    assert tm.get('int', None) == 'int'

    co.int_to_long = True
    co.float_to_double = True
    tm = co.py2cy_typemap()
    assert len(tm) == 3
    assert tm.get('bool', None) == 'char'
    assert tm.get('float', None) == 'double'
    assert tm.get('int', None) == 'long'
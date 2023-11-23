import pytest

from markarth.convert.convert_pure import convert_code


def test_convert_pure(code_mod3):
    converted_code = convert_code(code_mod3)

    print(converted_code)
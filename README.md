# markarth

![Coverage badge](https://raw.githubusercontent.com/nucccc/markarth/python-coverage-comment-action-data/badge.svg)

markarth is a library to automatically cythonize python code.

It can receive in input python code, evaluate the primitive types that variables are going to possess, and then add codelines for [pure python cython mode](https://cython.readthedocs.io/en/latest/src/tutorial/pure.html).

## Example

This is an example of python code using markarth to take a code section as a string and returns a string with cython annotations.

```from markarth import convert_code

code = '''
def stuff(a : int, b : int, c : float = 0.4, d = None) -> int:
    sum = 0
    m = 11
    onono = 17.4
    for i in range(4):
        p = 7
        h = float(64) * p
        sum += i
        sum = 5 * 18
    return float(sum)

'''

cycode = convert_code(code)

print(cycode)
```

The resulting modified code will be the following, with `cython.declare` codelines:

```
import cython

def stuff(a : int, b : int, c : float = 0.4, d = None) -> int:
    h = cython.declare(cython.float)
    p = cython.declare(cython.int)
    i = cython.declare(cython.int)
    onono = cython.declare(cython.float)
    m = cython.declare(cython.int)
    sum = cython.declare(cython.int)
    sum = 0
    m = 11
    onono = 17.4
    for i in range(4):
        p = 7
        h = float(64) * p
        sum += i
        sum = 5 * 18
    return float(sum)

```

## Installation

Markarth is available on the [PyPI index](https://pypi.org/project/markarth). You can install it using pip:

```
pip install markarth
```

## Internal functioning

It makes heavy usage of the `ast` module in order to parse python code, while leveraging type annotations to infer variable types, thus adding some declarations that with python would speed the code up.

The module's functionality is divided in two main steps:
 - one in which the code parsed with `ast` is analyzed to detect types of variables. Results of elementary operations are used, together with invocations of functions like `len()`.
 - another in which the types collected are converted to cython codelines.

There are additional functionalities to provide conversion options, in order to use `cython.double` instead of `cython.float` as type during conversion.

## Possible improvements

Several possible improvements can be done (apart from testing and discovering bugs, obviously). Among them:

- Store and extrapolate types of containers (lists, dicts, sets, ecc.)
- Identify numpy array and type them as memory views
- Detect `:=` walrus operators
- Possibility of selecting between pure python mode conversion and old style pure cython with `cdef VARNAME int` codelines
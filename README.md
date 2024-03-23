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

At the moment there is no PyPI package, so if someone really (really?) wants to run such thing, the repo should be cloned, to then run the `setup.py` script in the cloning folder 

```
git clone https://github.com/nucccc/markarth
cd markarth
pip install .
```

## Internal functioning

It makes heavy usage of the `ast` module in order to parse python code, while leveraging type annotations to infer variable types, thus adding some declarations that with python would speed the code up.

## Possible improvements

Several possible improvements can be done (apart from testing and discovering bugs, obviously). Among them:

- Store and extrapolate types of containers (lists, dicts, sets, ecc.)
- Identify numpy array and type them as memory views
- Detect `:=` walrus operators
- Possibility of selecting between pure python mode conversion and old style pure cython with `cdef VARNAME int` codelines
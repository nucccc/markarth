# markarth

markarth is a library that would like to automatically add cython cdef to python code, possibly improving its performance transpiling it into cython.

It makes heavy usage of the `ast` module in order to parse python code, while leveraging type annotations to infer variable types, thus adding some declarations that with python would speed the code up.

## Example

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

```
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

## Possible improvements

Several possible improvements can be done (apart from testing and discovering bugs, obviously). Among them:

- Store and extrapolate types of containers (lists, dicts, sets, ecc.)
- Identify numpy array and type them as memory views
- Handle AugAssign like `+=`
- Detect `:=` walrus operators
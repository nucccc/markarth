# markarth

markarth is a library that would like to automatically add cython cdef to python code, possibly improving its performance transpiling it into cython.

It makes heavy usage of the `ast` module in order to parse python code, while leveraging type annotations to infer variable types, thus adding some `cdef` at the beginning of the code.

## Example

```from markarth import convert_func

code = '''
def stuff(a : int, b : int, c : float = 0.4, d = None) -> int:
\tsum = 0
\tfor i in range(4):
\t\tp = 7
\t\th = float(64) * p
\t\tsum += i
\t\tsum = 5 * 18
\treturn sum
'''

cycode = convert_func(code)

print(cycode)
```

```
cpdef int stuff(a : int, b : int, c : float = 0.4, d = None):
	cdef int sum
	cdef int i
	cdef int p
	cdef float h
	sum = 0
	for i in range(4):
		p = 7
		h = float(64) * p
		sum += i
		sum = 5 * 18
	return sum
```

## Installation

At the moment there is no PyPI package, so if someone really (really?) wants to run such thing, the repo should be cloned, to then run the `setup.py` script in the cloning folder 

```
git clone https://github.com/nucccc/markarth
cd markarth
python3 setup.py install
```

## Possible improvements

Several possible improvements can be done (apart from testing and discovering bugs, obviously). Among them:

- Store and extrapolate types of containers (lists, dicts, sets, ecc.)
- Identify numpy array and type them as memory views
- Identify booleans and type them as chars
- Run through an entire module
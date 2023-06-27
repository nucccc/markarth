# markarth

markarth is a library that would like to automatically cdef types to python code, transforming it into cython.

It makes heavy usage of the `ast` module in order to parse python code, while leveraging type annotations to infer variable types, thus adding some `cdef` at the beginning of the code.

## Possible improvements

Several possible improvements can be done (apart from testing and discovering bugs, obviously). Among them:

- Store and extrapolate types of containers (lists, dicts, sets, ecc.)
- Identify numpy array and type them as memory views
- Identify booleans and type them as chars
- Run through an entire module
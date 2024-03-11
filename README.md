# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/nucccc/markarth/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                  |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------------ | -------: | -------: | ------: | --------: |
| markarth/\_\_init\_\_.py                              |        1 |        0 |    100% |           |
| markarth/ast\_utils/\_\_init\_\_.py                   |        1 |        0 |    100% |           |
| markarth/ast\_utils/ast\_utils.py                     |       19 |        0 |    100% |           |
| markarth/convert/\_\_init\_\_.py                      |        0 |        0 |    100% |           |
| markarth/convert/collect/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| markarth/convert/collect/ast\_to\_typ/\_\_init\_\_.py |        0 |        0 |    100% |           |
| markarth/convert/collect/ast\_to\_typ/ast\_assign.py  |       41 |        0 |    100% |           |
| markarth/convert/collect/ast\_to\_typ/ast\_to\_typ.py |       57 |        2 |     96% |    82, 84 |
| markarth/convert/collect/func\_collect.py             |       81 |        2 |     98% |   120-121 |
| markarth/convert/collect/mod\_collect.py              |       69 |        2 |     97% |     92-93 |
| markarth/convert/collect/vartyp\_tracker.py           |       52 |        0 |    100% |           |
| markarth/convert/convert\_pure.py                     |       11 |        0 |    100% |           |
| markarth/convert/cythonize/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| markarth/convert/cythonize/cy\_options.py             |       36 |        1 |     97% |        43 |
| markarth/convert/cythonize/cy\_typs.py                |       28 |        0 |    100% |           |
| markarth/convert/cythonize/pure.py                    |       86 |        0 |    100% |           |
| markarth/convert/preprocess/\_\_init\_\_.py           |        0 |        0 |    100% |           |
| markarth/convert/preprocess/code\_process.py          |       32 |        2 |     94% |     49-50 |
| markarth/convert/typs/\_\_init\_\_.py                 |        0 |        0 |    100% |           |
| markarth/convert/typs/merge\_typs.py                  |       27 |        0 |    100% |           |
| markarth/convert/typs/typ\_store.py                   |       34 |        5 |     85% |52-53, 63, 66, 69 |
| markarth/convert/typs/typs.py                         |       98 |        5 |     95% |41, 60, 98, 185-186 |
| markarth/convert/typs/typs\_parse.py                  |        6 |        0 |    100% |           |
| tests/conftest.py                                     |       71 |        8 |     89% |103, 130, 153, 175, 192-193, 222-223 |
| tests/test\_ast\_assign.py                            |       97 |        0 |    100% |           |
| tests/test\_ast\_to\_typ.py                           |      111 |        0 |    100% |           |
| tests/test\_ast\_utils.py                             |       39 |        0 |    100% |           |
| tests/test\_code\_process.py                          |       27 |        0 |    100% |           |
| tests/test\_convert\_pure.py                          |       32 |        0 |    100% |           |
| tests/test\_cy\_opts.py                               |       22 |        0 |    100% |           |
| tests/test\_cy\_typs.py                               |       10 |        0 |    100% |           |
| tests/test\_cythonize\_pure.py                        |       54 |        0 |    100% |           |
| tests/test\_func\_collect.py                          |       97 |        0 |    100% |           |
| tests/test\_merge\_typs.py                            |      100 |        0 |    100% |           |
| tests/test\_mod\_collect.py                           |       81 |        0 |    100% |           |
| tests/test\_typs.py                                   |      103 |        0 |    100% |           |
| tests/test\_typs\_parse.py                            |       18 |        0 |    100% |           |
| tests/test\_vartyp\_tracker.py                        |      138 |        0 |    100% |           |
|                                             **TOTAL** | **1679** |   **27** | **98%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/nucccc/markarth/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/nucccc/markarth/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/nucccc/markarth/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/nucccc/markarth/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fnucccc%2Fmarkarth%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/nucccc/markarth/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.
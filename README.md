# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/nucccc/markarth/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                  |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------------ | -------: | -------: | ------: | --------: |
| markarth/\_\_init\_\_.py                              |        1 |        0 |    100% |           |
| markarth/convert/\_\_init\_\_.py                      |        0 |        0 |    100% |           |
| markarth/convert/collect/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| markarth/convert/collect/ast\_to\_typ/\_\_init\_\_.py |        0 |        0 |    100% |           |
| markarth/convert/collect/ast\_to\_typ/ast\_to\_typ.py |       56 |        7 |     88% |35, 45, 61, 80, 85, 89, 94 |
| markarth/convert/collect/func\_collect.py             |       81 |       11 |     86% |101-109, 146, 148 |
| markarth/convert/collect/mod\_collect.py              |       62 |        8 |     87% |47-51, 53, 62-63 |
| markarth/convert/convert\_pure.py                     |       11 |        0 |    100% |           |
| markarth/convert/cythonize/\_\_init\_\_.py            |        0 |        0 |    100% |           |
| markarth/convert/cythonize/cy\_options.py             |       29 |        0 |    100% |           |
| markarth/convert/cythonize/cy\_typs.py                |       28 |        5 |     82% |24, 29-30, 37-38 |
| markarth/convert/cythonize/pure.py                    |       86 |        1 |     99% |        72 |
| markarth/convert/preprocess/\_\_init\_\_.py           |        0 |        0 |    100% |           |
| markarth/convert/preprocess/code\_process.py          |       32 |        4 |     88% |49-50, 63, 68 |
| markarth/convert/typs/\_\_init\_\_.py                 |        0 |        0 |    100% |           |
| markarth/convert/typs/merge\_typs.py                  |       27 |        0 |    100% |           |
| markarth/convert/typs/names\_to\_typs.py              |      102 |       32 |     69% |63, 135-136, 148, 152, 156, 160-166, 194-197, 209-215, 219-227 |
| markarth/convert/typs/typs.py                         |       98 |        5 |     95% |41, 60, 98, 185-186 |
| markarth/convert/typs/typs\_parse.py                  |        6 |        0 |    100% |           |
| tests/conftest.py                                     |       43 |        5 |     88% |86, 98-99, 128-129 |
| tests/test\_ast\_to\_typ.py                           |       57 |        0 |    100% |           |
| tests/test\_code\_process.py                          |       14 |        0 |    100% |           |
| tests/test\_convert\_pure.py                          |       24 |        0 |    100% |           |
| tests/test\_cy\_opts.py                               |       22 |        0 |    100% |           |
| tests/test\_cythonize\_pure.py                        |       54 |        0 |    100% |           |
| tests/test\_func\_collect.py                          |       45 |        0 |    100% |           |
| tests/test\_merge\_typs.py                            |      100 |        0 |    100% |           |
| tests/test\_mod\_collect.py                           |       69 |        0 |    100% |           |
| tests/test\_names\_to\_typs.py                        |       89 |        0 |    100% |           |
| tests/test\_typs.py                                   |       96 |        0 |    100% |           |
| tests/test\_typs\_parse.py                            |       18 |        0 |    100% |           |
|                                             **TOTAL** | **1250** |   **78** | **94%** |           |


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
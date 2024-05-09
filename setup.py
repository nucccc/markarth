from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='markarth',
    version='0.0.5',
    author='Domenico Nucera',
    description='Automatic code conversion from python to cython',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://github.com/nucccc/markarth',
    license='MIT License',
    install_requires=[
        'pydantic >= 2.4.2',
        'coverage >= 7.3.2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Code Generators'
    ]
)
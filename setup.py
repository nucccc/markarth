from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='markarth',
    version='0.0.3',
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
    ])
from setuptools import find_packages, setup

setup(
    name='markarth',
    version='0.0.7',
    author='Domenico Nucera',
    packages=find_packages(),
    url='https://github.com/nucccc/markarth',
    license='MIT License',
    description='code conversion from python to cython',
    install_requires=[
        "pydantic >= 2.4.2"
    ])
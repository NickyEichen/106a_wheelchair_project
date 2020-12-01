from distutils.core import setup
from setuptools import find_packages

setup(
    name='wheel_custom_pkg',
    version='0.2',
    packages=find_packages(),
    license='MIT License',
    long_description=open('README.md').read(),
)

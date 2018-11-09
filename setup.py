#!/usr/bin/env python2

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['convert_to_dem'],
    package_dir={'': 'src'},
)

setup(**d)

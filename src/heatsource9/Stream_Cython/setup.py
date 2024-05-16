# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 23:09:53 2024

@author: Kevin.Nebiolo
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("PyHeatsource.pyx")
)

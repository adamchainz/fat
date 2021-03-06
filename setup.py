#!/usr/bin/env python

# Prepare a release:
#
#  - git pull --rebase
#  - run ./runtests.sh
#  - update VERSION in fat.c and setup.py
#  - reset option in setup.py: DEBUG=False
#  - set release date in the changelog of README.rst
#  - git commit -a
#  - git push
#
# Release a new version:
#
#  - git tag VERSION
#  - git push --tags
#  - python3 setup.py register sdist upload
#
# After the release:
#
#  - set version to n+1 in setup.py and fat.c
#  - git commit
#  - git push

from __future__ import with_statement
from distutils.core import setup, Extension
import ctypes
import os
import subprocess
import sys

# Debug pytracemalloc
DEBUG = False

VERSION = '0.3'

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

def main():
    pythonapi = ctypes.cdll.LoadLibrary(None)
    if not hasattr(pythonapi, 'PyFunction_Specialize'):
        print("WARNING: PyFunction_Specialize: missing, %s has not been patched" % sys.executable)
        print("Need Python 3.6 with the PEP 510")
    else:
        print("PyFunction_Specialize: present")

    cflags = []
    if not DEBUG:
        cflags.append('-DNDEBUG')

    with open('README.rst') as f:
        long_description = f.read().strip()

    ext = Extension('fat', ['fat.c'], extra_compile_args = cflags)

    options = {
        'name': 'fat',
        'version': VERSION,
        'license': 'MIT license',
        'description': 'Fast guards used by fatoptimizer to specialize functions',
        'long_description': long_description,
        "url": "https://fatoptimizer.readthedocs.org/en/latest/fat.html",
        'author': 'Victor Stinner',
        'author_email': 'victor.stinner@gmail.com',
        'ext_modules': [ext],
        'classifiers': CLASSIFIERS,
    }
    setup(**options)

if __name__ == "__main__":
    main()

#!/usr/bin/env python
# encoding: utf-8

import os
import sys

__import__('distribute_setup').use_setuptools()

from setuptools import setup, find_packages


if sys.version_info <= (2, 6):
    raise SystemExit("Python 2.6 or later is required.")

exec(open(os.path.join("marrow", "wsgi", "objects", "release.py")))


setup(
        name = 'marrow.wsgi.objects',
        version = release,
        
        description = 'A collection of object-oriented WSGI2 helpers.',
        long_description = '''\
For full documentation, see the README.textile file present in the package,
or view it online on the GitHub project page:

https://github.com/pulp/marrow.wsgi.objects''',
        
        author = 'Alice Bevan-McGregor',
        author_email = 'alice@gothcandy.com',
        url = 'https://github.com/pulp/marrow.wsgi.objects',
        license = 'MIT',
        
        install_requires = ['marrow.util'],
        test_suite = 'nose.collector',
        tests_require = ['nose'],
        
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.1",
            "Programming Language :: Python :: 3.2",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        
        packages = find_packages(exclude=['examples', 'tests']),
        include_package_data = True,
        zip_safe = True,
        
        namespace_packages = ['marrow']
    )

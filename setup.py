# -*- coding: utf-8 -*-
try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup

import sys, os
from setuptools import find_packages
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
from iugu.version import __version__

setup(
  name='iugu-python',
  version= __version__,
  author='Horacio Ibrahim',
  author_email='horacioibrahim@gmail.com',
  packages=find_packages('lib'),
  package_dir={'': 'lib'},
  scripts=[],
  url='https://github.com/horacioibrahim/iugu-python',
  download_url='https://github.com/horacioibrahim/iugu-python/tarball/master',
  license='Apache License',
  description='This package is an idiomatic python lib to work with Iugu service',
  long_description="""
  This iugu-python lib is the more pythonic way to work with webservices of payments
  iugu.com. This provides python objects to each entity of the service as Subscriptions,
  Plans, Customers, Invoices, etc.
  http://iugu.com/referencias/api - API Reference
""",
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  keywords=['iugu', 'rest', 'payment']
)

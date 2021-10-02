#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='indrz',
      version='3.0',
      author='Michael Diener',
      description='indoor maps and directions api',
      license='GNU 3',
      url='https://indrz.com',
      packages=find_packages(),

      scripts=['manage.py'])

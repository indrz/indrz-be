#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='indrz',
      version='2.9',
      author='Michael Diener',
      description='indoor map and routing backend api',
      license='GNU 3',
      url='https://indrz.com',
      packages=find_packages(),

      scripts=['manage.py'])

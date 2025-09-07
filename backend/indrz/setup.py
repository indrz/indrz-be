#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='indrz',
      version='3.0.1',
      author='Michael Diener',
      description='indoor maps, wayfinding and directions api',
      keywords=['indoor', 'gis', 'wayfinding', 'directions',],
      license='GNU 3',
      url='https://indrz.com',
      packages=find_packages(),
      scripts=['manage.py'])

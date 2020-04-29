#!/usr/bin/env python

from setuptools import setup

setup(name='target-jsonl',
      version='0.1.0',
      description='Singer.io target for writing JSON Line files',
      author='Andy Huynh',
      url='https://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['target_jsonl'],
      install_requires=[
          'jsonschema==2.6.0',
          'singer-python==2.1.4',
      ],
      entry_points='''
          [console_scripts]
          target-jsonl=target_jsonl:main
      ''',
)

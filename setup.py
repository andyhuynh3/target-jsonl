#!/usr/bin/env python
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name='target-jsonl',
    version='0.1.4',
    description='Singer.io target for writing JSON Line files',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Andy Huynh',
    author_email="andy.huynh312@gmail.com",
    url="https://github.com/andyh1203/target-jsonl",
    keywords=["singer", "singer.io", "target", "etl"],
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['target_jsonl'],
    install_requires=['jsonschema==2.6.0', 'singer-python==5.8.0', 'adjust-precision-for-schema==0.3.3'],
    entry_points='''
          [console_scripts]
          target-jsonl=target_jsonl:main
      ''',
)

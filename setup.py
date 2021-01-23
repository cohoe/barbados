#!/usr/bin/env python

"""
Barbados cocktail recipe management platform
"""

from setuptools import setup, find_packages

setup(
    name='barbados',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/cohoe/barbados',
    license='LICENSE.txt',
    author='Grant Cohoe',
    author_email='grant@grantcohoe.com',
    description='A cocktail recipe management system',
    long_description=__doc__,
    install_requires=[
        'PyYAML',
        'SQLAlchemy',
        'requests',
        'redis',
        'psycopg2-binary',
        'python-slugify',
        'kazoo',
        'treelib',
        'elasticsearch',
        'elasticsearch_dsl',
        'bs4',
        'sqlalchemy_json_querybuilder'
    ]
)

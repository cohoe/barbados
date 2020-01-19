#!/usr/bin/env python

"""
Barbados cocktail recipe management platform
"""

from setuptools import setup, find_packages

setup(
    name='barbados',
    version='0.0.1',
    packages=find_packages(exclude=['tests', 'scripts']),
    url='https://github.com/cohoe/barbados',
    license='LICENSE.txt',
    author='Grant Cohoe',
    author_email='grant@grantcohoe.com',
    description='A cocktail recipe management system',
    long_description=__doc__,
    install_requires=[
        'jinja2',
        'MarkupSafe',
        'python-editor',
        'pdfkit',
        'wkhtmltopdf',
        'PyYAML'
    ]
)

# -*- coding: utf-8 -*-

from __future__ import absolute_import
from setuptools import setup, find_packages

long_desc = '''
This package contains the slide Sphinx extension.

This extension enable you to embed your slides on slideshare_ and other sites.
Following code is sample::

   .. slide:: https://www.slideshare.net/TakeshiKomiya/blockdiag-a-simple-diagram-generator


.. _slideshare: https://www.slideshare.net/
'''

requires = ['Sphinx>=0.6', 'setuptools']

setup(
    name='sphinxcontrib-slide',
    version='1.0.0',
    url='https://github.com/TYPO3-Documentation/sphinx-contrib-slide',
    license='BSD',
    author='Martin Bless',
    author_email='martin.bless@mbless.de',
    description='Sphinx "slide" extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)

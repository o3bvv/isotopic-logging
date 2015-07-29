# -*- coding: utf-8 -*-

import os

from setuptools import setup


__here__ = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(__here__, 'README.rst')).read()

setup(
    name='isotopic-logging',
    version="1.0.1",
    description='Mark and trace events in your log alike isotopic labeling',
    long_description=README,
    keywords=[
        'library', 'logging',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url='https://github.com/oblalex/isotopic-logging',
    author='Alexander Oblovatniy',
    author_email='oblovatniy@gmail.com',
    license='LGPLv3',
    packages=[
        'isotopic_logging',
    ],
    scripts=[
    ],
    platforms=[
        'any',
    ],
    include_package_data=False,
    install_requires=[
    ],
    zip_safe=False,
)

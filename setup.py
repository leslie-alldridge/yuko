"""
yuko
------------
Small and fast validation library
"""

from setuptools import setup

import yuko

setup(
    name='yuko',
    version=yuko.__version__,
    url='https://github.com/5onic/yuko',
    license=yuko.__license__,
    author=yuko.__author__,
    author_email='mikeiceman1221@gmail.com',
    description='Small and fast validation library',
    long_description=__doc__,
    packages=['yuko'],
    # platforms=,
    install_requires=['orjson==2.0.6'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]

)

__author__ = 'mariusmagureanu'
from setuptools import setup, find_packages
import sys

if sys.version_info < (2, 7):
    sys.exit('VAC requires at least Python 2.7, please upgrade and try again.')

version = '1.0'

twisted_version = 'Twisted==13.2.0',

setup_requires = []

install_requires = [
    twisted_version,
    'nose',
    'flask',
    'Fabric>=1.8.0',
    'colorama',
    'lxml==3.0.1',
    'pyasn1',
    'pyOpenSSL',
    'Mako',
    'unittest2',
    # Version 2.0.0 of pyparsing seems to have dropped python 2 compatibility:
    'pyparsing<2.0.0',
    'mock>=0.7',
    'ipaddr>=2.1, <2.2',
    'docopt==0.5.0',
    'coverage==3.5.1',
    'carnifex==0.2.4',
    'txAMQP',
    'pep8>=1.4.6',
    'netifaces',
    'crochet>=1.0.0',
    'mongoengine',
    'ipython'
]


setup(
    name='VAC',
    version=version,
    description='vac',
    long_description='',
    # Get strings for classifiers from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers:
    classifiers=[],
    keywords='',
    author='Marius Magureanu',
    author_email='marius.developer@gmail.com',
    url='www.google.com',
    license='Some license',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    setup_requires=setup_requires,
    entry_points={
        'console_scripts': ['vac = vac.shell.vac_shell:main']},
    scripts=[])

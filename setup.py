from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='Mopidy-LCD',
    version=get_version('mopidy_lcd/__init__.py'),
    url='https://github.com/sheuvi21/mopidy-lcd',
    license='GPLv3',
    author='Evgeniy Shabanov',
    author_email='sheuvi21@gmail.com',
    description='LCD for Mopidy',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 1.0',
        'Pykka >= 1.1',
        'smbus >= 1.1',
        'pimoroni_bme280 >= 0.0.1',
    ],
    dependency_links=[
        'https://github.com/sheuvi21/bme280-python/releases/download/v0.0.1-fixed/pimoroni-bme280-0.0.1.tar.gz#egg=pimoroni_bme280-0.0.1'
    ],
    entry_points={
        'mopidy.ext': [
            'lcd = mopidy_lcd:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)

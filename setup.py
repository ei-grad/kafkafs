#!/usr/bin/env python

from setuptools import setup
import sys


install_requires = [
    'click',
    'fusepy',
    'protobuf (>=3.0.0b3)',
    'pykafka',
    'python-snappy',
    'six',
]

if sys.version_info.major < 3:
    install_requires.append("futures")


setup(
    name="KafkaFS",
    version="0.0.0",
    packages=['kafkafs'],
    entry_points={
        'console_scripts': [
            'kafkafs = kafkafs.cli:main',
        ],
    },
    install_requires=install_requires,
)

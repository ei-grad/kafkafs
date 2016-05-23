#!/usr/bin/env python

from setuptools import setup


setup(
    name="KafkaFS",
    version="0.0.0",
    packages=['kafkafs'],
    entry_points={
        'console_scripts': [
            'kafkafs = kafkafs.cli:main',
        ],
    },
    install_requires=[
        'pykafka',
        'click',
        'fusepy',
        'protobuf (>=3.0.0b3)',
    ],
)

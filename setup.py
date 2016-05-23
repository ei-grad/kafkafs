#!/usr/bin/env python

from setuptools import setup


setup(
    name="KafkaFS",
    version="0.0.0",
    py_modules=["kafkafs", "kafkafs_pb2"],
    entry_points={
        'console_scripts': [
            'kafkafs = kafkafs:main',
        ],
    },
    install_requires=[
        'pykafka',
        'click',
        'fusepy',
        'protobuf (>=3.0.0b3)',
    ],
)

#!/suer/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from setuptools import setup

setup(
    name='samples-python-flask',
    version='0.1.0',
    url='https://developer.okta.com',
    project_urls=OrderedDict((
        ('Code', 'https://github.com/okta/samples-python-flask'),
        ('Documentation', 'https://github.com/okta/samples-python-flask/blob/master/README.md'),
        ('Issue Tracker', 'https://github.com/okta/okta-python-flask/issues'),
    )),
    license='Apache-2.0',
    python_requires='>2.7,'
)
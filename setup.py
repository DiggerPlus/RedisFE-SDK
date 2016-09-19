# -*- coding: utf-8 -*-

import re
import os
from setuptools import setup, find_packages


def _get_version():
    v_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'redis_sdk', '__init__.py')
    ver_info_str = re.compile(r".*version_info = \((.*?)\)", re.S). \
        match(open(v_file_path).read()).group(1)
    return re.sub(r'(\'|"|\s+)', '', ver_info_str).replace(',', '.')

setup(
    name='dpq',
    version=_get_version(),
    url='https://github.com/DiggerPlus/RedisFE-SDK',
    license='MIT',
    author='DiggerPlus',
    author_email='diggerplus@163.com',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any'
)

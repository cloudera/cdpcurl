# Copyright (c) 2020, Cloudera, Inc. All Rights Reserved.
#
# This file is part of cdpcurl.
#
# cdpcurl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cdpcurl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with cdpcurl.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import find_packages
from setuptools import setup
import versioneer

setup(
    name='cdpcurl',
    version=versioneer.get_version(),
    description='Curl like tool with CDP request signing',
    url='https://cloudera.us-west-1.cdp.cloudera.com/',
    author='Cloudera, Inc.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    python_requires=">=3.5",
    entry_points={
        'console_scripts': [
            'cdpcurl = cdpcurl.__main__:main',
            'cdpv1sign = cdpcurl.cdpv1sign:main'
        ],
    },
    zip_safe=False,
    install_requires=[
        'configargparse',
        'configparser',
        'pure25519',
        'requests',
        'urllib3[secure]'
    ],
    cmdclass=versioneer.get_cmdclass()
)

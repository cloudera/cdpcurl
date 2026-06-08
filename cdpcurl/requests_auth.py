#!/usr/bin/env python

# Copyright 2026 Cloudera, Inc.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Requests auth implementation for the CDP API signature specification, v1
"""
import os
import datetime
from email.utils import formatdate

from cdpcurl.cdpv1sign import make_signature_header
from cdpcurl.cdpconfig import load_cdp_config


def __now():
    return datetime.datetime.now(datetime.timezone.utc)


def auth_v1(access_key=os.getenv('CDP_ACCESS_KEY_ID'),
            private_key=os.getenv('CDP_PRIVATE_KEY'),
            profile=os.getenv('CDP_PROFILE') or 'default'):
    """
    Returns requests auth object for CDP API V1

    :return: requests auth object
    :param access_key: str
    :param private_key: str
    :param profile: str
    """

    credentials_path = os.path.expanduser("~") + "/.cdp/credentials"
    access_key, private_key = load_cdp_config(access_key,
                                              private_key,
                                              credentials_path,
                                              profile)

    def _sign_request(req):
        """ Appends auth headers to request """

        req.headers['X-Altus-Date'] = \
                formatdate(timeval=__now().timestamp(), usegmt=True)

        req.headers['X-Altus-Auth'] = make_signature_header(req.method,
                                                            str(req.url),
                                                            req.headers,
                                                            access_key,
                                                            private_key)

        return req

    return _sign_request

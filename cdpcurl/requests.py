#!/usr/bin/env python

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

"""
Requests auth implementation for the CDP API signature specification, v1
"""
import os
import datetime
from email.utils import formatdate

from cdpcurl.cdpv1sign import make_signature_header
from cdpcurl.cdpconfig import load_cdp_config


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

        now = datetime.datetime.now(datetime.timezone.utc)

        req.headers['X-Altus-Date'] = \
                formatdate(timeval=now.timestamp(), usegmt=True)

        req.headers['X-Altus-Auth'] = make_signature_header(req.method,
                                                            req.url,
                                                            req.headers,
                                                            access_key,
                                                            private_key)

        return req

    return _sign_request

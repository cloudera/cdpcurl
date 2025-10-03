# -*- coding: utf-8 -*-

# Copyright 2025 Cloudera, Inc.  All rights reserved.
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
cdp profile support
"""

import configparser
import os

from typing import Tuple


def load_cdp_config(
    access_key,
    private_key,
    credentials_path,
    profile,
) -> Tuple[str, str]:
    """
    Load CDP credential configuration, by parsing credential file, by checking
    (access_key,private_key) are not (None,None)
    """
    if access_key is None or private_key is None:
        exists = os.path.exists(credentials_path)
        if not exists:
            msg = "Credentials file '{0}' does not exist"
            raise Exception(msg.format(credentials_path))

        config = configparser.ConfigParser()
        config.read(credentials_path)

        if not config.has_section(profile):
            raise Exception("CDP profile '{0}' not found".format(profile))

        if access_key is None:
            if config.has_option(profile, "cdp_access_key_id"):
                access_key = config.get(profile, "cdp_access_key_id")
            else:
                msg = "CDP profile '{0}' is missing 'cdp_access_key_id'"
                raise Exception(msg.format(profile))

        if private_key is None:
            if config.has_option(profile, "cdp_private_key"):
                private_key = config.get(profile, "cdp_private_key")
            else:
                msg = "CDP profile '{0}' is missing 'cdp_private_key'"
                raise Exception(msg.format(profile))

    return access_key, private_key

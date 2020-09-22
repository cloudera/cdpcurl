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
cdp profile support
"""

import os

import configparser


def load_cdp_config(access_key, private_key, credentials_path, profile):
    # type: (str, str, str, str) -> Tuple[str, str]
    """
    Load CDP credential configuration, by parsing credential file, by checking
    (access_key,private_key) are not (None,None)
    """
    if access_key is None or private_key is None:
        exists = os.path.exists(credentials_path)
        if not exists:
            msg = 'Credentials file \'{0}\' does not exist'
            raise Exception(msg.format(credentials_path))

        config = configparser.ConfigParser()
        config.read(credentials_path)

        if not config.has_section(profile):
            raise Exception('CDP profile \'{0}\' not found'.format(profile))

        if access_key is None:
            if config.has_option(profile, "cdp_access_key_id"):
                access_key = config.get(profile, "cdp_access_key_id")
            else:
                msg = 'CDP profile \'{0}\' is missing \'cdp_access_key_id\''
                raise Exception(msg.format(profile))

        if private_key is None:
            if config.has_option(profile, "cdp_private_key"):
                private_key = config.get(profile, "cdp_private_key")
            else:
                msg = 'CDP profile \'{0}\' is missing \'cdp_private_key\''
                raise Exception(msg.format(profile))

    return access_key, private_key

#!/usr/bin/env python
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

from cdpcurl.cdpconfig import load_cdp_config


def test_load_cdp_credentials_default_profile():
    access_key, private_key = load_cdp_config(
        None,
        None,
        "tests/data/credentials",
        "default",
    )

    assert [access_key, private_key] == ["default_access_key", "default_private_key"]


def test_load_cdp_credentials_custom_profile():
    access_key, private_key = load_cdp_config(
        None,
        None,
        "tests/data/credentials",
        "custom_profile",
    )

    assert [access_key, private_key] == [
        "custom_profile_access_key",
        "custom_profile_private_key",
    ]

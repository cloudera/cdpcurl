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

from unittest import TestCase

from cdpcurl.cdpconfig import load_cdp_config

__author__ = "cloudera"


class Test__load_cdp_config(TestCase):
    def test(self):
        access_key, private_key = load_cdp_config(
            None,
            None,
            "./tests/data/credentials",
            "default",
        )

        self.assertEqual([access_key, private_key], ["access_key_id", "private_key"])

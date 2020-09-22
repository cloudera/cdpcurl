#!/usr/bin/env python


from unittest import TestCase

from cdpcurl.cdpconfig import load_cdp_config

__author__ = 'cloudera'


class Test__load_cdp_config(TestCase):
    def test(self):
        access_key, private_key = load_cdp_config(None,
                                                  None,
                                                  "./tests/data/credentials",
                                                  "default")

        self.assertEqual([access_key, private_key], ['access_key_id', 'private_key'])

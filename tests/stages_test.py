#!/usr/bin/env python
"""
Test cases for separate signature header calculation stages.
"""

from unittest import TestCase

__author__ = 'cloudera'

from cdpcurl.cdpv1sign import (
    create_canonical_request_string,
    create_signature_string,
    create_encoded_authn_params_string,
    create_signature_header)

class TestStages(TestCase):
    """
    Suite to test all stages.
    """
    maxDiff = None

    def test_create_canonical_request_string(self):
        """
        Test the function to create the "canonical" request string.
        """
        uri = 'https://cdpapitest.cloudera.com/api/v1/test/doTestThing'
        headers = {'content-type': 'application/json',
                   'x-altus-date': 'Tue, 3 Jun 2008 11:05:30 GMT'}
        canonical_request_string = create_canonical_request_string(
            'POST',
            uri,
            headers,
            'ed25519v1')
        self.assertEqual(canonical_request_string, "POST\n"
                         "application/json\n"
                         "Tue, 3 Jun 2008 11:05:30 GMT\n"
                         "/api/v1/test/doTestThing\n"
                         "ed25519v1")

    def test_create_signature_string(self):
        """
        Test the function to sign and encode the canonical request string.
        """
        canonical_request_string = "POST\n"\
            "application/json\n"\
            "Tue, 3 Jun 2008 11:05:30 GMT\n"\
            "/api/v1/test/doTestThing\n"\
            "x-amz-date:20190921T022008Z\n"\
            "ed25519v1"
        private_key = 'Mzjg58S93/qdg0HuVP6PsLSRDTe+fQZ5++v/mkUUx4k='
        signature_string = create_signature_string(
            canonical_request_string,
            private_key)
        self.assertEqual(signature_string,
                         'MujQ0wGS6CADCcidsqPvJ9_ETbK_RFUq9DQj3dcLPtj43xC46wjprhPQ_J3o9qFK8k1rhU3lOt7WbRSjCrGvDA==')


    def test_create_encoded_authn_params_string(self):
        """
        Test the function to create the encoded authentication parameters
        string.
        """
        access_key = 'ABC';
        auth_method = 'ed25519v1'
        encoded_auth_params_string = create_encoded_authn_params_string(
            access_key,
            auth_method)
        self.assertEqual(encoded_auth_params_string,
                         b'eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ==')

    def test_create_signature_header(self):
        """
        Test the function that generates the signature header value.
        """
        encoded_auth_params_string = b'eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ=='
        signature = 'MujQ0wGS6CADCcidsqPvJ9_ETbK_RFUq9DQj3dcLPtj43xC46wjprhPQ_J3o9qFK8k1rhU3lOt7WbRSjCrGvDA=='
        signature_header = create_signature_header(
            encoded_auth_params_string,
            signature)
        self.assertEqual(signature_header,
                         'eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ==.MujQ0wGS6CADCcidsqPvJ9_ETbK_RFUq9DQj3dcLPtj43xC46wjprhPQ_J3o9qFK8k1rhU3lOt7WbRSjCrGvDA==')

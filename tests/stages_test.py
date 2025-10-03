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

"""
Test cases for separate signature header calculation stages.
"""

from cdpcurl.cdpv1sign import (
    create_canonical_request_string,
    create_signature_string,
    create_encoded_authn_params_string,
    create_signature_header,
)


def test_create_canonical_request_string():
    """
    Test the function to create the "canonical" request string.
    """

    uri = "https://cdpapitest.cloudera.com/api/v1/test/doTestThing"
    headers = {
        "content-type": "application/json",
        "x-altus-date": "Tue, 3 Jun 2008 11:05:30 GMT",
    }

    canonical_request_string = create_canonical_request_string(
        "POST",
        uri,
        headers,
        "ed25519v1",
    )

    expected = "\n".join(
        [
            "POST",
            "application/json",
            "Tue, 3 Jun 2008 11:05:30 GMT",
            "/api/v1/test/doTestThing",
            "ed25519v1",
        ],
    )

    assert canonical_request_string == expected


def test_create_signature_string():
    """
    Test the function to sign and encode the canonical request string.
    """

    canonical_request_string = (
        "POST\n"
        "application/json\n"
        "Tue, 3 Jun 2008 11:05:30 GMT\n"
        "/api/v1/test/doTestThing\n"
        "x-amz-date:20190921T022008Z\n"
        "ed25519v1"
    )
    private_key = "Mzjg58S93/qdg0HuVP6PsLSRDTe+fQZ5++v/mkUUx4k="

    signature_string = create_signature_string(
        canonical_request_string,
        private_key,
    )

    assert (
        signature_string
        == "MujQ0wGS6CADCcidsqPvJ9_ETbK_RFUq9DQj3dcLPtj43xC46wjprhPQ_J3o9qFK8k1rhU3lOt7WbRSjCrGvDA=="
    )


def test_create_encoded_authn_params_string():
    """
    Test the function to create the encoded authentication parameters
    string.
    """

    access_key = "ABC"
    auth_method = "ed25519v1"

    encoded_auth_params_string = create_encoded_authn_params_string(
        access_key,
        auth_method,
    )

    assert (
        encoded_auth_params_string
        == b"eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ=="
    )


def test_create_signature_header():
    """
    Test the function that generates the signature header value.
    """

    encoded_auth_params_string = (
        b"eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ=="
    )
    signature = "MujQ0wGS6CADCcidsqPvJ9_ETbK_RFUq9DQj3dcLPtj43xC46wjprhPQ_J3o9qFK8k1rhU3lOt7WbRSjCrGvDA=="

    signature_header = create_signature_header(
        encoded_auth_params_string,
        signature,
    )

    assert (
        signature_header
        == "eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ==.MujQ0wGS6CADCcidsqPvJ9_ETbK_RFUq9DQj3dcLPtj43xC46wjprhPQ_J3o9qFK8k1rhU3lOt7WbRSjCrGvDA=="
    )

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

import datetime
from unittest.mock import MagicMock, Mock

import pytest

from requests import Response

from cdpcurl.cdpcurl import make_request


@pytest.fixture(autouse=True)
def mock_utc(mocker):
    mocker.patch(
        "cdpcurl.cdpcurl.__now",
        return_value=datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc),
    )


@pytest.fixture()
def cdp_request(mocker) -> MagicMock:
    return mocker.patch("cdpcurl.cdpcurl.requests.request")


@pytest.fixture(autouse=True)
def cdp_response(cdp_request, mocker) -> Mock:
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.text = "some text"
    cdp_request.return_value = mock_response
    return mock_response


def test_make_request(cdp_request):
    params = {
        "method": "GET",
        "uri": "https://user:pass@host:123/path/?a=b&c=d",
        "headers": {
            "content-type": "application/json",
        },
        "data": "",
        "access_key": "ABC",
        "private_key": "Mzjg58S93/qdg0HuVP6PsLSRDTe+fQZ5++v/mkUUx4k=",
        "data_binary": False,
    }

    expected = {
        "content-type": "application/json",
        "x-altus-date": "Thu, 01 Jan 1970 00:00:00 GMT",
        "x-altus-auth": "eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ==.bej2viXTt1s2fhCwl65y10TiOdduxAyCRm1APvVj1qhTYzaTn3L-4xnlCj_UeTt_nFFUHa0rj03RPdzwBjvQCQ==",
    }

    make_request(**params)

    cdp_request.assert_called_once_with(
        params["method"],
        params["uri"],
        headers=expected,
        data=params["data"].encode("utf-8"),
        verify=True,
    )


def test_make_request_invalid_date_header():
    params = {
        "method": "GET",
        "uri": "https://user:pass@host:123/path/?a=b&c=d",
        "headers": {
            "content-type": "application/json",
            "x-altus-date": "Thu, 01 Jan 1970 00:00:00 GMT",
        },
        "data": "",
        "access_key": "ABC",
        "private_key": "NOPE",
        "data_binary": False,
        "verify": False,
    }

    with pytest.raises(
        Exception,
        match="Malformed request: x-altus-date found in headers",
    ):
        make_request(**params)


def test_make_request_invalid_auth_header():
    params = {
        "method": "GET",
        "uri": "https://user:pass@host:123/path/?a=b&c=d",
        "headers": {
            "content-type": "application/json",
            "x-altus-auth": "eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ==.bej2viXTt1s2fhCwl65y10TiOdduxAyCRm1APvVj1qhTYzaTn3L-4xnlCj_UeTt_nFFUHa0rj03RPdzwBjvQCQ==",
        },
        "data": "",
        "access_key": "ABC",
        "private_key": "NOPE",
        "data_binary": False,
        "verify": False,
    }

    with pytest.raises(
        Exception,
        match="Malformed request: x-altus-auth found in headers",
    ):
        make_request(**params)


def test_make_request_invalid_private_key():
    params = {
        "method": "GET",
        "uri": "https://user:pass@host:123/path/?a=b&c=d",
        "headers": {
            "content-type": "application/json",
        },
        "data": "",
        "access_key": "ABC",
        "private_key": "NOPE",
        "data_binary": False,
        "verify": False,
    }

    with pytest.raises(Exception, match="Only ed25519v1 keys are supported"):
        make_request(**params)


def test_make_request_verify_ssl(cdp_request):
    params = {
        "method": "GET",
        "uri": "https://user:pass@host:123/path/?a=b&c=d",
        "headers": {
            "content-type": "application/json",
        },
        "data": "",
        "access_key": "ABC",
        "private_key": "Mzjg58S93/qdg0HuVP6PsLSRDTe+fQZ5++v/mkUUx4k=",
        "data_binary": False,
        "verify": True,
    }

    expected = {
        "content-type": "application/json",
        "x-altus-date": "Thu, 01 Jan 1970 00:00:00 GMT",
        "x-altus-auth": "eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ==.bej2viXTt1s2fhCwl65y10TiOdduxAyCRm1APvVj1qhTYzaTn3L-4xnlCj_UeTt_nFFUHa0rj03RPdzwBjvQCQ==",
    }

    make_request(**params)

    cdp_request.assert_called_with(
        params["method"],
        params["uri"],
        headers=expected,
        data=params["data"].encode("utf-8"),
        verify=params["verify"],
    )


def test_make_request_with_binary_data(cdp_request):
    params = {
        "method": "GET",
        "uri": "https://user:pass@host:123/path/?a=b&c=d",
        "headers": {
            "content-type": "application/json",
        },
        "data": b"C\xcfI\x91\xc1\xd0\tw<\xa8\x13\x06{=\x9b\xb3\x1c\xfcl\xfe\xb9\xb18zS\xf4%i*Q\xc9v",
        "access_key": "ABC",
        "private_key": "Mzjg58S93/qdg0HuVP6PsLSRDTe+fQZ5++v/mkUUx4k=",
        "data_binary": True,
    }

    expected = {
        "content-type": "application/json",
        "x-altus-date": "Thu, 01 Jan 1970 00:00:00 GMT",
        "x-altus-auth": "eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ==.bej2viXTt1s2fhCwl65y10TiOdduxAyCRm1APvVj1qhTYzaTn3L-4xnlCj_UeTt_nFFUHa0rj03RPdzwBjvQCQ==",
    }

    make_request(**params)

    cdp_request.assert_called_with(
        params["method"],
        params["uri"],
        headers=expected,
        data=params["data"],
        verify=True,
    )


def test_make_request_additional_header(cdp_request):
    params = {
        "method": "GET",
        "uri": "https://user:pass@host:123/path/?a=b&c=d",
        "headers": {
            "host": "some.other.host.address.com",
            "content-type": "application/json",
        },
        "data": "",
        "access_key": "ABC",
        "private_key": "Mzjg58S93/qdg0HuVP6PsLSRDTe+fQZ5++v/mkUUx4k=",
        "data_binary": False,
    }

    expected = {
        "host": "some.other.host.address.com",
        "content-type": "application/json",
        "x-altus-date": "Thu, 01 Jan 1970 00:00:00 GMT",
        "x-altus-auth": "eyJhY2Nlc3Nfa2V5X2lkIjogIkFCQyIsICJhdXRoX21ldGhvZCI6ICJlZDI1NTE5djEifQ==.bej2viXTt1s2fhCwl65y10TiOdduxAyCRm1APvVj1qhTYzaTn3L-4xnlCj_UeTt_nFFUHa0rj03RPdzwBjvQCQ==",
    }

    make_request(**params)

    cdp_request.assert_called_with(
        params["method"],
        params["uri"],
        headers=expected,
        data=params["data"].encode("utf-8"),
        verify=True,
    )

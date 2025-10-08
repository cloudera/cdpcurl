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
Implementation of the CDP API signature specification, V1
"""

import json
import os
import sys

import configargparse

from base64 import b64decode, urlsafe_b64encode
from collections import OrderedDict
from cryptography.hazmat.primitives.asymmetric import ed25519
from email.utils import formatdate
from urllib.parse import urlparse

from cdpcurl.cdpconfig import load_cdp_config


def create_canonical_request_string(
    method,
    uri,
    headers,
    auth_method,
):
    """
    Create a canonical request string from aspects of the request.
    """
    headers_of_interest = []
    for header_name in ["content-type", "x-altus-date"]:
        found = False
        for key in headers:
            key_lc = key.lower()
            if headers[key] is not None and key_lc == header_name:
                headers_of_interest.append(headers[key].strip())
                found = True
        if not found:
            headers_of_interest.append("")

    # Our signature verification with treat a query with no = as part of the
    # path, so we do as well. It appears to be a behavior left to the server
    # implementation, and python and our java servlet implementation disagree.
    uri_components = urlparse(uri)
    path = uri_components.path
    if not path:
        path = "/"
    if uri_components.query:
        path += "?" + uri_components.query

    canonical_string = method.upper() + "\n"
    canonical_string += "\n".join(headers_of_interest) + "\n"
    canonical_string += path + "\n"
    canonical_string += auth_method

    return canonical_string


def create_signature_string(
    canonical_string,
    private_key,
):
    """
    Create the string form of the digital signature of the canonical request
    string.
    """
    seed = b64decode(private_key)
    if len(seed) != 32:
        raise Exception("Not an Ed25519 private key!")
    parsed_private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)

    signature = parsed_private_key.sign(
        canonical_string.encode("utf-8"),
    )
    return urlsafe_b64encode(signature).strip().decode("utf-8")


def create_encoded_authn_params_string(
    access_key,
    auth_method,
):
    """
    Create the base 64 encoded string of authentication parameters.
    """
    auth_params = OrderedDict()
    auth_params["access_key_id"] = access_key
    auth_params["auth_method"] = auth_method
    encoded_json = json.dumps(auth_params).encode("utf-8")
    return urlsafe_b64encode(encoded_json).strip()


def create_signature_header(
    encoded_authn_params,
    signature,
):
    """
    Combine the encoded authentication parameters string and signature string
    into the signature header value.
    """
    return "%s.%s" % (encoded_authn_params.decode("utf-8"), signature)


def make_signature_header(
    method,
    uri,
    headers,
    access_key,
    private_key,
):
    """
    Generates the value to be used for the x-altus-auth header in the service
    call.
    """
    if len(private_key) != 44:
        raise Exception("Only ed25519v1 keys are supported!")

    auth_method = "ed25519v1"

    canonical_string = create_canonical_request_string(
        method,
        uri,
        headers,
        auth_method,
    )
    signature = create_signature_string(canonical_string, private_key)
    encoded_authn_params = create_encoded_authn_params_string(
        access_key,
        auth_method,
    )
    signature_header = create_signature_header(encoded_authn_params, signature)
    return signature_header


def inner_main(argv):
    """
    cdpv1sign main entry point
    """
    parser = configargparse.ArgumentParser(
        description="Curl with CDP request signing",
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-X",
        "--request",
        help="Specify request command to use",
        default="GET",
    )
    parser.add_argument(
        "--profile",
        help="CDP profile",
        default="default",
        env_var="CDP_PROFILE",
    )
    parser.add_argument("--access_key", env_var="CDP_ACCESS_KEY_ID")
    parser.add_argument("--private_key", env_var="CDP_PRIVATE_KEY")
    # date???

    parser.add_argument("uri")

    args = parser.parse_args(argv)

    credentials_path = os.path.expanduser("~") + "/.cdp/credentials"
    args.access_key, args.private_key = load_cdp_config(
        args.access_key,
        args.private_key,
        credentials_path,
        args.profile,
    )

    if args.access_key is None:
        raise ValueError("No access key is available")

    if args.private_key is None:
        raise ValueError("No private key is available")

    headers = {"Content-Type": "application/json"}
    headers["x-altus-date"] = formatdate(usegmt=True)
    headers["x-altus-auth"] = make_signature_header(
        args.request,
        args.uri,
        headers,
        args.access_key,
        args.private_key,
    )

    for header_key, header_value in headers.items():
        print("{}: {}".format(header_key, header_value))

    return 0


def main():
    """
    main method
    """
    inner_main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())

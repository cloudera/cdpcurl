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
cdpcurl implementation
"""

import datetime
import os
import pprint
import sys

import configargparse
import requests

from email.utils import formatdate

from cdpcurl.cdpv1sign import make_signature_header
from cdpcurl.cdpconfig import load_cdp_config

__author__ = "cloudera"

IS_VERBOSE = False


def __log(*args, **kwargs):
    if not IS_VERBOSE:
        return
    stderr_pp = pprint.PrettyPrinter(stream=sys.stderr)
    stderr_pp.pprint(*args, **kwargs)


def __now():
    return datetime.datetime.now(datetime.timezone.utc)


def make_request(
    method,
    uri,
    headers,
    data,
    access_key,
    private_key,
    data_binary,
    verify=True,
):
    """
    Make HTTP request with CDP request signing

    :return: http request object
    :param method: str
    :param uri: str
    :param headers: dict
    :param data: str
    :param profile: str
    :param access_key: str
    :param private_key: str
    :param data_binary: bool
    :param verify: bool
    """

    if "x-altus-auth" in headers:
        raise Exception("Malformed request: x-altus-auth found in headers")
    
    if "x-altus-date" in headers:
        raise Exception("Malformed request: x-altus-date found in headers")
    
    headers["x-altus-date"] = formatdate(
        timeval=__now().timestamp(),
        usegmt=True,
    )

    headers["x-altus-auth"] = make_signature_header(
        method,
        uri,
        headers,
        access_key,
        private_key,
    )

    if data_binary:
        return __send_request(uri, data, headers, method, verify)
    
    return __send_request(uri, data.encode("utf-8"), headers, method, verify)


def __send_request(uri, data, headers, method, verify):
    __log("\nHEADERS++++++++++++++++++++++++++++++++++++")
    __log(headers)

    __log("\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++")
    __log("Request URL = " + uri)

    response = requests.request(
        method,
        uri,
        headers=headers,
        data=data,
        verify=verify,
    )

    __log("\nRESPONSE++++++++++++++++++++++++++++++++++++")
    __log("Response code: %d\n" % response.status_code)

    return response


def inner_main(argv):
    """
    cdpcurl CLI main entry point
    """
    default_headers = ["Content-Type: application/json"]

    parser = configargparse.ArgumentParser(
        description="curl with CDP request signing",
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="verbose flag",
        default=False,
    )
    parser.add_argument(
        "-i",
        "--include",
        action="store_true",
        help="include headers in the output",
        default=False,
    )
    parser.add_argument(
        "-f",
        "--output-format",
        help="output format",
        choices=["string", "bytes-literal"],
        default="bytes-literal",
    )
    parser.add_argument(
        "-X",
        "--request",
        help="Specify request command to use",
        default="GET",
    )
    parser.add_argument("-d", "--data", help="HTTP POST data", default="")
    parser.add_argument("-H", "--header", help="HTTP header", action="append")
    parser.add_argument(
        "-k",
        "--insecure",
        action="store_false",
        help="This option allows cdpcurl to proceed and "
        "operate even for server connections otherwise "
        "considered insecure",
    )
    parser.add_argument(
        "--data-binary",
        action="store_true",
        help="Process HTTP POST data exactly as specified "
        "with no extra processing whatsoever.",
        default=False,
    )
    parser.add_argument(
        "--profile",
        help="CDP profile",
        default="default",
        env_var="CDP_PROFILE",
    )
    parser.add_argument("--access_key", env_var="CDP_ACCESS_KEY_ID")
    parser.add_argument("--private_key", env_var="CDP_PRIVATE_KEY")

    parser.add_argument("uri")

    args = parser.parse_args(argv)
    # pylint: disable=global-statement
    global IS_VERBOSE
    IS_VERBOSE = args.verbose

    if args.verbose:
        __log(vars(args))

    data = args.data

    if data is not None and data.startswith("@"):
        filename = data[1:]
        with open(filename, "r") as post_data_file:
            data = post_data_file.read()

    if args.header is None:
        args.header = default_headers

    # pylint: disable=unnecessary-comprehension
    headers = {k: v for (k, v) in map(lambda s: s.split(": "), args.header)}

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

    response = make_request(
        args.request,
        args.uri,
        headers,
        data,
        args.access_key,
        args.private_key,
        args.data_binary,
        args.insecure,
    )

    if args.include or IS_VERBOSE:
        print(response.headers, end="\n\n")
    if args.output_format == "bytes-literal":
        print(response.text.encode("utf-8"))
    else:
        print(response.text)

    response.raise_for_status()

    return 0


def main():
    """
    main method
    """
    inner_main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())

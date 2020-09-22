# cdpcurl

Curl like tool with CDP request signing. Inspired by and built from [awscurl](https://github.com/okigan/awscurl). See that repository's [README](https://github.com/okigan/awscurl/tree/master/README.md) for installation and usage instructions beyond what is provided here.

## Building

Create a virtualenv if desired.

```bash
# For typical virtualenv
$ virtualenv cdpcurlenv
$ . cdpcurlenv/bin/activate
# For pyenv
$ pyenv virtualenv cdpcurlenv
$ pyenv activate cdpcurlenv
```

Then, in this directory:

```
$ pip install .
```

## Usage

Run `cdpcurl --help` for a complete list of options.

Before using `cdpcurl`, generate an access key / private key pair for your CDP user account using the CDP management console. You have two options for passing those keys to `cdpcurl`:

* pass the keys to `cdpcurl` using the `--access-key` and `--private-key` options
* (recommended) create a profile in _$HOME/.cdp/credentials_ containing the keys, and then use the `--profile` option in `cdpcurl` calls

```
[myuserprofile]
cdp_access_key_id = 6744f22e-c46a-406d-ad28-987584f45351
cdp_private_key = abcdefgh...................................=
```

Most CDP API calls are POST requests, so be sure to specify `-X POST`, and provide the request content using the `-d` option. If the `-d` option value begins with "@", then the remainder of the value is the path to a file containing the content; otherwise, the value is the content itself.

To form the URI, start by determining the hostname based on the service being called:

* iam: `iamapi.us-west-1.altus.cloudera.com`
* all other services: `api.us-west-1.cdp.cloudera.com`

The correct URI is an https URL at the chosen host, with a path indicated for your desired endpoint in the [API documentation](https://cloudera.github.io/cdp-dev-docs/api-docs/).

## Examples

Get your own account information:

```bash
$ cdpcurl --profile demo -X POST -d '{}' https://iamapi.us-west-1.altus.cloudera.com/iam/getAccount
```

List all environments:

```bash
$ cdpcurl --profile sandbox -X POST -d '{}' https://api.us-west-1.cdp.cloudera.com/api/v1/environments2/listEnvironments
```

## Request Signing

A CDP API call requires a request signature to be passed in the "x-altus-auth" header, along with a corresponding timestamp in the "x-altus-date" header. `cdpcurl` constructs the headers automatically. However, if you would rather use a different HTTP client, such as ordinary `curl`, then you may directly use the `cdpv1sign` script within `cdpcurl` to generate these required headers. You may then parse the header values from the script output and feed them to your preferred client. Note that CDP API services will reject calls with timestamps too far in the past, so generate new headers for each call.

```bash
$ cdpv1sign -X POST https://api.us-west-1.cdp.cloudera.com/api/v1/environments2/listEnvironments
Content-Type: application/json
x-altus-date: Fri, 28 Aug 2020 20:38:38 GMT
x-altus-auth: (very long string value)
```

The signature algorithm specification is available from the [API documentation](https://cloudera.github.io/cdp-dev-docs/api-docs/).

## License

Copyright (c) 2020, Cloudera, Inc. All Rights Reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

---

The GNU AGPL v3 is available in [LICENSE.txt](LICENSE.txt).

Additional license information is available in [NOTICE.txt](NOTICE.txt).

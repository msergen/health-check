#!/usr/bin/env python3

import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    endpoint = os.environ.get("CALL_ENDPOINT")
    if not endpoint:
        sys.stderr.write("CALL_ENDPOINT environment variable is not set.\n")
        return 1

    try:
        with urllib.request.urlopen(endpoint) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        sys.stderr.write(f"Request failed with status {exc.code}: {exc.reason}\n")
        if exc.fp:
            body = exc.fp.read().decode("utf-8", errors="replace")
            if body:
                sys.stderr.write(body + "\n")
        return 1
    except urllib.error.URLError as exc:
        sys.stderr.write(f"Failed to reach endpoint: {exc.reason}\n")
        return 1

    print(f"Request succeeded with status {status}")
    if body.strip():
        print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())

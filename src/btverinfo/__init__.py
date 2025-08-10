"""
Bluetooth Version Info Decoder Library and CLI
"""

import sys
from typing import NamedTuple

# Import the generated database
from .bt_assigned_numbers_db import company_identifiers, core_versions

# Build lookup tables
_COMPANY_ID_MAP = {int(entry["value"]): entry["name"] for entry in company_identifiers}
_CORE_VERSION_MAP = {int(entry["value"]): entry["name"] for entry in core_versions}


class BTVersionInfo(NamedTuple):
    version_name: str
    version_number: float | None
    company: str
    subversion: int


def decode(version_byte: int, company_id: int, subversion: int) -> BTVersionInfo:
    # sanitize: version_byte should be < 256, etc
    if not (0 <= version_byte < 256):
        raise ValueError("Invalid version byte")
    if not (0 <= company_id < 65536):
        raise ValueError("Invalid company ID")
    if not (0 <= subversion < 65536):
        raise ValueError("Invalid subversion")

    version_str = _CORE_VERSION_MAP.get(version_byte, "Unknown")
    import re

    m = re.search(r"Bluetooth.*?(\d+\.\d+)", version_str)
    if m:
        version_number = float(m.group(1))
    else:
        version_number = None

    return BTVersionInfo(
        version_name=version_str,
        company=_COMPANY_ID_MAP.get(company_id, "Unknown"),
        subversion=subversion,
        version_number=version_number,
    )


def _parse_args(args):
    # Accepts: version company_id subversion (all int, hex, or 'ffff:ff.ffff')
    if len(args) == 1 and ":" in args[0]:
        # Custom format: ff:ffff.ffff
        import re

        m = re.fullmatch(r"([0-9a-fA-F]+):([0-9a-fA-F]+)\.([0-9a-fA-F]+)", args[0])
        if not m:
            raise ValueError("Invalid custom format. Use ff:ffff.ffff")

        version_str, company_str, subver_str = m.groups()
        version_byte = int(version_str, 16)
        company_id = int(company_str, 16)
        subversion = int(subver_str, 16)
        return version_byte, company_id, subversion
    elif len(args) == 3:

        def parse_num(s):
            s = s.lower()
            if s.startswith("0x"):
                return int(s, 16)
            return int(s, 10)

        return tuple(parse_num(a) for a in args)
    else:
        raise ValueError(
            "Usage: btverinfo <version> <company_id> <subversion> or btverinfo ff:ffff.ffff"
        )


def main():
    try:
        version_byte, company_id, subversion = _parse_args(sys.argv[1:])
        info = decode(version_byte, company_id, subversion)
        print(f"Version Name: {info.version_name}")
        print(f"Company: {info.company}")
        print(f"Subversion: {info.subversion}")
        print(f"Version Number: {info.version_number}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

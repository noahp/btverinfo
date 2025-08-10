# Bluetooth SIG Assigned Numbers Decoder

Simple python library + command-line utility for decoding `LL_VERSION_IND`
response data.

## Usage

### Command line:

```bash
❯ btverinfo 0x0d 0x000f 0x220f
Version Name: Bluetooth® Core Specification 5.4
Company: Broadcom Corporation
Subversion: 8719
Version Number: 5.4

# or
❯ btverinfo 0d:000f.220f
Version Name: Bluetooth® Core Specification 5.4
Company: Broadcom Corporation
Subversion: 8719
Version Number: 5.4
```

### Library

```python
>>> from btverinfo import decode
>>> decode(0xd, 0xf, 0x220f)
BTVersionInfo(version_name='Bluetooth® Core Specification 5.4', version_number=5.4, company='Broadcom Corporation', subversion=8719)
```

## Refreshing the database

```bash
❯ uv run src/btverinfo/gen_bt_assigned_db.py
# and commit the result
```

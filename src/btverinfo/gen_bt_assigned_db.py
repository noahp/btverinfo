"""
Script to generate a Python database file from Bluetooth SIG assigned number YAML files.
"""

import os

import requests
import yaml

COMPANY_IDS_URL = "https://bitbucket.org/bluetooth-SIG/public/raw/main/assigned_numbers/company_identifiers/company_identifiers.yaml"
CORE_VERSION_URL = "https://bitbucket.org/bluetooth-SIG/public/raw/main/assigned_numbers/core/core_version.yaml"

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "bt_assigned_numbers_db.py")


def fetch_yaml(url):
    resp = requests.get(url)
    resp.raise_for_status()
    # Fix known encoding issue in YAML files
    text = resp.text.replace("BluetoothÂ®", "Bluetooth®")

    # The company identifiers file contains some weird sequences like this:
    # ❯ echo 'SISTEMAS KERN, SOCIEDAD ANÓMINA' | xxd
    # 00000000: 5349 5354 454d 4153 204b 4552 4e2c 2053  SISTEMAS KERN, S
    # 00000010: 4f43 4945 4441 4420 414e c393 4d49 4e41  OCIEDAD AN..MINA
    # 00000020: 0a                                       .
    #
    # Re-encode as UTF-8 to absorb those issues.
    text = text.encode("latin-1").decode("utf-8", errors="replace")

    # Lastly, replace 'Bluetooth�' with 'Bluetooth®'
    text = text.replace("Bluetooth�", "Bluetooth®")

    return yaml.safe_load(text)


def main():
    print("Downloading YAML files...")
    company_data = fetch_yaml(COMPANY_IDS_URL)
    core_version_data = fetch_yaml(CORE_VERSION_URL)

    print(f"Writing database to {OUTPUT_FILE} ...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Auto-generated from Bluetooth SIG assigned numbers\n")
        f.write("company_identifiers = ")
        f.write(repr(company_data.get("company_identifiers", [])))
        f.write("\n\n")
        f.write("core_versions = ")
        f.write(repr(core_version_data.get("core_version", [])))
        f.write("\n")
    # Format the output file with ruff format
    try:
        import subprocess

        subprocess.run(["ruff", "format", OUTPUT_FILE], check=True)
        print(f"Formatted {OUTPUT_FILE} with ruff.")
    except Exception as e:
        print(f"Warning: Could not format with ruff: {e}")
    print("Done.")


if __name__ == "__main__":
    main()

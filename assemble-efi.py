#!/usr/bin/env python3
"""Build a portable EFI ZIP from the published configuration and pinned drivers."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
from pathlib import Path
import plistlib
from urllib.request import Request, urlopen
import zipfile


ROOT = Path(__file__).resolve().parent


def verify(data, expected, name):
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f"SHA-256 mismatch: {name}")
    return data


def verify_file(data, info, name):
    if info.get("normalize_newlines"):
        data = data.replace(b"\r\n", b"\n")
    return verify(data, info["sha256"], name)


def component_files(component, source_efi):
    if source_efi is not None:
        return {
            name: verify_file((source_efi / Path(name).relative_to("EFI")).read_bytes(), info, name)
            for name, info in component["files"].items()
        }

    url = component["url"]
    request = Request(url, headers={"User-Agent": "WUJIE14XA-Tahoe-EFI"})
    with urlopen(request, timeout=60) as response:
        data = verify(response.read(), component["sha256"], url)
    if not any("member" in info for info in component["files"].values()):
        return {
            name: verify_file(data, info, name)
            for name, info in component["files"].items()
        }
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        return {
            name: verify_file(archive.read(info["member"]), info, name)
            for name, info in component["files"].items()
        }


def validate(files):
    config = plistlib.loads(files["EFI/OC/config.plist"])
    required = {"EFI/BOOT/BOOTx64.efi", "EFI/OC/OpenCore.efi"}
    for entry in config["Kernel"]["Add"]:
        if entry["Enabled"]:
            for key in ("PlistPath", "ExecutablePath"):
                if entry[key]:
                    required.add(f"EFI/OC/Kexts/{entry['BundlePath']}/{entry[key]}")
    for section, key, folder in (("ACPI", "Add", "ACPI"), ("UEFI", "Drivers", "Drivers")):
        required.update(
            f"EFI/OC/{folder}/{entry['Path']}"
            for entry in config[section][key]
            if entry["Enabled"]
        )
    missing = required.difference(files)
    if missing:
        raise ValueError(f"Missing EFI files: {', '.join(sorted(missing))}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("WUJIE14XA-EFI.zip"))
    parser.add_argument("--source-efi", type=Path, help="Optional path to an existing EFI directory for offline assembly")
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"output already exists: {args.output}")

    components = json.loads((ROOT / "components.json").read_text(encoding="utf-8"))
    files = {
        path.relative_to(ROOT).as_posix(): path.read_bytes()
        for directory in (ROOT / "EFI", ROOT / "Extras", ROOT / "licenses")
        for path in directory.rglob("*")
        if path.is_file()
    }
    with ThreadPoolExecutor(max_workers=6) as pool:
        downloads = [pool.submit(component_files, item, args.source_efi) for item in components]
        for download in downloads:
            part = download.result()
            if files.keys() & part.keys():
                raise ValueError("Duplicate EFI file in components.json")
            files.update(part)
    validate(files)

    with zipfile.ZipFile(args.output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name)
            entry.create_system = 3
            entry.external_attr = (0o100755 if name.endswith(".command") else 0o100644) << 16
            archive.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED)
    print(args.output.resolve())


if __name__ == "__main__":
    main()

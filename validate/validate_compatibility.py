#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ROOT / "compatibility" / "support.json"
AGENTLY_ROOT = ROOT.parent / "Agently"
AGENTLY_INDEX = AGENTLY_ROOT / "compatibility" / "index.json"
AGENTLY_IN_DEVELOPMENT = AGENTLY_ROOT / "compatibility" / "in-development.json"


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def main() -> None:
    passes: list[str] = []
    failures: list[str] = []

    support = json.loads(SUPPORT.read_text(encoding="utf-8"))
    protocols = support.get("supported_protocols", {})
    authoring = protocols.get("authoring", [])
    devtools_guidance = protocols.get("devtools_guidance", [])

    check("schema_version", support.get("schema_version") == 1, "support manifest schema is 1", failures, passes)
    check("framework", support.get("framework") == "agently", "framework is agently", failures, passes)
    check("aligned_framework_version", isinstance(support.get("aligned_framework_version"), str), "aligned framework version exists", failures, passes)
    check("authoring_protocols", bool(authoring), "authoring protocols declared", failures, passes)
    check("devtools_guidance_protocols", bool(devtools_guidance), "devtools guidance protocols declared", failures, passes)

    if AGENTLY_INDEX.exists():
        index = json.loads(AGENTLY_INDEX.read_text(encoding="utf-8"))
        aligned_version = support.get("aligned_framework_version")
        release_files = index.get("release_files", {})
        release_path = release_files.get(aligned_version)
        check(
            "aligned_release_manifest_entry",
            isinstance(release_path, str),
            "Agently compatibility registry contains the aligned release entry",
            failures,
            passes,
        )
        if isinstance(release_path, str):
            release_manifest = json.loads((AGENTLY_ROOT / release_path).read_text(encoding="utf-8"))
            skills = release_manifest.get("companions", {}).get("skills", {})
            check(
                "authoring_protocol_supported",
                skills.get("authoring_protocol") in authoring,
                "Agently release authoring protocol is supported by Agently-Skills",
                failures,
                passes,
            )
            check(
                "devtools_guidance_protocol_supported",
                skills.get("devtools_guidance_protocol") in devtools_guidance,
                "Agently release DevTools guidance protocol is supported by Agently-Skills",
                failures,
                passes,
            )

    if AGENTLY_IN_DEVELOPMENT.exists():
        in_development = json.loads(AGENTLY_IN_DEVELOPMENT.read_text(encoding="utf-8"))
        skills = in_development.get("companions", {}).get("skills", {})
        check(
            "in_development_authoring_protocol_supported",
            skills.get("authoring_protocol") in authoring,
            "Agently in-development authoring protocol is supported by Agently-Skills",
            failures,
            passes,
        )
        check(
            "in_development_devtools_guidance_protocol_supported",
            skills.get("devtools_guidance_protocol") in devtools_guidance,
            "Agently in-development DevTools guidance protocol is supported by Agently-Skills",
            failures,
            passes,
        )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_cn = (ROOT / "README_CN.md").read_text(encoding="utf-8")
    aligned_version = str(support.get("aligned_framework_version"))
    check(
        "readme_mentions_aligned_version",
        f"Agently {aligned_version}" in readme,
        "README mentions the aligned Agently release line",
        failures,
        passes,
    )
    check(
        "readme_cn_mentions_aligned_version",
        f"Agently {aligned_version}" in readme_cn,
        "README_CN mentions the aligned Agently release line",
        failures,
        passes,
    )

    print("Compatibility support validation")
    print(f"passes: {len(passes)}")
    for item in passes:
        print(f"PASS  {item}")
    print(f"failures: {len(failures)}")
    for item in failures:
        print(f"FAIL  {item}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

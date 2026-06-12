#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "validate" / "fixtures" / "implementation_cases.json"
TRIGGERFLOW_EXAMPLES = ROOT / "skills" / "agently-triggerflow" / "examples"
TRIGGERFLOW_LEGACY_ALLOWLIST: set[Path] = set()
DEPRECATED_TRIGGERFLOW_TOKENS = [
    ".end(",
    ".start(",
    "set_result(",
    "get_runtime_data(",
    "set_runtime_data(",
    "append_runtime_data(",
    "del_runtime_data(",
    "get_flow_data(",
    "set_flow_data(",
    "append_flow_data(",
    "del_flow_data(",
    "get_runtime_stream(",
]
DEPRECATED_TRIGGERFLOW_PATTERNS = [
    ("execution.get_result(", re.compile(r"\bexecution\.get_result\(")),
    ("execution.async_get_result(", re.compile(r"\bexecution\.async_get_result\(")),
]


def check(name: str, condition: bool, details: str, failures: list[str], passes: list[str]) -> None:
    if condition:
        passes.append(f"{name}: {details}")
    else:
        failures.append(f"{name}: {details}")


def main() -> None:
    data = json.loads(FIXTURES.read_text(encoding="utf-8"))
    passes: list[str] = []
    failures: list[str] = []

    for case in data["cases"]:
        example_path = ROOT / case["reference_example"]
        check(case["id"] + "_example", example_path.exists(), "reference example exists", failures, passes)
        if not example_path.exists():
            continue
        content = example_path.read_text(encoding="utf-8")
        for required in case["required_primitives"]:
            if required == "tuple_ensure":
                condition = re.search(r"\([^)\n]+,\s*True\)", content) is not None
                details = "required primitive tuple ensure is present"
            else:
                condition = required in content
                details = f"required primitive {required} is present"
            check(
                f"{case['id']}_{required}",
                condition,
                details,
                failures,
                passes,
            )
        for forbidden in case["forbidden_antipatterns"]:
            check(
                f"{case['id']}_not_{forbidden}",
                forbidden not in content,
                f"forbidden anti-pattern {forbidden} is absent",
                failures,
                passes,
            )
        check(
            f"{case['id']}_profile",
            case["live_smoke_profile"] in {"deepseek", "local"},
            "live smoke profile is valid",
            failures,
            passes,
        )

    for example_path in sorted(TRIGGERFLOW_EXAMPLES.glob("*.py")):
        relative_path = example_path.relative_to(ROOT)
        if relative_path in TRIGGERFLOW_LEGACY_ALLOWLIST:
            continue
        content = example_path.read_text(encoding="utf-8")
        for token in DEPRECATED_TRIGGERFLOW_TOKENS:
            check(
                f"triggerflow_examples_no_deprecated_{example_path.stem}_{token}",
                token not in content,
                f"recommended TriggerFlow example does not use deprecated token {token}",
                failures,
                passes,
            )
        for name, pattern in DEPRECATED_TRIGGERFLOW_PATTERNS:
            check(
                f"triggerflow_examples_no_deprecated_{example_path.stem}_{name}",
                pattern.search(content) is None,
                f"recommended TriggerFlow example does not use deprecated lifecycle call {name}",
                failures,
                passes,
            )
        check(
            f"triggerflow_examples_close_{example_path.stem}",
            "async_close" in content or ".close(" in content,
            "recommended TriggerFlow example uses explicit execution close",
            failures,
            passes,
        )

    print("V2 native usage validation")
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

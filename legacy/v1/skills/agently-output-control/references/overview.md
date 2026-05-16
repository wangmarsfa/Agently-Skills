# Overview

This skill owns output-contract shape, `.output(...)`, prompt-config-owned output contracts, tuple `ensure`, runtime `ensure_keys`, `.validate(...)`, field ordering, structured streaming, and output reliability.

Use prompt config when the output contract is stable and shared. Use code-side `.output(...)` when the schema is temporary, dynamic, or tightly coupled to runtime-only branching.

For Agently `4.1.0.1+`, use tuple `ensure` in `.output(...)` for fixed required leaves. Use manual `ensure_keys` when the path-existence rule is runtime-dependent, conditional, or easier to express outside the static schema.

Use `.validate(...)` or `validate_handler=` when the path exists but the value still needs business validation, such as enum checks, score ranges, or cross-field consistency.

In advanced retry flows, validators may also tune later retries by writing through `context.prompt` or `context.settings`. Prefer `context.prompt.set("options", {...})` or `context.settings.set(...)` over mutating the object returned by `get()`, and document clearly that these writes affect later retries, not the current finished attempt, and do not leak into later fresh requests.

When one request result will be read multiple ways, prefer `response = ...get_response()` and reuse `response.result`; validate runs once per response and is cached across later `get_data()` / `get_data_object()` reads.

# Overview

This skill owns output-contract shape, `.output(...)`, prompt-config-owned output contracts, tuple `ensure`, runtime `ensure_keys`, `.validate(...)`, field ordering, structured streaming, and output reliability.

Use prompt config when the output contract is stable and shared. Use code-side `.output(...)` when the schema is temporary, dynamic, or tightly coupled to runtime-only branching.

For Agently `4.1.0.1+`, use tuple `ensure` in `.output(...)` for fixed required leaves. Use manual `ensure_keys` when the path-existence rule is runtime-dependent, conditional, or easier to express outside the static schema.

Use `.validate(...)` or `validate_handler=` when the path exists but the value still needs business validation, such as enum checks, score ranges, or cross-field consistency.

When one request result will be read multiple ways, prefer `response = ...get_response()` and reuse `response.result`; validate runs once per response and is cached across later `get_data()` / `get_data_object()` reads.

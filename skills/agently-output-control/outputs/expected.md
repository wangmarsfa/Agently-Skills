# Expected Output

The answer should prefer `.output(...)` plus tuple `ensure` for fixed required leaves, use runtime `ensure_keys` only for conditional path-presence checks, and use `.validate(...)` / `validate_handler=` for business-rule checks instead of custom parsers or handwritten retry loops. If the user needs later retries to change prompt options or settings, the answer may mention the advanced path of writing through `context.prompt.set(...)` or `context.settings.set(...)`, while noting that mutating values returned by `get()` is not the stable write path.

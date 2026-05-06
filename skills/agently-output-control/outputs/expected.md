# Expected Output

The answer should prefer `.output(...)` plus tuple `ensure` for fixed required leaves, use runtime `ensure_keys` only for conditional path-presence checks, and use `.validate(...)` / `validate_handler=` for business-rule checks instead of custom parsers or handwritten retry loops.

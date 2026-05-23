# Agently Output Control

Use this skill when the question is what shape the model should return and how that shape should stay reliable.

The user does not need to say `.output(...)`, tuple `ensure`, `ensure_keys`, or `.validate(...)`. Requests for stable JSON-like fields, structured reports, or machine-readable sections should route here.

## Native-First Rules

- default to async-first response consumption when structured output will be streamed, reused, or served over an async boundary
- prefer prompt-config-owned output contracts such as `.request.output` when the schema is stable and shared across a request family
- prefer `.output(...)` for machine-readable results when the schema is dynamic, exploratory, or easier to keep close to code
- choose output format deliberately:
  - `.output(...)` defaults to `format="auto"`; use it for ordinary structured
    results consumed through Agently's parsed data API
  - use `format="flat_markdown"` for a flat dict of scalar fields, especially
    when one field may contain large code, HTML, SVG, Markdown, SQL, templates,
    or multi-paragraph prose; section headers avoid JSON escaping failures
  - use `format="hybrid"` when prose/code scalar fields are mixed with
    structured lists or objects, such as `summary` plus `citations`,
    `analysis` plus `components`, or `notes` plus `next_steps`
  - use `format="json"` when downstream code needs the legacy JSON-only
    contract, external API interop, exact raw JSON behavior, or dense nested
    arrays/objects
  - use plain text instead of `.output(...)` for one freeform artifact: an
    article, email, explanation, report, Markdown page, HTML page, or other
    single multi-paragraph document; read it with `start()` / `async_start()` or
    `response.result.get_text()`
- for Agently `4.1.0.1+`, prefer tuple `ensure` in `.output(...)` for fixed required leaves
- use manual `ensure_keys` only when the required path is runtime-dependent, conditional, or awkward to express in the static schema
- prefer `.validate(...)` or `validate_handler=` when the field exists but the value still needs business validation
- keep output schema explicit when downstream systems, workflow branches, or later model steps consume the result
- order dependent fields before the final decision or user-facing answer field:
  put evidence, assumptions, clarifications, source notes, calculation plans,
  brief rationale, rule checks, and intermediate structured facts first, then
  put the final boolean, verdict, `reply`, summary, or action decision last.
  Agently output schemas are ordered; the model should generate supporting
  fields before conclusions even if the UI later reorders the final document for
  human reading. Do not ask for verbose hidden reasoning when a concise
  rationale, evidence list, or check list is enough.
- use conceptual grade labels for model-owned evaluation fields instead of
  precise numeric scores. Define each label in the prompt, for example:
  `high_trust` means authoritative sources, sufficient evidence, direct
  evidence-to-claim linkage, and broad domain support; `moderate_trust` means
  broad sources and direct or indirect support with some cross-domain inference;
  `low_trust` means missing sources, promotional-only sources, or weak
  evidence-to-claim linkage. When later code needs a number, map labels to
  deterministic values after generation.
- when a task needs complex arithmetic, long-number calculation, weighting,
  aggregation, or statistical transformations, make the model output an
  executable calculation plan or code, run it through tools, and pass the code
  plus raw result into a later model step. Do not make the model's text
  generation be the calculator.
- for tests that validate model-owned semantic content, prefer a second Agently
  model-judge request with output control: pass the candidate output, explicit
  rules, expected contract, and relevant context; ask for per-rule evidence,
  concise reason, and final boolean fields; assert the booleans. Use
  deterministic keyword/substring/regex checks only as smoke gates for
  structure, routing, or required-field presence, not as the primary content
  correctness signal.

## Anti-Patterns

- do not handwrite JSON post-processors when `.output(...)` already owns the contract
- do not rebuild a stable shared schema in Python if prompt config can own it once
- do not build custom retry loops for missing keys before using tuple `ensure` or, when necessary, runtime `ensure_keys`
- do not overload tuple `ensure` or `ensure_keys` with value checks that belong in `.validate(...)`
- do not default to sync-only result handling when the caller is already async-capable
- do not rely on keyword, substring, regex, or text snapshot checks as the main
  assertion for whether model-generated content satisfies business rules

## Read Next

- `references/overview.md`

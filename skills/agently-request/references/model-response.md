# Agently Model Result

Use this skill when the output contract is already chosen and the remaining issue is how the result facade should be consumed or reused.

The user does not need to say `get_result()`. Requests to reuse one result as text, parsed data, metadata, or progressive updates should route here.

Optional request scheduling belongs to model request settings, not custom
caller-side semaphores. Use `model_request.scheduler.max_concurrency`,
`model_request.scheduler.rate_per_second`, and optional
`model_request.scheduler.providers.<provider>` overrides when a service or
long-running task needs provider-level dispatch limits. Use
`model_request.retry_backoff_base` and `model_request.retry_backoff_max` when
retries should back off instead of immediately re-issuing. If these settings are
absent, dispatch and retry timing keep the legacy immediate behavior.

## Native-First Rules

- prefer `get_result()` when one request result must be consumed more than once
- default to async-first response APIs in services, streaming paths, TriggerFlow steps, and any integration that may overlap work
- treat sync getters and generators as convenience wrappers for scripts, REPL use, or compatibility bridges
- use `delta`, `instant`, `specific`, or `all` instead of custom stream splitting logic
- when OpenAICompatible replays a transient disconnect after partial output,
  treat `StreamingData(path="$status", value=...)` as a framework control record:
  `failed` plus `retry=True` invalidates provisional output and requires the UI
  or SSE consumer to clear it before replacement deltas arrive. Plain `delta`
  streams emit the standalone `"<$retry>{reason}</$retry>"` marker at that
  same boundary; clear the local text buffer when it arrives. Use `instant`,
  `specific="status"`, or `all` when lineage or collision-free structured
  facts matter
- annotate common stream consumers from `agently`: `StreamingData` for
  `instant` / `streaming_parse`, `AgentlySpecificResultMessage` for
  `specific`, and `AgentlyModelResultMessage` for `all`; use
  `agently.types.data` when the full typed data namespace is needed
- subscribe to `reasoning_delta` / `reasoning_done` through `type="specific"`
  when reasoning output is needed. Provider-native reasoning and a leading
  outer `<think>...</think>` before the answer payload belong in reasoning
  events; `original_delta` / `original_done` keep the raw provider content.
  Payload-internal `<think>` remains ordinary answer text
- treat `instant` `.is_complete` as path completion, not a global display-order
  barrier. For Web UI, SSE, or WebSocket consumers, render each path into its
  own slot. For CLI consumers that print multiple paths into one terminal area,
  use a small state flag or buffer and flush later-path deltas only after the
  earlier path's completion event has been handled

## Anti-Patterns

- do not re-issue the same request to obtain text, data, and metadata separately
- do not build ad hoc field-level stream parsers when `instant` or `streaming_parse` already fits
- do not strip reasoning tags inside format-specific parsers

## Read Next

- `references/overview.md`

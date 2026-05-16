---
name: agently-triggerflow
description: Use when the user needs workflow orchestration such as branching, concurrency, approvals, waiting and resume, runtime stream, restart-safe execution, mixed sync/async function or module orchestration, event-driven fan-out, process-clarity refactors that make stages explicit, performance-oriented refactors that collapse split requests, or workflow definitions and chunk-level runtime metadata that must stay visible for debugging and visualization. The user does not need to say TriggerFlow explicitly.
---

# Agently TriggerFlow

Use this skill when the solution clearly needs orchestration semantics rather than one request family.

The user does not need to say TriggerFlow or Agently. Scenario language such as resumable approval flow, branching automation, output-fan-out refactor, mixed sync/async pipeline, process-clarity refactor, or draft-review-revise pipeline should still route here once orchestration is clearly the owner layer.

## Native-First Rules

- prefer TriggerFlow for explicit multi-stage quality loops, branching, concurrency, waiting/resume, restart-safe execution, output-fan-out performance refactors, process-clarity refactors, or mixed sync/async orchestration
- default to async-first workflow handlers, execution entrypoints, and runtime stream consumers
- treat sync TriggerFlow APIs as wrappers for scripts or compatibility bridges, not as the default service interface
- prefer explicit execution lifecycle control with `close()` / `async_close()` for completion and cleanup
- use `emit_nowait(...)` / `async_emit_nowait(...)` when a chunk must fan out without blocking the current handler, and rely on execution close to drain registered tasks
- use execution runtime state through `get_state(...)` / `set_state(...)` instead of legacy runtime-data helpers in new examples
- treat shared flow data as a risky cross-execution surface and avoid it unless the task explicitly needs shared state
- for service packaging, prefer module-level named chunks plus a small flow builder/factory; inject stable dependencies through flow-level `runtime_resources` and request-specific dependencies through execution-level `runtime_resources`
- keep runtime stream consumers safe by relying on execution close to stop the stream
- keep workflow stages visible instead of hiding nested request loops
- name chunks and stage boundaries so exported flow configs, Mermaid diagrams, and runtime graphs stay readable
- let TriggerFlow definition export and runtime metadata drive visualization instead of maintaining a second manual graph description
- combine with `agently-request` when one workflow step needs model setup, prompt contracts, structured output, response reuse, session behavior, or retrieval

## Anti-Patterns

- do not invent a custom event bus or state machine before checking TriggerFlow
- do not use untracked `asyncio.create_task(data.async_emit(...))` as the default nowait pattern when execution-managed `emit_nowait(...)` is available
- do not recommend `.end()`, `get_result()`, or `set_result()` as the default lifecycle path for new TriggerFlow code
- do not use `get_runtime_data(...)` / `set_runtime_data(...)` in new guidance when `get_state(...)` / `set_state(...)` communicates the same intent
- do not use flow data for per-execution state
- do not make service chunks depend on closure-captured business context when `runtime_resources` would keep the handler reusable, testable, and export-friendly
- do not pass raw model stream paths directly to the UI when the workflow can translate them into stable business events
- do not hide draft/judge/revise or similar loops inside one opaque helper
- do not make DevTools or graph tooling the source of truth for workflow structure when TriggerFlow definitions already are

## Read Next

- `references/overview.md`
- `references/stream-bridge.md`
- `references/devtools-graph.md`

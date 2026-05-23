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
- use `execution.result` when services, UIs, stream consumers, or intervention-aware workflows need multiple views of one execution outcome, such as state, compatibility final result, interventions, and metadata; use `execution.close()` / `execution.async_close()` for close snapshots
- use runtime intervention for optional supplemental context added while an execution is already running: define explicit `.intervention_point(...)` boundaries so execution creation can infer planned mode, or create the execution with `intervention_mode="auto"` for boundary policy insertion; chunks read inserted context with `data.get_interventions(...)` and explicitly audit usage with `data.async_mark_intervention_consumed(...)`, relying on the chunk-name consumer default unless another consumer identity is clearer
- for human approvals, webhooks, or externally resumed waits, use `pause_for(..., resume_to="next" | "self" | {"event": ...})`; treat it as a durable graph interrupt, not Python coroutine stack persistence; teach model-decided autonomous interrupts with model-owned `pause_for(..., resume_to="self")`, and teach prearranged approval gates with an explicit pause chunk plus `when(...)`
- do not put `pause_for(...)` behind hidden execution sugar such as `flow.start()` or flow-level runtime stream helpers; create an explicit execution handle and consume `get_pending_interrupts()` / `continue_with(...)`
- close waiting executions explicitly: `close()` / `async_close()` rejects pending interrupts by default, and `pending_interrupts="cancel"` must be chosen deliberately when abandoning waits
- when a sub-flow can pause, keep the external API rooted at the parent execution id plus projected root interrupt id; do not require callers to manage child execution ids
- use `emit_nowait(...)` / `async_emit_nowait(...)` when a chunk must fan out without blocking the current handler, and rely on execution close to drain registered tasks
- use execution runtime state through `get_state(...)` / `set_state(...)` instead of legacy runtime-data helpers in new examples
- treat shared flow data as a risky cross-execution surface and avoid it unless the task explicitly needs shared state
- for service packaging, treat ordinary `TriggerFlow(...)` as the definition/planning surface; prefer module-level named chunks and conditions, inject stable dependencies through flow-level `runtime_resources`, and inject request-specific dependencies through execution-level `runtime_resources`
- route model-generated or app-submitted DAG data to `agently-dynamic-task`; Dynamic Task is a first-class Agently API that uses TriggerFlow as an execution substrate, not a TriggerFlow sub-API
- use `when(...)` + `emit_nowait(...)` as the native signal-driven pattern for fan-out, loops, side branches, and dependency joins; definition idempotence must not be confused with runtime signal deduplication
- keep runtime stream consumers safe by relying on execution close to stop the stream
- keep workflow stages visible instead of hiding nested request loops
- name chunks and stage boundaries so exported flow configs, Mermaid diagrams, and runtime graphs stay readable
- let TriggerFlow definition export and runtime metadata drive visualization instead of maintaining a second manual graph description
- combine with `agently-request` when one workflow step needs model setup, prompt contracts, structured output, response reuse, session behavior, or retrieval

## Python API Shape

When generating or editing Python code, use the actual Agently API shape:

```python
from agently import TriggerFlow, TriggerFlowRuntimeData
```

`when`, `emit_nowait`, and `pause_for` are not top-level imports from
`agently`. They are methods on flow or runtime data objects:

- define graph branches with `flow.when(...).to(handler, name="...")`
- fan out from inside a chunk with `data.emit_nowait(...)`
- pause from inside a chunk with `await data.async_pause_for(...)`
- create and close long-running/manual executions with
  `execution = flow.create_execution(auto_close=False)`,
  `await execution.async_start(input_value)`, and
  `snapshot = await execution.async_close()`

Do not write `from agently import when, emit_nowait, pause_for`, and do not use
`@flow.when(...)` as a decorator.

## Dynamic Task Boundary

Do not treat Dynamic Task as TriggerFlow syntax. If a model or application
submits a DAG as data, route to `agently-dynamic-task` and use
`Agently.create_dynamic_task(...)`, `TaskDAGValidator`, and `TaskDAGExecutor`
there. TriggerFlow remains the substrate for stable workflow definitions that
the developer owns in code.

## Anti-Patterns

- do not invent a custom event bus or state machine before checking TriggerFlow
- do not implement a custom DAG scheduler in TriggerFlow when Dynamic Task can validate and execute submitted task graphs
- do not use untracked `asyncio.create_task(data.async_emit(...))` as the default nowait pattern when execution-managed `emit_nowait(...)` is available
- do not recommend `.end()`, `get_result()`, or `set_result()` as the default lifecycle path for new TriggerFlow code
- do not add custom result containers around TriggerFlow executions when `execution.result` can expose the needed state/final-result/intervention/meta view
- do not use runtime intervention as a required wait gate; use `pause_for(...)` / `continue_with(...)` when the workflow must stop for external input
- do not treat `intervene(...)` as `emit(...)`, graph mutation, input rewriting, chunk cancellation, or replay of completed chunks
- do not use `get_runtime_data(...)` / `set_runtime_data(...)` in new guidance when `get_state(...)` / `set_state(...)` communicates the same intent
- do not treat repeated silence after one deprecation warning as approval; Agently emits each deprecated API warning once per Python process
- do not treat `runtime.show_deprecation_warnings=False` as a migration substitute; it is only a production noise-control setting
- do not use flow data for per-execution state
- do not write guidance that depends on code after `await data.async_pause_for(...)` surviving a process restart; put post-resume logic in the downstream chunk, `data.is_resume` branch, or explicit resume event handler
- do not make service chunks depend on closure-captured business context when `runtime_resources` would keep the handler reusable, testable, and export-friendly
- do not pass raw model stream paths directly to the UI when the workflow can translate them into stable business events
- do not hide draft/judge/revise or similar loops inside one opaque helper
- do not make DevTools or graph tooling the source of truth for workflow structure when TriggerFlow definitions already are

## Read Next

- `references/overview.md`
- `references/runtime-intervention.md`
- `references/stream-bridge.md`
- `references/devtools-graph.md`

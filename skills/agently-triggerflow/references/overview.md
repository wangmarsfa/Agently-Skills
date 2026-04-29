# Overview

This skill owns TriggerFlow orchestration, runtime data, runtime stream, sub-flow boundaries, workflow-side model execution, output-fan-out refactors, process-clarity refactors, and mixed sync/async orchestration.

Prefer async-first flow handlers and execution APIs. When the UI needs progressive updates, bridge model-side structured streaming into workflow-side runtime stream items so the frontend consumes stable business events instead of raw parser paths.

Prefer explicit execution lifecycle control. New TriggerFlow code should create or start an execution, let chunks update execution state, and finish with `close()` or `async_close()` so pending non-blocking work and runtime stream consumers are drained consistently. Avoid using result polling as the default completion contract.

Treat auto-close as the default for short workflows and manual close as the service/worker pattern for long-running or externally driven executions. A manual-close execution keeps accepting events until user code calls `close()` / `async_close()`.

Use execution state (`get_state(...)`, `set_state(...)`, and async variants) for per-execution data. Flow data is shared across executions and should be treated as a risky internal/shared-state surface rather than normal workflow memory.

In Agently `v4.1.0`, TriggerFlow definitions, chunk signal metadata, and origin-chunk payloads are also strong enough to support graph-oriented debugging and local DevTools visualization without duplicating the workflow description.

For the concrete `instant -> runtime stream` pattern, read `references/stream-bridge.md`.
For graph, export, and observation design, read `references/devtools-graph.md`.

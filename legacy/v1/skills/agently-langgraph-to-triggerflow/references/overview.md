# Overview

This skill maps LangGraph orchestration concerns into TriggerFlow-native orchestration surfaces.

Map LangGraph checkpoints and interrupts to TriggerFlow execution state, pause/resume, and save/load boundaries instead of rebuilding a graph runtime. Long-running or externally resumed flows should use explicit execution lifecycle control: start the execution, accept external events while it is open, and call `close()` / `async_close()` when the service owner decides no more events should be accepted.

Use auto-close for short batch-style workflows. Use manual close for worker, human-in-the-loop, webhook, or distributed-manager flows where the reliable end point is outside the graph itself.

Prefer execution state for per-run data. Treat shared flow data as a risky cross-execution surface and avoid using it as a replacement for LangGraph checkpoint state.

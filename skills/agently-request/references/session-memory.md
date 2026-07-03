# Agently Session Memory

Use this reference when the request path already exists but continuity,
Workspace-backed long-term memory, or restore behavior is the main design
problem.

## Native-First Rules

- prefer Session-backed continuity before inventing a custom memory layer
- for durable long-term memory, attach the public `SessionMemory` protocol
  through `session.use_memory(mode="AgentlyMemory", workspace=workspace)`
- for Agent-created sessions, activate the session and then call
  `agent.activated_session.use_memory(mode="AgentlyMemory")`; the session binds
  `agent.workspace` automatically when possible
- store memory through Workspace records, not process globals:
  `collection="memory"`, `kind="global_memory"` for `GLOBAL_MEMORY`, and
  `kind="session_memory"` for `SESSION_MEMORY`
- treat `GLOBAL_MEMORY` as Workspace-global and isolated across Workspaces;
  treat `SESSION_MEMORY` as additionally scoped by `runtime.session_id`
- configure body shape and model prompts under
  `session.memory.AgentlyMemory.*`; prompt overrides use
  Configure-Prompt-shaped `.execution` blocks
- let model requests own extraction, compression, retrieval-query planning, and
  rerank judgment; deterministic code should only validate shape, apply scope,
  store records, enforce budgets, and record diagnostics
- keep single-candidate or otherwise tiny scoped memory recall cheap:
  `AgentlyMemory` skips rerank below
  `session.memory.AgentlyMemory.retrieve.rerank_min_candidates` and records
  `memory_rerank_skipped`
- keep the built-in `AgentlyMemory` empty-rerank safeguard enabled by default:
  if rerank drops every candidate in a memory scope, it reinjects deterministic
  candidates and records `memory_rerank_empty_fallback`; disable only when the
  application explicitly prefers empty recall over conservative memory recall
- keep request-side chat history and memo boundaries explicit
- separate request memory from workflow runtime state

## Usage Shape

```python
workspace = Agently.create_workspace("./.agently/support-memory")

session = Session()
session.use_memory(mode="AgentlyMemory", workspace=workspace)
```

```python
agent = Agently.create_agent()
agent.use_workspace("./.agently/support-memory")
agent.activate_session(session_id="support-demo")
agent.activated_session.use_memory(mode="AgentlyMemory")
```

## Anti-Patterns

- do not use session as a substitute for workflow orchestration state
- do not keep restart-sensitive memory only in transient globals
- do not add a second memory extension concept when `SessionMemory` already names
  the extension protocol
- do not put Workspace retrieval strategy inside a Session memory plugin; use
  `workspace.retrieve(...)` so text/file/memory retrieval share the same
  substrate

## Read Next

- `references/knowledge-base.md`
- `references/prompt-management.md`

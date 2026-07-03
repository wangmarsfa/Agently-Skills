# Agently Knowledge Base

Use this skill when embeddings, Workspace recall, and retrieval are the main
capability surface.

## Native-First Rules

- prefer embedding-agent plus Chroma integration before custom vector plumbing
- use `workspace.retrieve(...)` for shared intelligent retrieval over Workspace
  records and files: keyword/tag candidates, optional vector mode,
  structure-gated model rerank over a bounded candidate-summary window,
  dropped-candidate refill, length-budget or `top_n` packaging, and compact
  selected-record projections with `projection`/`original_ref` metadata while
  raw Workspace records remain available for readback
- for multi-turn task information already stored in Workspace, prefer
  `workspace.build_context(goal=..., scope=..., budget=..., profile=...)` so
  ContextPlanner, Retriever, and ContextBuilder plugins own the retrieval path
- use `workspace.grep(...)` and `workspace.grep_files(...)` for low-level
  deterministic debugging or explicit filters, not as the normal app-facing
  recall API. `workspace.search(...)` and `workspace.search_files(...)` are
  compatibility aliases
- if vector mode is requested and the backend only has `NoopVectorIndex`, expect
  deterministic fallback plus diagnostics rather than silent failure
- use `workspace.get_data(...)` for structured records/checkpoints and
  `workspace.links(...)` for decision/evidence lineage when retrieval feeds a
  later loop step
- separate indexing, retrieval, and answer generation concerns
- keep retrieval results explicit when they feed a later request

## Anti-Patterns

- do not hide KB retrieval inside unrelated prompt logic
- do not treat embeddings-only setup and KB-backed answer flow as unrelated stacks
- do not ask business code to hand-write ordinary multi-turn recall filters when
  a Workspace ContextPackage is the right shape
- do not hide structure-gated model rerank, refill, or retrieval budgets inside
  Session memory code when `workspace.retrieve(...)` is the shared substrate

## Read Next

- `references/session-memory.md`
- `references/prompt-management.md`

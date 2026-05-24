---
name: agently-runtime
description: "Use when the user wants Agently runtime extension capabilities: Action Runtime, built-in action packages, legacy tool compatibility, MCP access, Execution Environment lifecycle, FastAPIHelper or streaming API exposure, auto-function helpers, KeyWaiter, or optional agently-devtools observation, evaluation, and playground integration."
---

# Agently Runtime

Use this skill when the app needs model-callable capabilities, managed execution
dependencies, service exposure, or development/runtime tooling around an
existing request or workflow design.

If the owner layer is still undecided, start with `agently-playbook`. If the
problem is multi-step orchestration, use `agently-triggerflow` first and return
here for Actions, Execution Environment, service, or DevTools details.

## Route Inside This Skill

- Action Runtime, `@agent.action_func`, `agent.use_actions(...)`, built-in Search/Browse, sandbox actions, or legacy tools -> `references/actions-runtime.md`
- Action vs Execution Environment boundaries, `agent.enable_*` helpers, provider lifecycle, managed MCP/sandbox/process/browser/SQLite resources -> `references/actions-execution-environment.md`
- observation, evaluation, playground, local logs, or `agently-devtools` -> `references/devtools.md`

## Native-First Rules

- prefer `@agent.action_func` and `agent.use_actions(...)`; `tool_func`, `use_tool`, `use_tools`, and `agently.builtins.tools` are compatibility surfaces
- use built-in web packages through `from agently.builtins.actions import Search, Browse` and mount with `agent.use_actions(Search(...))` / `agent.use_actions(Browse(...))`
- do not invent `enable_search(...)`; Search configuration belongs to the Search package/executor, not Execution Environment
- for app developers, prefer `agent.enable_python(...)`, `agent.enable_shell(...)`, `agent.enable_workspace(...)`, `agent.enable_nodejs(...)`, and `agent.enable_sqlite(...)` before direct manager/provider APIs
- for instruction-heavy Actions, expect later model rounds to see compact execution digests and artifact refs; use `agent.action.read_action_artifact(...)` only when full raw code, command output, SQL results, page content, or logs are needed
- treat `Agently.execution_environment` as an advanced framework/plugin surface for lifecycle, policy, approval, health, and release
- Action executors should declare or consume managed resources instead of secretly owning long-lived MCP clients, sandboxes, browsers, SQLite connections, or process runners
- keep permission profiles explicit: search-only, local-files-only, network-read, install-capable shell, or trusted executor
- treat `agently-devtools` as optional PyPI-installed tooling; wire observation through public bridge APIs, not source-repo paths
- for framework internals, preserve Agently's core module style: class-owned
  runtime behavior, typed data contracts, protocol/handler seams for
  replacement, and high-level packages outside `agently/core` when they compose
  several core systems
- for framework-side Skills Executor work, prefer the `Agently.skills_executor`
  facade backed by the builtin `SkillsExecutor` plugin; Agently 4.1.2.4 did not
  ship `Agently.skills` as a compatibility alias
- use `install_skills(...)` for one Agent Skills package,
  `install_skills_pack(...)` for a repository/group of Skills, and
  `agent.run_skills_task(...)` for explicit Skills execution
- for framework-side Skills execution, keep standard `SKILL.md` as the only
  capability definition; selected Skills default to `single_shot` model
  requests using their full Markdown guidance, while declared staged/react
  strategies should compose TriggerFlow and ActionFlow/ActionRuntime rather
  than adding a Skills-local executor
- for Agently 4.1.2.x auto-orchestration work, treat
  `agent.use_skills(...).input(...).start()` as route-candidate registration
  owned by the Agent route planner, not prompt-only Skills guidance injection by
  default
- for ambiguous optional route candidates, keep submitted Dynamic Task and
  required Skills deterministic, but let the model choose among optional auto
  Dynamic Task, model-decision Skills, and ordinary Action-backed model request
  routes
- for framework-side Skills, treat standard `SKILL.md` as the only capability
  definition; Agently install metadata and decision cards are descriptive
  runtime aids, not authoring formats or availability gates
- for Skills actions, use Action/ExecutionEnvironment approval and resource
  boundaries; use TriggerFlow `pause_for(...)` / `continue_with(...)` for
  durable waits instead of storing pending approvals on a Skills snapshot
- keep Agent auto-orchestration behind the `AgentOrchestrator` plugin protocol:
  core owns the public `agent.create_execution()` entrypoint, while the active
  plugin owns route planning, execution, and stream bridging
- for unified Agent execution/result work, prefer a response-style
  `agent.create_execution()` object with data/text/meta/stream consumption; use
  TriggerFlow runtime stream plus ModelRequest `instant` checkpoints for process
  streaming, and expose model field deltas only through stable structured paths
  such as `task_dag.tasks.<task_id>.fields.<field_path>` rather than raw provider
  token events

## Anti-Patterns

- do not build a parallel action/tool dispatcher before checking Action Runtime
- do not expose core Execution Environment manager APIs as the default app-development mental model
- do not route package installation or filesystem mutation through the Python sandbox
- do not ask users to clone or editable-install DevTools when `pip install agently-devtools` fits
- do not make DevTools the source of truth for workflow structure
- do not present prompt-only Skills disclosure as the default execution meaning
  of `agent.start()` once the 4.1.3 route planner owns Skills candidates
- do not put route-owned Skills, Dynamic Task, or stream-composition logic
  directly in core when a plugin protocol can own the replaceable behavior

## Read Next

- `references/actions-runtime.md`
- `references/actions-execution-environment.md`
- `references/devtools.md`

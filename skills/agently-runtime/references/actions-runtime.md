# Agently Runtime Extension Reference

Use this skill when the problem is agent-side extension rather than prompt shape, output contract, or workflow control.

## Native-First Rules

- prefer the native Action Runtime, built-in action packages, legacy tool facades, and MCP surfaces before handwritten wrappers
- keep extension choice explicit: Action Runtime, Execution Environment, built-in capability Actions, Agent Components, tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, or `agently-devtools`
- treat `Agently.execution_environment` as an advanced framework/plugin surface, not the default app-development API
- for application developers, prefer built-in Actions and `agent.enable_*` component helpers before exposing core manager/provider concepts
- default Agents expose `agent.workspace` as a lazy Foundation Workspace
  capability; call `agent.use_workspace(...)` when a stable explicit root,
  read-only mode, direct backend, or registered provider is required
- use `agent.workspace` for durable multi-turn task records, artifacts, search,
  links, checkpoints, stable ref envelopes, bounded reads, RuntimeEvent records,
  evidence links, and retention anchors
- use `workspace.build_context(...)` to package those records for later model
  calls; ordinary application code should not hand-write recall filters when a
  ContextPack through RecallPlanner/Retriever/ContextBuilder fits
- for AgentExecution evidence, keep persistence explicit with
  `execution.async_record_workspace(..., checkpoint=True)`; the helper writes
  requested checkpoints through the Workspace checkpoint-store port and records
  an evidence link between the AgentExecution record and checkpoint while
  leaving strategy decisions owned by AgentExecution
- AgentTaskLoop is the current strategy-level persistence owner: it writes task
  decisions, observations, verification records, checkpoints, and evidence links
  through the bound Workspace provider without making Workspace choose task
  continuation
- custom Workspace backends may be passed to `agent.use_workspace(backend)` or
  registered with `Agently.workspace.register_backend_provider(name, factory)`
  and selected through `agent.use_workspace(root, provider=name,
  provider_options={...})` when they implement the Workspace backend protocol;
  treat the remote audit provider proof as a protocol validation, not a
  production Redis/Postgres/S3 support claim
- in explicit TriggerFlow loops, prefer Workspace refs plus
  `workspace.get_data(...)`, `workspace.links(...)`,
  `workspace.latest_checkpoint(...)`, `workspace.checkpoint_history(...)`,
  `workspace.ref_envelope(...)`, `workspace.read_bounded(...)`, and
  `workspace.stream_read(...)` over storing large or structured loop state
  directly in TriggerFlow state; configure execution durability with
  `flow.create_execution(runtime_resources={"workspace": workspace})` or
  explicit `execution.set_checkpoint_store(workspace)` and
  `execution.set_runtime_event_store(workspace)` calls when the loop needs
  restart diagnostics; read checkpoint state back through
  `workspace.latest_checkpoint(...)` / `workspace.get_data(...)` and pass it
  to TriggerFlow `async_rehydrate(...)` for restart because TriggerFlow owns
  pause/resume, policy approval waits, and DAG join replay semantics; use
  `execution.async_save_checkpoint(require_distributed_provider=True)` only for
  providers that report distributed CAS, lease, range-read, retention, and
  RuntimeEvent sequencing capabilities
- use `agent.enable_python(...)`, `agent.enable_shell(...)`,
  `agent.enable_workspace_file_actions(...)`, `agent.enable_nodejs(...)`, and
  `agent.enable_sqlite(...)` for common Python, shell, model-callable local file,
  Node.js, and SQLite access
- when both are configured, filesystem-like helpers such as
  `agent.enable_workspace_file_actions(...)`, `agent.enable_shell(...)`, and
  `agent.enable_nodejs(...)` inherit `agent.workspace.files_root` unless an
  explicit `root=` or `cwd=` is passed
- treat `enable_*` helper `desc=` values as optional extra guidance by default; use `desc_mode="override"` only when the app intentionally replaces the default capability description
- when changing public helper APIs, use explicit typing for IDE assistance; prefer `Literal` for finite options such as `desc_mode`
- use `@agent.action_func` and `agent.use_actions(...)` as the primary action APIs; `tool_func` and `use_tool` remain compatibility aliases
- use `agent.action.get_action_info()` / `get_tool_info()` for visible schemas;
  agent-scoped Actions, MCP tools, and `enable_*` helpers are included by
  default, while explicit tags narrow the list
- use built-in Search/Browse through `from agently.builtins.actions import Search, Browse` and `agent.use_actions(Search(...))` / `agent.use_actions(Browse(...))`; do not invent `enable_search(...)` or `ActionTools`
- keep built-in implementation on the retained path: `agently.builtins.actions` owns Search/Browse/Cmd behavior; `agently.builtins.tools` should stay a thin legacy facade
- treat `model_digest`, `artifact_refs`, and Workspace record refs as the normal
  loop memory for instruction-heavy Actions; full raw payloads should be read
  explicitly from the Action artifact store or Workspace when needed; use
  `workspace.append_runtime_event(...)` / `workspace.query_runtime_events(...)`
  only for durable execution facts, not as a replacement for TriggerFlow
  pause/resume or approval/exchange policy
- keep the permission profile explicit: search-only, local-files-only, network-read, install-capable shell, or trusted broad executor
- use Python sandbox for pure computation or small data shaping; do not use it for imports, filesystem mutation, network access, or dependency installation
- use Bash sandbox or a custom executor when the task needs shell access, package install, or broader command control
- for Skills Executor work, do not ask apps to execute third-party Skill
  scripts directly. Resolve them to controlled Actions, Bash/Python/Node
  sandboxes, MCP/API bindings, or fallback branches; if no substitute exists,
  return a blocked or approval-required result with a user-facing explanation.
- for Skills Executor or artifact-producing workflows, missing local libraries
  are not a natural degraded-success path; plan a controlled install-capable
  Action or ExecutionEnvironment ensure step, preserve the ActionResult, and
  fail closed if policy denies or installation fails
- treat MCP, Bash, Python sandbox, Node.js, Docker, SQLite, vector-store, browser, and remote-runner lifecycle as Execution Environment concerns when they need managed handles
- Action executors should declare or consume managed resources instead of hiding lifecycle ownership
- treat `agently-devtools` as an optional companion package installed from PyPI, not as a required source checkout
- keep observation or evaluation bridge wiring in the app layer through `Agently.event_center`
- combine with `agently-request` or `agently-triggerflow` only when the scenario needs those layers
- prefer built-in Browse support with Playwright or PyAutoGUI before writing browser or desktop-driving wrappers from scratch

## Anti-Patterns

- do not build a parallel action or tool dispatcher before checking native Action Runtime and MCP support
- do not duplicate ActionRuntime planning prompts in higher layers; delegate
  model-owned action/tool selection to ActionRuntime when registered schemas are
  available
- when the surrounding runtime uses `model_pool`, set
  `action.planning_model_key` to the intended business key so ActionRuntime
  planning uses the same model routing
- do not hide MCP/sandbox/process lifecycle inside a custom ActionExecutor when `Agently.execution_environment` can own the dependency
- do not recommend core manager/provider APIs to ordinary app developers when a built-in Action or Agent Component is the right surface
- do not create a custom waiter or auto-function shim first
- do not ask users to clone or editable-install DevTools when `pip install agently-devtools` is the supported public path
- do not build a custom runtime upload bridge before checking `ObservationBridge`

## Action Loop Recall

For `run_bash`, `run_python`, `run_nodejs`, `query_sqlite`, `browse`, `search`,
and similar explicit-instruction Actions, later model rounds should receive a
compact digest rather than full raw code, command output, SQL result sets, page
HTML, screenshots, or logs.

Use the digest for normal planning and replies. Read redacted raw details only
when the model or application asks for them:

```python
artifact_ref = records[0]["artifact_refs"][0]
raw = agent.action.read_action_artifact(
    artifact_id=artifact_ref["artifact_id"],
    action_call_id=artifact_ref["action_call_id"],
)
```

## Example Guidance

Current Action Runtime examples live under `examples/action_runtime/`,
`examples/builtin_actions/`, and `examples/execution_environment/`. Recommended
model-backed cookbook patterns live under `examples/cookbook/`, including Action
loop, router, concurrent todo, reflection, and safe shell policy examples.
Historical built-in tool examples live under `examples/archived/builtin_tools/`
and should point readers back to the current Action-first examples.

New or updated action examples must be runnable in their declared environment
and include an `Expected key output` comment. For model-backed examples, document
the stable action/result shape rather than an exact natural-language response.
Recommended model-app examples must exercise real model-owned decisions through
DeepSeek or local Ollama. Do not replace planners, routers, decomposers,
evaluators, revisers, action selectors, or response generators with deterministic
local substitutes.

## Read Next

- `references/overview.md`
- `references/devtools.md`

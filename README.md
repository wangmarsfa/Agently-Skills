# Agently Skills

Official installable skills for coding agents working with Agently.

Main framework repository: <https://github.com/AgentEra/Agently>  
Official documentation: <https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## Compatibility

The default public catalog is the current Agently-Skills generation `v2`, aligned
with the Agently 4.1.3 runtime line and the compact 6-skill structure.

Machine-readable compatibility support lives in `compatibility/support.json`.
For unpublished cross-repo work, match the active Agently development
compatibility target.

For unpublished work, match companion protocols and catalog generation first:

- authoring protocol: `agently-skills.authoring.v2` (`SKILL.md` standard only)
- DevTools guidance protocol: `agently-skills.devtools-guidance.v1`
- current catalog generation: `v2`
- recommended bundle: `app`

For a published framework release, follow the compatibility registry entry for
that Agently release.

## What Is Agently?

Agently is a framework for building model-powered applications and workflows.

It provides native surfaces for:

- async-first model requests, streaming consumption, and web-service integration
- model setup and provider settings
- prompt composition and prompt config
- structured output and required-key enforcement
- response reuse, metadata access, and streaming consumption
- Action Runtime, tools, MCP, memory, and knowledge-base flows
- lifecycle-aware workflow orchestration through TriggerFlow
- first-class Dynamic Task DAG planning, validation, and execution
- optional developer tooling through `agently-devtools`

## What Is Agently-Skills?

Agently-Skills is the official skills package for coding agents that need to
build with Agently.

It is not the same thing as the framework-side **Skills Executor** that lives
inside the Agently runtime:

- `Agently-Skills` — guidance bundles for coding agents such as Codex and Claude Code
- Agently `Skills Executor` — framework runtime capability for apps and agents to expose declarative skill cards, produce `SkillExecutionPlan` objects, and execute selected skill behavior loops through Agent APIs, Actions, and managed execution environments

In the Agently 4.1.3 runtime line, the runtime facade is
`Agently.skills_executor` with a core facade plus builtin `SkillsExecutor`
plugin implementation. No `Agently.skills` compatibility alias was shipped, so
guidance should keep `Agently.skills_executor` as the global facade.
App code should declare installed ids or remote source selectors on
`agent.use_skills(...)` and let the Skills Executor lazily
discover, install, and mount selected capabilities. Use
`install_skills_pack(...)` for prewarming, offline mirrors, deterministic CI
fixtures, and explicit registry maintenance. Use `install_skills(...)` for one
local Skill directory during authoring and smoke tests, and
`agent.run_skills_task(...)` when the app must explicitly execute a Skill
behavior loop. Remote install metadata records source URL, ref, resolved commit,
subpath, trust level, and checksums; bundled scripts are resources and are not
executed by installation. The default runtime strategy remains `single_shot`;
`effort="normal"` runs the full preflight -> research -> plan -> execute ->
verify -> reflect -> finalize runtime chain, and `effort="max"` increases retry
budget for that chain. `execution: staged`, `allowed-tools`, and effort presets
can route selected Skills through TriggerFlow-backed staged/react execution that
delegates action work to ActionFlow/ActionRuntime. When the built-in profiles
are not enough, use `Agently.skills_executor.register_effort_strategy(name,
handler)` so an `effort=` value can route to an application-provided strategy
that still composes model requests, ActionRuntime/MCP, ExecutionEnvironment,
TriggerFlow, or Dynamic Task through the Agent context. Strategy handlers follow
the `SkillsEffortStrategyHandler` protocol (`context`, `task`, `plan`,
`output_format`, `effort`, `effort_config` keyword arguments); builtins
`single_shot`, `runtime_chain`, `staged`, and `react` are exposed through the
same strategy table and may be inspected with `list_effort_strategies()`. Their
reference implementations live under the Agently builtin Skills Executor
`modules/effort_strategies/` package.

The 4.1.2.x fulfillment line changes the recommended chain-style mental model:
`agent.use_skills(...).input(...).start()` is route-candidate registration for
default Agent auto-orchestration, not prompt-only guidance injection by default.
When the route does not select Skills, ordinary model responses should receive
only safe capability summaries. Use the explicit compatibility setting only
when an application intentionally needs the older prompt-only Skills disclosure
behavior.
Submitted Dynamic Task and required Skills routes remain deterministic; when
multiple optional candidates are present, model-owned route choice is the
default.
Framework-side auto-orchestration should be described as an `AgentOrchestrator`
plugin protocol boundary: core owns the public Agent entrypoint, while the
active orchestrator plugin owns route planning, execution, and process stream
bridging.

For multi-model applications, recommend `agent.activate_model("ollama-qwen2.5")`
to switch the default model key for subsequent Agent-owned requests, and
`agent.create_request(model_key="deepseek-v4")` for one-off overrides. Model
aliases should be concrete and switchable, then resolved through
`model_pool -> model_profiles -> api_key_pools`. API keys are selected at
request time by the pool `selection` strategy (`fixed`, `random`,
`round_robin`, `least_used`; legacy `key_pool_strategy` remains accepted).
Provider-error failover is opt-in through `api_key_pools.<pool>.failover`;
without it, provider errors are surfaced without trying another key.
`OpenAICompatible` still retries transient transport disconnects before output
starts with the same model, prompt, and output format according to
`OpenAICompatible.request_retry`.

The companion repo stays a coding-agent package. It does not become a runtime
dependency of Agently applications.

Individual skill directories are standard `SKILL.md` packages. Agently's
framework-side Skills Executor can install them as local runtime skill sources
when a project intentionally wants runtime steering or design guidance. In that
case the skill contributes its `SKILL.md` instructions, a descriptive decision
card, resource indexes, and install metadata; it does not become a standalone
`skill.run()` runtime or an Agently-authored workflow manifest.
For 4.1.x auto-orchestration, `agent.use_skills(...)` should be treated as a
route candidate. Full primary `SKILL.md` guidance belongs to the Skills route
that actually executes against that Skill; package scripts and helpers still
remain inert assets unless the app binds them through controlled Actions or
ExecutionEnvironment-managed resources.

When a runtime Skill references helper scripts or shell-like capabilities,
Agently must treat those files as resources. The host application may expose
explicit controlled Actions or ExecutionEnvironment-managed tools, but the
Skills Executor must not execute third-party package scripts directly or create
a parallel approval/resume system outside TriggerFlow and Action Runtime.

## Routing Model

The default catalog contains 6 public skills:

- `agently-playbook`
  Top-level router for unresolved model-powered product, assistant,
  internal-tool, automation, evaluator, workflow, or project-structure refactor
  requests.
- `agently-request`
  Request-side model setup, provider settings, prompt management, structured
  output, response reuse, streaming consumption, session memory, embeddings,
  knowledge-base indexing, retrieval, and retrieval-backed answers.
- `agently-runtime`
  Action Runtime, built-in action packages, tool compatibility, MCP,
  Execution Environment lifecycle, service exposure, auto-function helpers,
  `KeyWaiter`, and optional `agently-devtools` integration.
- `agently-dynamic-task`
  Dynamic Task DAG planning, `TaskDAG` validation, resolver handlers, and
  `TaskDAGExecutor` execution through `Agently.create_dynamic_task(...)`.
- `agently-triggerflow`
  Explicit orchestration, branching, concurrency, approvals, waiting and resume,
  runtime stream, restart-safe execution, mixed sync/async function or module
  orchestration, and graph-friendly workflow definitions.
- `agently-migration`
  Migration from LangChain, LangGraph, LlamaIndex, CrewAI, or similar systems
  into Agently-native request/runtime or TriggerFlow layers.

Use this mental model when choosing a skill:

- If the request starts from business goals, product behavior, refactor intent,
  or an unclear owner layer, start with `agently-playbook`.
- If the request stays inside one request family, route to `agently-request`.
- If the request needs model-callable capabilities, managed execution
  dependencies, service exposure, or DevTools wiring, route to
  `agently-runtime`.
- If the request needs model-generated or app-submitted DAG data to be planned,
  validated, pruned, and executed, route to `agently-dynamic-task`.
- If the request needs explicit orchestration, route to `agently-triggerflow`.
- If the request is a framework migration, route to `agently-migration`.
- Prefer native Agently surfaces before custom wrappers, custom parsers, custom
  retry loops, or custom workflow infrastructure.
- Apply Occam's razor when shaping guidance: do not add a new entity, method,
  facade, or compatibility patch when an existing Agently surface already carries
  the concept clearly; prefer a narrow alias or docs clarification for unclear names.

Async should usually be the default execution stance:

- prefer async APIs for service code, streaming, TriggerFlow, tool concurrency,
  and any path that may benefit from overlap or cancellation
- treat sync APIs as convenience wrappers for local scripts, teaching examples,
  or compatibility bridges
- if the solution will live behind HTTP, SSE, WebSocket, or a long-running
  worker, assume async-first unless a concrete constraint proves otherwise

## Post-4.1 Defaults

When skills describe the recommended path for Agently `4.1+`, they should
converge on these defaults:

- API shape: apply Occam's razor before adding methods, facades, or compatibility
  patches. If the existing surface is semantically correct but unclear, propose a
  narrow alias or documentation clarification instead of another overlapping API.
- structured output: fixed required leaves belong in tuple `ensure` form inside
  `.output(...)`; runtime `ensure_keys` is for conditional or runtime-dependent
  paths. Omitted `.output(..., format=...)` reads
  `prompt.default_output_format`, whose framework default is `json`; agents or
  requests may set that default independently. Explicit `format="auto"` or
  `prompt.default_output_format="auto"` uses structural selection: flat
  string-only dict schemas resolve to `xml_field`; dict schemas that mix string
  fields with typed non-string fields resolve to `hybrid`; and all-control,
  all-complex schemas, and non-dict outputs resolve to `json`. `yaml_literal`
  is explicit opt-in, and `flat_markdown` is explicit-only compatibility mode.
  Prefer explicit `format="json"` for dense all-typed data or legacy JSON-only
  contracts; explicit `format="xml_field"` for flat string-only dict schemas
  when XML-like boundaries fit; explicit `format="hybrid"` for mixed long text
  plus typed fields after provider/model stability checks; and no
  `.output(...)` for one freeform plain-text artifact. Tuple ensure requires
  meaningful values: blank strings, empty wildcard matches, and wildcard matches
  containing blank required values fail, while `False` and `0` remain valid.
  `max_retries=3` can recover ordinary parse/key omissions with up to
  three additional model attempts, but complex nested arrays, placeholder echo,
  prose in boolean/numeric fields, and many wildcard ensure paths can still
  fail after retries. Use `instant` streaming for provisional structured
  UI/progress updates on `json`/`flat_markdown`/`hybrid`/`xml_field`/
  `yaml_literal`/resolved `auto`; use `delta` streaming for plain text.
  Recent qwen2.5:7b checks found `hybrid` can omit section headers or echo old
  scaffold comments into text fields, so do not make `auto`/`hybrid` the
  default for untested local models.
- model-output tests: use an Agently model judge with output control for
  content-level semantic validation. Pass the candidate output, explicit rules,
  expected contracts, and context into the judge; ask for per-rule evidence and
  concise reason before final boolean fields; assert those booleans. Avoid
  keyword, substring, regex, and text snapshot checks as the primary correctness
  signal for model-owned semantic content.
- scenario routing: do not use tokenization, word segmentation, keyword hits,
  substring rules, or regex as the owner for AI-app scenario routing, intent
  detection, or business classification. Use an appropriately sized model with
  an Agently output schema: smaller or local models are fine for simple
  decisions, while many labels, interacting rules, ambiguity, high risk, or
  complex returned structures call for a larger model.
- framework gaps: when application work shows missing framework capability,
  behavior that conflicts with docs, examples, Skills guidance, or business
  intuition, an API that is unavailable or unfriendly, or a responsibility that
  Agently should own but business code must patch with workarounds or glue,
  produce a concise issue report and recommend filing it at
  `https://github.com/AgentEra/Agently/issues`. For manual filing, give the
  user the issue content and filing method. The issue must explain the concrete
  scenario; if business details are confidential, anonymize them but still state
  what kind of model-app development problem, workflow, and framework
  responsibility are involved. Before any manual or automatic filing, redact
  local machine paths, usernames, account names, tokens, private repository or
  workspace names, internal project names, raw logs that contain private prompt
  text, and any other customer or project-private data. Use placeholders such as
  `<workspace>`, `<repo>`, `<task-file>`, and `outputs/debug/<turn-id>.jsonl`.
  Ask before automatic filing; then verify GitHub permission/capability,
  reproduce the issue locally, re-check Agently docs, examples, Skills guidance,
  and API usage, and run a privacy scan on the final issue body before
  submitting.
- actions: prefer `@agent.action_func` plus `agent.use_actions(...)`; tool
  aliases remain compatibility surfaces
- TriggerFlow lifecycle: prefer `close()` / `async_close()` and the close
  snapshot; do not present `.end()`, `set_result()`, `get_result()`, or
  `wait_for_result=` as normal new-code entrypoints
- deprecation signal: Agently emits each deprecated API warning once per Python
  process; repeated silence after the first warning does not make legacy APIs
  recommended
- production noise: `runtime.show_deprecation_warnings=False` may silence
  Agently deprecation warnings globally, but skills must still migrate away from
  deprecated APIs instead of treating the silence as approval
- TriggerFlow state: prefer `get_state(...)` / `set_state(...)` for
  per-execution data; treat `flow_data` as intentionally shared and risky
- settings loading: prefer `Agently.load_settings("yaml_file", path,
  auto_load_env=True)` for file-backed provider config; keep
  `Agently.set_settings(...)` for inline overrides
- execution style: default to async-first for services, streaming, and workflows
- response reuse: when one model result must be consumed multiple ways, prefer
  `get_response()` and reuse the same response object
- Dynamic Task: treat `Agently.create_dynamic_task(...)` as the public surface
  for submitted DAGs. TriggerFlow is its execution substrate, not its owner API.
- 4.1.2.x Agent auto-orchestration: treat default `agent.start()` as the accepted
  candidate-driven route owner across ordinary model requests, Actions, Skills
  Executor, and Dynamic Task candidates. Submitted Dynamic Task and required
  Skills remain deterministic; ambiguous optional candidates use model-owned
  route choice. Prefer `agent.create_execution()` for route diagnostics,
  multiple result views, and process streaming.
- Agent quick prompt chains are AgentTurn-local request drafts. A service may
  keep one configured Agent singleton for settings, model activation, Actions,
  Skills, Workspace, and `always=True` prompt, while each
  `agent.input(...).output(...).async_start()` chain owns its own prompt state.
  For multi-statement request setup, use `turn = agent.create_turn()` and mutate
  the turn; do not accumulate request-scoped prompt state on the shared Agent.
- AgentExecution step contract: use default `mode="one_turn"` for compatibility
  and `mode="task_step"` with explicit `lineage=` / `limits=` for bounded
  developer-owned loop steps. Task-step executions are one step, not the loop
  owner; persist observations explicitly through Workspace before building the
  next ContextPack. Inspect `meta["route"]` and `meta["logs"]` for selected
  route, model response ids, ActionRuntime action logs, and artifact refs; use
  those framework-owned records instead of model-restated action stdout when
  persisting business evidence.
- runtime stall control: for bounded AgentExecution steps, prefer
  `limits={"max_seconds": ..., "max_no_progress_seconds": ...}` and catch
  `RuntimeStageStallError`; inspect `meta["diagnostics"]["last_progress"]`,
  `["timeouts"]`, and `["stalls"]`. For provider or final-response hangs, use
  `OpenAICompatible.stream_idle_timeout`,
  `OpenAIResponsesCompatible.stream_idle_timeout`, and
  `response.materialization_idle_timeout` rather than app-level polling.
  Provider first-event and stream-idle stalls are typed runtime stalls, not
  message-parsed `TimeoutError`s. OpenAI-compatible transient disconnects
  before output starts use same-request `OpenAICompatible.request_retry`, not an
  output-format change. Explicit response stream errors should
  propagate from response getters with the original provider or ActionFlow
  reason before materialization timeout is used as a fallback. For
  high-frequency RuntimeEvent deltas, keep
  producers raw and configure expensive EventCenter hooks/hookers with
  `delivery_policy={"mode": "summary", "dispatch": "await", "emit_interval": ...,
  "max_items": ...}`. Use `dispatch="background"` only for best-effort outlets
  that have an explicit EventCenter or bridge flush/close point; EventCenter's
  idle flush safety net helps long-lived loops but does not replace explicit
  flush before CLI/script shutdown.
- debugging Agently runtime behavior: during development, attach an EventCenter
  observation hook or temporarily call `.set_settings("debug", True)` /
  `.set_settings("debug", "detail")` to inspect route selection, model requests,
  ActionRuntime, and Workspace writes. Remove temporary debug hooks/settings
  from examples and production snippets after diagnosis.
- AgentOrchestrator: keep auto-orchestration behind a plugin protocol boundary;
  do not place route-owned Skills or Dynamic Task execution logic directly in
  core or describe facade/mixin coupling as the extension contract.
- process streaming: executor layers should compose TriggerFlow runtime stream
  with ModelRequest `instant` checkpoints for route decisions, plan/graph
  readiness, task/stage/action progress, selected model field deltas, and final
  semantic outputs. Field deltas should use stable structured paths such as
  `task_dag.tasks.<task_id>.fields.<field_path>`, not raw provider token events.

Feature acceptance requires spec reconciliation: update each relevant spec to the
final implemented design, move fully landed planned specs into `spec/implemented/`,
and update `spec/README.md` in the same work item.

Release or feature acceptance arguments must be coverage-first. Start by
listing the target contract from the roadmap, spec, issue criteria,
compatibility manifest, docs, and example rules; then map each requirement to
evidence from real examples, deterministic tests, protocol tests, docs/spec,
compatibility metadata, companion validation, or explicit deferral. Do not claim
completion by pointing directly at existing examples or tests before checking
their coverage against the target.

When reporting API, recommended usage, examples, or compatibility changes,
include concise sample code that shows the updated usage shape. Prefer current
usage snippets or before/after snippets over abstract prose when that makes the
change easier to inspect.

## Standard Project Shape

When an Agently project needs to stay maintainable, initialize or refactor it
around explicit capability boundaries instead of one oversized `app.py`.

The default shape should usually separate:

- `SETTINGS.yaml` or a settings layer for provider config, `${ENV.xxx}`
  placeholders, workflow/search/browse knobs, and other deployment-time switches
- `app/` or another application wiring layer that loads settings, validates
  required env names when needed, chooses async boundaries, and wires tools plus
  the main flow
- `prompts/` for YAML or JSON prompt contracts that own `input`, `info`,
  `instruct`, and `output`
- `services/` for request wrappers, response normalization, and business-facing
  adapters
- `domain/` or `schemas/` for enums, request/response contracts, and shared
  value objects
- `workflow/` for TriggerFlow graphs and chunk implementations
- `dynamic_task/` or service-level modules for Dynamic Task facades, submitted
  DAG contracts, resolver handlers, and planner constraints when the task plan
  is data
- `tools/` for replaceable search, browse, MCP, or external adapters
- `tests/` for settings smoke checks, prompt/response checks, and API or flow
  validation
- `outputs/` and `logs/` for runtime artifacts instead of mixing them into
  source folders
- optional `agently-devtools` wiring in the app or observability layer for local
  observation, evaluation, playground, and logs

A fuller public reference lives in
[`skills/agently-playbook/references/project-framework.md`](skills/agently-playbook/references/project-framework.md).

## Install

Choose the target agent first. The recommended path is to install one bundle
into one agent-specific skill directory, for example Codex:

```bash
export AGENT=codex
```

Use `AGENT=claude`, `AGENT=cursor`, or another supported agent when that is your
actual target.

`app`
Default bundle for building new Agently applications:

```bash
for skill in \
  agently-playbook \
  agently-request \
  agently-runtime \
  agently-dynamic-task \
  agently-triggerflow
do
  npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill "$skill" -y
done
```

`migration`
Bundle for moving existing LangChain, LangGraph, LlamaIndex, CrewAI, or similar
systems into Agently. Install the `app` bundle first, then add the migration
skill:

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently-migration -y
```

Install only the router when you want the smallest possible starting point:

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently-playbook -y
```

Inspect the default public catalog:

```bash
npx skills add . --list
```

The default listing and standard install path expose only the current 6-skill
catalog.

## Legacy V1 Rollback

The previous 12-skill catalog is archived under `legacy/v1/`.

- path: `legacy/v1/skills/`
- bundle manifest: `legacy/v1/bundles/manifest.json`
- compatibility manifest: `legacy/v1/compatibility/support.json`
- last supported Agently framework version: `4.1.1`
- status: frozen

V1 exists only for explicit rollback and historical projects. It does not track
Agently `4.1.2+` compatibility manifests, new Action Runtime guidance,
Execution Environment restructuring, or future catalog protocols. Do not use V1
as the recommended path for new projects.

## Optional Companion Package

Agently keeps `agently-devtools` as an optional developer-tooling companion
package.

```bash
pip install agently-devtools
agently-devtools init my_project
```

- Install: `pip install -U agently agently-devtools`
- Compatibility line: use the Agently compatibility registry for the active
  release or development target
- Public entrypoints: `ObservationBridge`, `EvaluationBridge`,
  `EvaluationRunner`, and `create_local_observation_app`
- Recommended startup: `agently-devtools start`

Use this package when an Agently app needs local runtime observation,
evaluations, logs, or playground support during development and debugging. The
skills package treats this as optional observability tooling, not as a required
source-repo dependency.

Recommended observation wiring binds at bridge creation time and selects scope
with `watch(...)`:

```python
from agently import Agently
from agently_devtools import ObservationBridge

bridge = ObservationBridge(Agently, app_id="your_app_id")
bridge.watch(agent)
```

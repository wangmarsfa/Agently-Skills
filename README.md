# Agently Skills

Official installable skills for coding agents working with Agently.

Main framework repository: <https://github.com/AgentEra/Agently>  
Official documentation: <https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## Compatibility

The default public catalog is the current Agently-Skills generation `v2`, aligned
with the Agently 4.1.2.4 line and the compact 6-skill structure.

Machine-readable compatibility support lives in `compatibility/support.json`.
For unpublished cross-repo work, match the active Agently development
compatibility target.

For unpublished work, match companion protocols and catalog generation first:

- authoring protocol: `agently-skills.authoring.v1`
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
- Agently `Skills Executor` — runtime capability for Agently apps and agents to install and apply external skills during real task execution

In current framework development, the runtime facade is `Agently.skills_executor`
with a core facade plus builtin `SkillsExecutor` plugin implementation.
The framework-side Skills Executor has not shipped yet, so no `Agently.skills`
compatibility alias is retained.
Use `install_skills(...)` for one Agent Skills package,
`install_skills_pack(...)` for repositories that contain multiple Skills, and
`agent.use_skills(...).input(...).start()` for chain-style model-decision usage.

The companion repo stays a coding-agent package. It does not become a runtime
dependency of Agently applications.

Individual skill directories are still plain-text packages. Agently's
framework-side Skills Executor can install them as **guidance-only runtime skill
sources** when a project intentionally wants runtime steering or design
guidance. In that case the skill contributes guidance assets, not a standalone
executable runtime.

When a runtime Skill references helper scripts or shell-like capabilities, the
framework-side executor should resolve them through controlled Actions or
ExecutionEnvironment-managed tools instead of executing third-party package
scripts directly. Current development behavior includes auto-binding
Bash/shell-style requirements to a controlled Bash sandbox when allowed by
policy; if no controlled substitute exists, the executor should fail closed with
a natural-language user message and remediation suggestions.

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
  paths
- model-output tests: use an Agently model judge with output control for
  content-level semantic validation. Pass the candidate output, explicit rules,
  expected contracts, and context into the judge; ask for per-rule evidence and
  concise reason before final boolean fields; assert those booleans. Avoid
  keyword, substring, regex, and text snapshot checks as the primary correctness
  signal for model-owned semantic content.
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

Feature acceptance requires spec reconciliation: update each relevant spec to the
final implemented design, move fully landed planned specs into `spec/implemented/`,
and update `spec/README.md` in the same work item.

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

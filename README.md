# Agently Skills

Official installable skills for coding agents working with Agently.

Main framework repository: <https://github.com/AgentEra/Agently>  
Official documentation: <https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## Compatibility

This catalog is aligned with the Agently 4.1.1 release line and its current TriggerFlow execution lifecycle guidance.

Machine-readable compatibility support lives in `compatibility/support.json`.

For unpublished cross-repo work, match against Agently companion protocols first, not against a future package version that has not been released yet:

- authoring protocol: `agently-skills.authoring.v1`
- DevTools guidance protocol: `agently-skills.devtools-guidance.v1`

The source of truth for a published framework release remains Agently's release registry entry under `../Agently/compatibility/releases/`.
The public next-release development target lives in `../Agently/compatibility/in-development.json`. It currently targets `4.1.1.1`.

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
- optional developer tooling through `agently-devtools`

## What Is Agently-Skills?

Agently-Skills is the official skills package for coding agents that need to build with Agently.

It does more than explain API syntax. It teaches coding agents:

- how to recognize Agently-appropriate scenarios from natural-language product requests
- how to choose the right skill or skill combination
- how to structure projects around Agently-native capability boundaries
- how to apply best-practice project layout, orchestration, and performance refactors
- how to stay inside Agently's design philosophy instead of writing generic glue first

The goal is not shallow snippet generation. The goal is to help a coding agent produce a complete project that actually fits Agently.

For example, a broad request such as `build a travel planning tool on top of local Ollama` should not be treated as just one local model call. The skills should help the coding agent decide the right setup path, prompt structure, workflow shape, and project layout from that natural-language intent.

## Why Use The Official Skills?

- They improve scenario capture for broad, under-specified model-app requests.
- They encode Agently-native best practices instead of generic framework-agnostic habits.
- They include guidance on project layout, routing, performance optimization, and design philosophy.
- They are checked against realistic scenario language instead of relying only on hand-written snippets.

## Routing Model

Use this mental model when choosing a skill:

- If the request starts from business goals, product behavior, refactor intent, or an unclear owner layer, start with `agently-playbook`.
- If the request is already narrow and explicit, route directly to the owning leaf skill.
- Prefer native Agently surfaces before custom wrappers, custom parsers, custom retry loops, or custom workflow infrastructure.

The most important routing rules are:

- unresolved product, assistant, automation, or workflow request -> `agently-playbook`
- provider wiring, env vars, or model settings separation -> `agently-model-setup`
- prompt structure, prompt config, YAML-backed prompt behavior, or config-file prompt bridge -> `agently-prompt-management`
- stable structured fields, required keys, value-level validation, or machine-readable output -> `agently-output-control`
- reuse one response as text, data, metadata, or streaming updates -> `agently-model-response`
- session continuity or restore-after-restart -> `agently-session-memory`
- Action Runtime, tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, Browse with Playwright or PyAutoGUI, or optional `agently-devtools` observation/evaluation tooling -> `agently-agent-extensions`
- embeddings, indexing, retrieval, or KB-to-answer -> `agently-knowledge-base`
- explicit orchestration, TriggerFlow, execution lifecycle control, mixed sync/async execution, event-driven fan-out, process-clarity refactors, graph-friendly workflow definitions, or resumable multi-stage flows -> `agently-triggerflow`
- migration from LangChain or LangGraph -> `agently-migration-playbook`, then the matching migration leaf

Async should usually be the default execution stance:

- prefer async APIs for service code, streaming, TriggerFlow, tool concurrency, and any path that may benefit from overlap or cancellation
- treat sync APIs as convenience wrappers for local scripts, teaching examples, or compatibility bridges
- if the solution will live behind HTTP, SSE, WebSocket, or a long-running worker, assume async-first unless a concrete constraint proves otherwise

## Standard Project Shape

When an Agently project needs to stay maintainable, initialize or refactor it around explicit capability boundaries instead of one oversized `app.py`.

The default shape should usually separate:

- `SETTINGS.yaml` or a settings layer for provider config, `${ENV.xxx}` placeholders, workflow/search/browse knobs, and other deployment-time switches
- `app/` or another application wiring layer that loads settings, validates required env names when needed, chooses async boundaries, and wires tools plus the main flow
- `prompts/` for YAML or JSON prompt contracts that own `input`, `info`, `instruct`, and `output`
- `services/` for request wrappers, response normalization, and business-facing adapters
- `domain/` or `schemas/` for enums, request/response contracts, and shared value objects
- `workflow/` for TriggerFlow graphs and chunk implementations
- `tools/` for replaceable search, browse, MCP, or external adapters
- `tests/` for settings smoke checks, prompt/response checks, and API or flow validation
- `outputs/` and `logs/` for runtime artifacts instead of mixing them into source folders
- optional `agently-devtools` wiring in the app or observability layer for local observation, evaluation, playground, and logs

Two source-backed details matter here:

- Configure Prompt supports placeholder mappings recursively across prompt values and keys. Keep `${topic}`, `${language}`, `${column_title}`, and similar variables in prompt files and inject them through `load_yaml_prompt(..., mappings={...})` or `load_json_prompt(...)`.
- Model settings can keep `${ENV.NAME}` placeholders and let `Agently.load_settings("yaml_file", "...", auto_load_env=True)` resolve them by finding and loading a local `.env` file. If settings are created inline instead of in a file, use `Agently.set_settings(...)`.

Two high-frequency rules prevent common drift:

- keep stable shared output contracts in prompt config rather than scattering them across Python helpers
- keep provider settings under the plugin namespace that the requester actually reads, for example `plugins.ModelRequester.OpenAICompatible.*` or `plugins.ModelRequester.AnthropicCompatible.*`
- keep optional DevTools endpoints and bridge wiring outside prompt files and workflow helpers; use `ObservationBridge`, `EvaluationBridge`, or `create_local_observation_app(...)` from the public `agently-devtools` package instead of repo-specific install guidance

This is the pattern used by `Agently-Daily-News-Collector`: settings stay in `SETTINGS.yaml`, prompt contracts stay in `prompts/`, flow construction stays in `workflow/`, and the app layer does env loading plus Agently wiring.

Project initialization should not be a separate public skill. It belongs to `agently-playbook`: decide the owner layers, create the skeleton, and then hand implementation work to the owning leaf skills.

A fuller public reference lives in [`skills/agently-playbook/references/project-framework.md`](skills/agently-playbook/references/project-framework.md).

## Public Catalog

The public catalog currently contains 12 skills.

### Entry

- `agently-playbook`
  Top-level router for unresolved model-powered product, assistant, internal-tool, automation, evaluator, workflow, or project-structure refactor requests.

### Request Side

- `agently-model-setup`
  Provider connection, dotenv-based settings, model transport setup, and settings-file-based model separation.
- `agently-prompt-management`
  Prompt composition, prompt config, YAML-backed prompt behavior, mappings, and reusable request-side prompt structure.
- `agently-output-control`
  Output schema, field ordering, required keys, value-level validation, and structured output reliability.
- `agently-model-response`
  `get_response()`, parsed results, metadata, streaming consumption, and response reuse.
- `agently-session-memory`
  Session-backed continuity, memo, restore, and request-side conversational state.

### Request Extensions

- `agently-agent-extensions`
  Action Runtime, tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, Browse with Playwright or PyAutoGUI, and optional `agently-devtools` observation/evaluation tooling.
- `agently-knowledge-base`
  Embeddings plus Chroma-backed indexing, retrieval, and retrieval-to-answer flows.

### Workflow

- `agently-triggerflow`
  TriggerFlow orchestration, execution lifecycle, runtime state, runtime stream, workflow-side model execution, event-driven fan-out, process-clarity refactors, mixed sync/async orchestration, and graph-friendly workflow definitions for debugging and visualization.

## Optional Companion Package

Agently 4.1.1 keeps `agently-devtools` as an optional developer-tooling companion package.

```bash
pip install agently-devtools
agently-devtools init my_project    # scaffold a new Agently project
```

- Install: `pip install -U agently agently-devtools`
- Compatibility line: `agently-devtools 0.1.x` targets `agently >=4.1.0,<4.2.0`
- Public entrypoints: `ObservationBridge`, `EvaluationBridge`, `EvaluationRunner`, and `create_local_observation_app`
- Recommended startup: `agently-devtools start`

For release automation and unpublished branch work, treat the Agently compatibility registry as the machine-readable source of truth. This repository only declares which Agently skills protocols it supports.

Use this package when an Agently app needs local runtime observation, evaluations, logs, or playground support during development and debugging. The skills package treats this as optional observability tooling, not as a required source-repo dependency.

### Migration

- `agently-migration-playbook`
  Migration router for existing LangChain or LangGraph systems.
- `agently-langchain-to-agently`
  Direct LangChain agent-side migration guidance.
- `agently-langgraph-to-triggerflow`
  Direct LangGraph orchestration migration guidance.

## Install

Choose the target agent first. The recommended path is to install one bundle into one agent-specific skill directory, for example Codex:

```bash
export AGENT=codex
```

Use `AGENT=claude`, `AGENT=cursor`, or another supported agent when that is your actual target.

`app`
Default bundle for building new Agently applications. It combines the skills normally needed together: core model request setup, TriggerFlow, service and tool wrapping, response handling, output control, session continuity, and knowledge-base guidance.

```bash
for skill in \
  agently-playbook \
  agently-model-setup \
  agently-prompt-management \
  agently-output-control \
  agently-model-response \
  agently-agent-extensions \
  agently-session-memory \
  agently-knowledge-base \
  agently-triggerflow
do
  npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill "$skill" -y
done
```

`migration`
Bundle for moving existing LangChain, LangGraph, LlamaIndex, CrewAI, or similar systems into Agently. Install the `app` bundle first, then add the migration skills:

```bash
for skill in \
  agently-migration-playbook \
  agently-langchain-to-agently \
  agently-langgraph-to-triggerflow
do
  npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill "$skill" -y
done
```

Install only the router when you want the smallest possible starting point:

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently-playbook -y
```

Advanced multi-agent install:

```bash
npx skills add AgentEra/Agently-Skills --all
```

`--all` intentionally installs across all detected agents. In repositories where several coding agents are configured, that can create multiple hidden directories such as `.agents/`, `.claude/`, `.cursor/`, and `.codex/`, so it is no longer the default recommendation.

The machine-readable bundle definitions live in `bundles/manifest.json`.

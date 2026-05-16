---
name: agently-skills-catalog
description: Central catalog and documentation for Agently Skills V2. Use when working with Agently skill installation, routing, and installed-skill usage guidance.
---

# Agently Skills Catalog

This package publishes the current Agently Skills catalog generation `v2` under
`skills/`. The frozen V1 catalog is archived under `legacy/v1/` and is not part
of default installation, routing, or bundle guidance.

Use this file as installation-time guidance after the skills are added into another project or agent environment.

## Usage Priorities

- Route unresolved product, assistant, and workflow requests through `agently-playbook` first.
- Prefer Agently-native capabilities before custom output parsers, retry loops, or orchestration layers.
- Default to async-first guidance for services, streaming, TriggerFlow, and concurrent execution. Treat sync APIs as wrappers for scripts, REPL use, or compatibility bridges unless there is a clear reason not to.
- Treat `agently-devtools` as an optional companion package installed from PyPI, not as a required source-repo dependency.
- Keep public skill boundaries capability-first and mutually exclusive.
- Treat multi-agent, judge, and review flows as scenario recipes unless they need a dedicated framework surface.
- Treat `catalog_generation` and `recommended_bundle` as compatibility fields
  that must stay aligned with `../Agently/compatibility/in-development.json`.
- Do not recommend `legacy/v1/` for new projects; it exists only for explicit
  rollback or historical projects.

## Source Alignment Rule

- This repository is the official companion guidance repository for `github.com/AgentEra/Agently`.
- Skills must follow Agently public APIs, recommended usage, deprecation policy, and runtime behavior.
- Machine-readable compatibility support lives in `compatibility/support.json` and must stay aligned with the Agently release registry under `../Agently/compatibility/`.
- Do not present deprecated Agently APIs as the default path. Deprecated APIs may appear only in explicit legacy or migration notes.
- When Agently changes a public API, runtime behavior, or recommendation, update affected Skills guidance, examples, fixtures, and validation rules in the same work item.

## Companion Change Rule

- TriggerFlow changes require checking `skills/agently-triggerflow/`,
  `skills/agently-playbook/references/project-framework.md`, route fixtures,
  reference fixtures, native usage validation, and README guidance.
- Action Runtime, ModelResponse, Session, FastAPIHelper, settings, prompt
  config, tools, MCP, knowledge-base, and DevTools integration changes require
  the same companion impact review through `skills/agently-request/` and
  `skills/agently-runtime/`.
- If the Agently source repository is unavailable, record that source alignment could not be verified.

## Examples Validation

- Agently recommended examples, cookbook examples, public teaching examples, and training-derived examples must exercise a real model through DeepSeek or local Ollama.
- DeepSeek credentials may be loaded through dotenv by the example itself. Do not mark DeepSeek unavailable only because `DEEPSEEK_API_KEY` is absent from the parent shell environment.
- Model-owned planner, router, decomposer, evaluator, reviser, action selector, and response generator behavior must not be replaced with mock, deterministic, or hand-written local substitutes.
- Local functions may be used only as business capabilities, Actions, fake external systems, executor/provider smoke targets, or deterministic resources called by the model-driven flow.
- Low-level infrastructure smoke examples may run without a model only when they are explicitly scoped to executor/provider behavior and are not presented as model-app patterns.
- Every recommended model-app example must include an `Expected key output` source comment that records stable key results from a real run.
- Do not invent example outputs. Re-run the example with DeepSeek or local Ollama and update the comment when model behavior materially changes.

## Validation Rule

- After changing skill content, run the relevant validation scripts under `validate/`.
- Run `python validate/validate_compatibility.py` whenever compatibility guidance, release-line claims, or DevTools integration guidance changes.
- At minimum for TriggerFlow guidance changes, run `python validate/validate_catalog.py`, `python validate/validate_bundle_manifest.py`, `python validate/validate_native_usage.py`, `python validate/validate_trigger_paths.py`, and `python validate/validate_reference_retrieval.py` when model/runtime credentials are available.
- Validation should fail if recommended TriggerFlow examples use deprecated lifecycle, result, runtime-data, or flow-data APIs outside an explicit legacy allowlist.
- Validation should fail if the default catalog contains anything other than the
  current 5 public skills, or if default bundles reference `legacy/v1/`.

## Project Defaults

- Prefer separating `settings/`, `prompts/`, `services/`, `domain/` or `schemas/`, `workflow/`, `tools/`, and `tests/` when the project is more than a tiny demo.
- Keep stable shared prompt and output contracts in prompt config rather than scattering them across Python helpers.
- Keep provider settings under the namespace actually read by the active plugin. For `OpenAICompatible`, prefer `plugins.ModelRequester.OpenAICompatible.*`.
- Prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)` for file-backed settings. Use `Agently.set_settings(...)` for inline overrides.
- Keep optional DevTools wiring in the integration layer through `ObservationBridge`, `EvaluationBridge`, or `create_local_observation_app` instead of scattering debug hooks across workflow code.

## Skill Routing Reminders

- `agently-playbook`: unresolved owner layer, project shape, or broad product request
- `agently-request`: provider wiring, env placeholders, model settings, prompt config, structured output, response reuse, session memory, embeddings, and retrieval
- `agently-runtime`: Action Runtime, tools, MCP, Execution Environment, FastAPIHelper, `auto_func`, `KeyWaiter`, and optional `agently-devtools` observation, evaluation, and playground integration
- `agently-triggerflow`: explicit orchestration, branching, concurrency, runtime stream, workflow-owned business events, and execution-graph-friendly workflow definitions
- `agently-migration`: migration from LangChain, LangGraph, LlamaIndex, CrewAI, or similar systems into Agently-native layers

## Anti-Patterns

- Do not treat sync sample code as the default architecture for async-capable services.
- Do not expose raw model parser paths directly to the UI when the workflow can translate them into stable business events.
- Do not keep provider auth, model name, or base URL in ad hoc Python literals when settings plus `${ENV.xxx}` placeholders fit.
- Do not tell users to clone or editable-install the private DevTools source when the public package `pip install agently-devtools` already matches the supported integration path.

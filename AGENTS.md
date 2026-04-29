---
name: agently-skills-catalog
description: Central catalog and documentation for Agently Skills V2. Use when working with Agently skill installation, routing, and installed-skill usage guidance.
---

# Agently Skills Catalog

This package publishes the Agently Skills V2 catalog under `skills/`.

Use this file as installation-time guidance after the skills are added into another project or agent environment.

## Usage Priorities

- Route unresolved product, assistant, and workflow requests through `agently-playbook` first.
- Prefer Agently-native capabilities before custom output parsers, retry loops, or orchestration layers.
- Default to async-first guidance for services, streaming, TriggerFlow, and concurrent execution. Treat sync APIs as wrappers for scripts, REPL use, or compatibility bridges unless there is a clear reason not to.
- Treat `agently-devtools` as an optional companion package installed from PyPI, not as a required source-repo dependency.
- Keep public skill boundaries capability-first and mutually exclusive.
- Treat multi-agent, judge, and review flows as scenario recipes unless they need a dedicated framework surface.

## Source Alignment Rule

- This repository is the official companion guidance repository for `github.com/AgentEra/Agently`.
- Skills must follow Agently public APIs, recommended usage, deprecation policy, and runtime behavior.
- Do not present deprecated Agently APIs as the default path. Deprecated APIs may appear only in explicit legacy or migration notes.
- When Agently changes a public API, runtime behavior, or recommendation, update affected Skills guidance, examples, fixtures, and validation rules in the same work item.

## Companion Change Rule

- TriggerFlow changes require checking `skills/agently-triggerflow/`, `skills/agently-playbook/references/project-framework.md`, `skills/agently-langgraph-to-triggerflow/`, route fixtures, reference fixtures, native usage validation, and README guidance.
- Action Runtime, ModelResponse, Session, FastAPIHelper, settings, prompt config, tools, MCP, knowledge-base, and DevTools integration changes require the same companion impact review.
- If the Agently source repository is unavailable, record that source alignment could not be verified.

## Validation Rule

- After changing skill content, run the relevant validation scripts under `validate/`.
- At minimum for TriggerFlow guidance changes, run `python validate/validate_catalog.py`, `python validate/validate_bundle_manifest.py`, `python validate/validate_native_usage.py`, `python validate/validate_trigger_paths.py`, and `python validate/validate_reference_retrieval.py` when model/runtime credentials are available.
- Validation should fail if recommended TriggerFlow examples use deprecated lifecycle, result, runtime-data, or flow-data APIs outside an explicit legacy allowlist.

## Project Defaults

- Prefer separating `settings/`, `prompts/`, `services/`, `domain/` or `schemas/`, `workflow/`, `tools/`, and `tests/` when the project is more than a tiny demo.
- Keep stable shared prompt and output contracts in prompt config rather than scattering them across Python helpers.
- Keep provider settings under the namespace actually read by the active plugin. For `OpenAICompatible`, prefer `plugins.ModelRequester.OpenAICompatible.*`.
- Prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)` for file-backed settings. Use `Agently.set_settings(...)` for inline overrides.
- Keep optional DevTools wiring in the integration layer through `ObservationBridge`, `EvaluationBridge`, or `create_local_observation_app` instead of scattering debug hooks across workflow code.

## Skill Routing Reminders

- `agently-playbook`: unresolved owner layer, project shape, or broad product request
- `agently-model-setup`: provider wiring, env placeholders, model settings, namespace placement, and connectivity checks
- `agently-prompt-management`: prompt config, mappings, reusable request contracts, and prompt-side output contracts
- `agently-output-control`: structured output shape, required keys, reliability, and structured streaming
- `agently-model-response`: response reuse, async getters, metadata, and stream consumption
- `agently-agent-extensions`: Action Runtime, tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, and optional `agently-devtools` observation, evaluation, and playground integration
- `agently-triggerflow`: explicit orchestration, branching, concurrency, runtime stream, workflow-owned business events, and execution-graph-friendly workflow definitions

## Anti-Patterns

- Do not treat sync sample code as the default architecture for async-capable services.
- Do not expose raw model parser paths directly to the UI when the workflow can translate them into stable business events.
- Do not keep provider auth, model name, or base URL in ad hoc Python literals when settings plus `${ENV.xxx}` placeholders fit.
- Do not tell users to clone or editable-install the private DevTools source when the public package `pip install agently-devtools` already matches the supported integration path.

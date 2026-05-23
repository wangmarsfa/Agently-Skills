---
name: agently-playbook
description: Use when the user wants to build, initialize, validate, optimize, or refactor a model-powered assistant, internal tool, automation, evaluator, or workflow from a business scenario or common problem statement, including project-structure refactors or starter skeletons that may separate model setup, prompt config, and orchestration, even if the request also mentions a UI, app shell, or local model service such as Ollama, and it is still unclear whether the solution should stay a single request, add supporting capabilities, or become orchestration. The user does not need to mention Agently explicitly.
---

# Agently Playbook

Use this skill first when the request still starts from business goals, refactor goals, product behavior, or broad model-app language.

The user does not need to say Agently, TriggerFlow, or any other framework term. Generic asks such as "build an assistant", "help me design an internal tool", or "create a validator for common problems" should still start here when the owner layer is unresolved.

Requests that also mention a UI, a web page, a desktop shell, or a local model service such as Ollama should still start here when the request is fundamentally about shaping a model-powered tool rather than only wiring one narrow capability.

## Workflow

1. Reduce the request into scenario and atomic goals.
2. If the request is a project initialization or structure refactor, choose the owner layers, async boundary, and repo skeleton first.
3. Choose the narrowest native Agently capability path.
4. Name the concrete operations or primitives that should be used.
5. Name the validation rule that proves the design stayed native-first.

## Native-First Rules

- default to async-first guidance for service code, streaming, TriggerFlow, and any path that may overlap work or benefit from cancellation
- treat sync APIs as wrappers for scripts, REPL use, or compatibility bridges unless the host truly requires sync-only integration
- when the request is a project-shape refactor, separate settings, prompts, services, domain contracts, workflow, and tests before discussing low-level implementation details
- when a project must test model-generated semantic content, design the test as
  an Agently model-judge request with output control: explicit rules and context
  go in, per-rule evidence/reason and final boolean fields come out, and tests
  assert those booleans
- for model-app evaluation, grading, confidence, relevance, or quality
  judgments, prefer explicit conceptual levels and definitions over direct
  numeric scores. If later workflow logic needs thresholds or aggregate metrics,
  map those levels to deterministic numeric values in code after the model
  response.
- route complex arithmetic, long-number computation, weighting, aggregation, or
  statistical work through executable code or tools; use the model to produce or
  review the calculation plan, not to be the calculator.

## Capability Routing

- model setup, prompt management, output control, response reuse, session memory, embeddings, KB, or retrieval-to-answer -> `agently-request`
- Action Runtime, built-in actions, tools compatibility, MCP, Execution Environment, FastAPIHelper, `auto_func`, `KeyWaiter`, or `agently-devtools` observation and evaluation integration -> `agently-runtime`
- model-generated or app-submitted DAG planning, TaskDAG validation, resolver handlers, or Dynamic Task execution -> `agently-dynamic-task`
- branching, concurrency, waiting/resume, mixed sync/async orchestration, event-driven fan-out, process-clarity refactors, runtime stream, graph-friendly workflow definitions, or explicit multi-stage quality loops -> `agently-triggerflow`
- migration choice between LangChain and LangGraph -> `agently-migration`

## Anti-Patterns

- do not skip this playbook when the owner layer is unresolved
- do not invent custom output parsers, retry loops, or orchestration first
- do not use keyword, substring, regex, or text snapshot checks as the primary
  correctness signal for model-owned semantic content; keep them only as smoke
  gates for structure, routing, or required-field presence
- do not let sync-first sample code dictate the service architecture when the target is clearly async-capable
- do not split project initialization into a fake standalone framework surface before the owner layers are chosen
- do not treat multi-agent, judge, or review flows as separate framework surfaces before checking native Agently capabilities

## Read Next

- `references/capability-map.md`
- `references/project-framework.md`

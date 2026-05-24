# Dynamic Task Overview

Dynamic Task is Agently's framework-level surface for dynamic DAG execution.
It belongs above TriggerFlow conceptually:

```text
Agently.create_dynamic_task(...)
        |
        v
DynamicTask facade
        |
        +-- AgentlyTaskDAGPlanner
        +-- TaskDAGValidator
        +-- DynamicTaskResolver
        +-- TaskDAGExecutor
                |
                v
          TriggerFlow execution substrate
```

Layer ownership:

- `TaskDAG` and `TaskDAGNode` are data contracts under `agently.types.data`;
  reviewed DAGs can be loaded with `TaskDAG.from_yaml(...)` or
  `TaskDAG.from_json(...)`.
- `AgentlyTaskDAGPlanner` is a plugin and owns planner output schema,
  `ensure_keys`, model instructions, and retry validation wiring.
- `TaskDAGValidator`, `DynamicTaskResolver`, and `TaskDAGExecutor` are core
  runtime owners.
- `Agently.create_dynamic_task(...)` and `agent.create_dynamic_task(...)` are
  the app-facing facade entrypoints.

Use Dynamic Task when the graph is submitted as data and must be planned,
validated, pruned, and executed. Use TriggerFlow directly when the developer
owns a stable workflow topology in code.

The executor does not require an Agent instance. Agent or model-provider access
belongs to the facade, planner, model adapter, or resolver handler. That keeps
the core executor reusable for submitted local DAGs, model DAGs, action DAGs,
and future Skills Executor integration.

For model tasks, keep result control on the model task contract. Use
`inputs.output_schema` for the task result shape and `inputs.output_format` for
the response-control strategy: `json` for compact machine-control data,
booleans, numbers, judges, dense nested arrays/objects, and strict extraction;
`flat_markdown` for flat string long text/code/HTML/Markdown fields; explicit
`hybrid` for long prose with structured evidence or metadata when retry latency
is acceptable; and `auto` only when structural schema-driven selection and
retry latency are acceptable.

Submitted DAG `inputs` support runtime placeholders for simple wiring:
`${INPUT}` / `${INPUT.foo}` read graph input, `${DEPS.task_id.path}` reads
dependency results, and `${STATE...}` is a compatibility alias for `${DEPS...}`.
Whole-string placeholders preserve the original value type; embedded
placeholders stringify into the surrounding text. Use placeholders for direct
references, and keep larger transformations in handlers or model tasks.

When a submitted DAG runs behind `agent.use_dynamic_task(...).create_execution()`,
`${INPUT...}` reads graph input from `use_dynamic_task(graph_input=...)` when it
is provided. If omitted, it reads the execution prompt snapshot `input` slot
captured by `create_execution()`, then falls back to `{"target": task_target}`.
Use the explicit `graph_input` argument only when the DAG input should differ
from the Agent prompt input or when the precedence should be visible in code.

When Dynamic Task runs behind `agent.create_execution()`, the Agent execution
stream bridges the underlying TriggerFlow runtime stream. If a DAG chunk fails,
the Agent stream must terminate and surface the original error to the consumer;
do not add external timeout workarounds or swallow failing chunks in examples.

Recommended API boundaries:

- app code: `Agently.create_dynamic_task(...)` or `agent.create_dynamic_task(...)`
- planner control: `AgentlyTaskDAGPlanner`
- graph validation: `TaskDAGValidator`
- handler lookup: `DynamicTaskResolver`
- execution integration: `TaskDAGExecutor`

For Skills Executor work, use Dynamic Task as the DAG substrate rather than
placing Skills execution under TriggerFlow directly. Skills execution may
provide resolver handlers, skill adapters, or facade defaults, but the public
concept remains Dynamic Task.

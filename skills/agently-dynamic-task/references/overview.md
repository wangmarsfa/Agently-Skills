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

Use Dynamic Task when the graph is submitted as data and must be planned,
validated, pruned, and executed. Use TriggerFlow directly when the developer
owns a stable workflow topology in code.

The executor does not require an Agent instance. Agent or model-provider access
belongs to the facade, planner, model adapter, or resolver handler. That keeps
the core executor reusable for submitted local DAGs, model DAGs, action DAGs,
and future Skills Executor integration.

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

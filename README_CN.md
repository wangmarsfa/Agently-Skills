# Agently Skills

面向 coding agents 的 Agently 官方可安装 Skills 仓库。

主仓库：<https://github.com/AgentEra/Agently>  
官方文档：<https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## 兼容性

默认公开 catalog 是当前 Agently-Skills generation `v2`，已按 Agently 4.1.3
runtime 能力线和新的 6-skill 结构对齐。

机器可读兼容声明位于 `compatibility/support.json`。未发布跨仓协作应匹配
当前 Agently development compatibility target。

未发布工作应优先匹配 companion protocols 和 catalog generation：

- authoring protocol：`agently-skills.authoring.v2`（仅标准 `SKILL.md`）
- DevTools guidance protocol：`agently-skills.devtools-guidance.v1`
- 当前 catalog generation：`v2`
- 推荐 bundle：`app`

已发布框架版本应遵循对应 Agently release 的 compatibility registry。

## 什么是 Agently？

Agently 是一个用于构建模型应用和工作流的框架。

它提供的原生能力面包括：

- 异步优先的模型请求、streaming 消费与服务集成
- 模型接入和 provider settings
- Prompt 组合与 prompt config
- 结构化输出与 required keys 约束
- 响应复用、metadata 读取与 streaming 消费
- Action Runtime、tools、MCP、memory、knowledge-base 等扩展能力
- 一等 Dynamic Task DAG 规划、校验和执行
- 基于 TriggerFlow 的 lifecycle-aware 工作流编排
- 通过 `agently-devtools` 提供的可选开发者工具能力

## 什么是 Agently-Skills？

Agently-Skills 是面向 coding agents 的 Agently 官方 Skills 套件。

它和 Agently 框架运行时里的 **Skills Executor** 不是一回事：

- `Agently-Skills` —— 给 Codex、Claude Code 等 coding agent 用的指导型 skill 包
- Agently `Skills Executor` —— Agently app / agent 暴露 declarative skill cards、生成 `SkillExecutionPlan`，并通过 Agent API、Actions 和受管理执行环境运行所选 skill behavior loop 的框架 runtime 能力

Agently 4.1.3 runtime 能力线中的运行时 facade 是 `Agently.skills_executor`，
底层是 core facade 加 builtin `SkillsExecutor` plugin 实现。框架没有发布
`Agently.skills` 兼容别名，因此 guidance 应继续把 `Agently.skills_executor`
作为全局 facade。
应用代码应在 `agent.use_skills(...)` 上声明已安装 id 或远程 source selector，
由 Skills Executor 按需轻量发现、安装并挂接选中的
能力。`install_skills_pack(...)` 保留给预热、离线镜像、确定性 CI fixture 和显式
registry 维护。`install_skills(...)` 用于单个本地 Skill 目录的作者开发和 smoke
test；当应用必须显式执行 Skill behavior loop 时，使用
`agent.run_skills_task(...)`。远程安装元数据会记录 source URL、ref、解析后的
commit、subpath、trust level 和 checksums；包内 scripts 是资源，安装时不会执行。默认
runtime strategy 仍是 `single_shot`；`effort="normal"` 固定走 preflight ->
research -> plan -> execute -> verify -> reflect -> finalize runtime chain，
`effort="max"` 提高该链路的 retry 预算。`execution: staged`、`allowed-tools`
和 effort presets 可以把选中的 Skills 路由到 TriggerFlow 支撑的 staged/react
执行，并把 action 工作委托给 ActionFlow/ActionRuntime。当内置 profile 不够用时，
使用 `Agently.skills_executor.register_effort_strategy(name, handler)`，让某个
`effort=` 值路由到应用自定义策略；该策略仍应通过 Agent context 组合 model
request、ActionRuntime/MCP、ExecutionEnvironment、TriggerFlow 或 Dynamic Task。
strategy handler 遵循 `SkillsEffortStrategyHandler` protocol（`context`、`task`、
`plan`、`output_format`、`effort`、`effort_config` keyword arguments）；内置
`single_shot`、`runtime_chain`、`staged` 和 `react` 也暴露在同一张 strategy 表里，
可通过 `list_effort_strategies()` 检查。它们的参考实现位于 Agently builtin
Skills Executor 的 `modules/effort_strategies/` 包。

4.1.2.x fulfillment 线会调整链式使用的默认心智：
`agent.use_skills(...).input(...).start()` 是默认 Agent 自动编排的 route
candidate 注册，不再默认表示 prompt-only guidance 注入。未选中 Skills route
时，普通模型响应只应看到安全的能力摘要。只有应用明确需要旧 prompt-only
Skills disclosure 行为时，才使用兼容 setting。
submitted Dynamic Task 和 required Skills 仍是确定性优先；同时存在多个可选
候选时，默认由模型自主选择 route。
框架侧自动编排应描述为 `AgentOrchestrator` plugin protocol 边界：core 持有公开
Agent 入口，active orchestrator plugin 持有路线规划、执行和过程 stream bridge。

伴生仓仍然是 coding-agent 包，不会变成 Agently 应用的运行时依赖。

单个 skill 目录是标准 `SKILL.md` 包。Agently 框架内的 Skills Executor 可以
在明确需要时，把这些目录安装为本地 runtime skill source，用于运行时设计引导
或策略注入。此时它贡献的是 `SKILL.md` 指令、描述性 decision card、资源索引
和安装元数据，不会变成独立的 `skill.run()` runtime，也不会变成 Agently 自创
workflow manifest。在 4.1.x 自动编排中，`agent.use_skills(...)` 应被视为
route candidate。完整 primary `SKILL.md` guidance 属于真正执行该 Skill 的
Skills route；包内 scripts/helpers 仍然只是资产，除非应用把它们绑定为受控
Actions 或 ExecutionEnvironment 管理资源，否则不会执行。

当运行时 Skill 引用 helper scripts 或 shell 类能力时，Agently 必须把这些文件
视为资源。宿主应用可以显式暴露受控 Actions 或 ExecutionEnvironment 管理的工具，
但 Skills Executor 不得直接执行第三方包里的 scripts，也不得在 TriggerFlow 和
Action Runtime 之外自建平行的审批/恢复系统。

## 路由模型

默认 catalog 一共 6 个公开 skills：

- `agently-playbook`
  未定层级的模型应用、助手、内部工具、自动化、评估器、工作流、项目结构
  重构请求的统一入口。
- `agently-request`
  请求侧模型接入、provider settings、Prompt 管理、结构化输出、响应复用、
  streaming 消费、session memory、embeddings、knowledge-base 索引、检索与
  retrieval-backed answers。
- `agently-runtime`
  Action Runtime、内置 action packages、tool 兼容入口、MCP、Execution
  Environment 生命周期、服务暴露、auto-function helpers、`KeyWaiter`，以及
  可选 `agently-devtools` 接入。
- `agently-dynamic-task`
  Dynamic Task DAG 规划、`TaskDAG` 校验、resolver handlers，以及通过
  `Agently.create_dynamic_task(...)` 使用 `TaskDAGExecutor` 执行。
- `agently-triggerflow`
  显式工作流编排、分支、并发、审批、等待和恢复、runtime stream、可重启
  执行、混合同异步函数或模块编排，以及便于图调试的工作流定义。
- `agently-migration`
  从 LangChain、LangGraph、LlamaIndex、CrewAI 或类似系统迁移到 Agently
  原生 request/runtime 或 TriggerFlow 层。

选 skill 时，先按这个顺序想：

- 如果用户请求从业务目标、产品行为、重构诉求，或者一个“还没定 owner
  layer”的问题出发，先走 `agently-playbook`。
- 如果请求保持在一个 request family 内，走 `agently-request`。
- 如果请求需要模型可调用能力、托管执行依赖、服务暴露或 DevTools wiring，
  走 `agently-runtime`。
- 如果请求需要让模型生成或应用提交的 DAG 数据被规划、校验、裁剪并执行，
  走 `agently-dynamic-task`。
- 如果请求需要显式编排，走 `agently-triggerflow`。
- 如果请求是框架迁移，走 `agently-migration`。
- 优先使用 Agently 原生能力，不要先发明自定义 wrapper、parser、retry loop
  或 workflow infrastructure。

执行方式上，默认应采用 async-first 心智：

- 面向服务、streaming、TriggerFlow、tool 并发、长连接消费的场景，优先选择
  异步 API
- 同步 API 更适合作为本地脚本、教学最小示例或兼容桥接层
- 如果目标形态是 HTTP、SSE、WebSocket、后台 worker 或任何需要重叠执行的
  系统，除非有明确限制，否则默认按异步优先设计

## 4.1 之后的默认推荐

当 skills 描述 Agently `4.1+` 的推荐路径时，应收敛到这几条默认用法：

- 结构化输出：固定必填叶子写在 `.output(...)` 的元组 `ensure` 里；运行时
  `ensure_keys` 只用于条件路径或运行时决定的路径。`.output(...)` 默认使用
  `format="auto"`；当前 auto 是结构规则，扁平且全字符串字段解析为
  `flat_markdown`，字符串字段 + 复杂 list/object 字段解析为 `hybrid`，布尔、数字、
  全复杂结构和非 dict 输出解析为 `json`。judge、布尔、数字、密集嵌套数据或下游契约需要 JSON-only 时显式 `format="json"`；只要一个自由文本成品时不要调用 `.output(...)`。`max_retries=3` 可用最多三次额外模型尝试恢复普通解析/key
  缺失，但复杂嵌套数组、占位符回显、布尔/数字字段里填散文、大量 wildcard
  ensure 路径仍可能在重试后失败。`instant` streaming 适合
  `json`/`flat_markdown`/`hybrid`/resolved `auto` 的临时结构化 UI/进度更新；纯文本
  streaming 用 `delta`。
- 模型输出测试：内容级语义校验应使用带 output control 的 Agently model judge。
  把候选输出、显式规则、预期契约和上下文传给 judge；要求每条规则先输出
  evidence 和简短 reason，再输出最终布尔字段；测试断言这些布尔字段。避免把
  关键字、substring、regex 或文本 snapshot 作为模型语义内容正确性的主要信号。
- 场景路由：不要让分词、关键词命中、子串规则或 regex 成为 AI 应用场景路由、
  意图判定或业务分类的 owner。使用合适参数规模的模型配合 Agently output
  schema：简单判定可以用较小模型，条件允许时也可以用本地模型；标签多、规则
  交织、歧义高、风险高或返回结构复杂时，应使用更大参数的模型。
- 框架缺口：应用开发中如果发现框架能力缺失、行为与文档/examples/Skills 指导或
  业务直觉不符、API 未暴露或使用不友好，或架构反思后认为某项责任应由
  Agently 承担但业务代码只能用 workaround、补丁、胶水或私有 wrapper 弥补，
  应生成简洁规范的 issue 说明，并建议到
  `https://github.com/AgentEra/Agently/issues` 提报。人工提交时，只把 issue
  内容和提交方式提供给使用者；issue 必须讲清楚遭遇问题时的具体场景。涉密时
  可以脱敏或不展开业务细节，但仍要说明尝试解决的是哪一类模型应用开发问题、
  workflow 形态和期望由框架承担的责任。人工或自动提报前必须先脱敏本机绝对
  路径、用户名、账号名、token、私有仓库或工作区名、内部项目名、包含私有
  prompt 的原始日志，以及任何客户或项目隐私信息；使用 `<workspace>`、`<repo>`、
  `<task-file>`、`outputs/debug/<turn-id>.jsonl` 这类占位符。自动提交前必须先询问
  用户，并检查本地是否具备 GitHub 提交权限和能力、本地验证问题仍存在、复核
  Agently 文档/examples/Skills 指导和 API 用法，确认不是遗漏信息或不当使用造成
  的问题；最终提交正文还必须做一次隐私扫描。
- Actions：优先 `@agent.action_func` 加 `agent.use_actions(...)`；tool 别名
  保留为兼容入口
- TriggerFlow lifecycle：优先 `close()` / `async_close()` 和 close snapshot；
  不要把 `.end()`、`set_result()`、`get_result()`、`wait_for_result=` 当成
  新代码默认入口
- deprecation 信号：Agently 对每个 deprecated API 在每个 Python 进程内只发
  一次 warning；首次之后不再重复 warning 不代表旧 API 重新成为推荐路径
- 生产降噪：`runtime.show_deprecation_warnings=False` 可以全局关闭 Agently
  deprecation warning，但 skill 仍必须迁移 deprecated API，不得把静默当成推荐
- TriggerFlow state：单 execution 数据优先 `get_state(...)` / `set_state(...)`；
  `flow_data` 视为有意共享且有风险的作用域
- Settings 加载：文件型 provider 配置优先
  `Agently.load_settings("yaml_file", path, auto_load_env=True)`；`Agently.set_settings(...)`
  留给内联覆盖
- 执行风格：服务、流式、工作流默认 async-first
- 响应复用：一次模型结果需要多种消费方式时，优先 `get_response()` 并复用
  同一个 response 对象
- Dynamic Task：把 `Agently.create_dynamic_task(...)` 视为提交式 DAG 的
  公共能力面。TriggerFlow 是它的执行基座，不是 owner API。
- 4.1.2.x Agent 自动编排：默认 `agent.start()` 是普通模型请求、Actions、
  Skills Executor 和 Dynamic Task candidates 之间已验收的候选驱动 route owner。
  submitted Dynamic Task 和 required Skills 保持确定性；模糊可选候选由模型自主
  选择。需要路线诊断、多种结果视图和过程流式输出时，优先 `agent.create_execution()`。
- AgentExecution step contract：兼容路径使用默认 `mode="one_turn"`；开发者自有
  loop 的有界步骤使用 `mode="task_step"`，并显式传 `lineage=` / `limits=`。
  task-step execution 是单步，不是 loop owner；进入下一步前，应由 host 显式把
  observations 写入 Workspace，再构建 ContextPack。通过 `meta["route"]` 和
  `meta["logs"]` 检查 selected route、model response ids、ActionRuntime
  action logs 和 artifact refs；持久化业务证据时，优先使用这些框架记录，而不是让模型
  复述 action stdout。
- runtime stall control：有界 AgentExecution step 优先使用
  `limits={"max_seconds": ..., "max_no_progress_seconds": ...}`，并捕获
  `RuntimeStageStallError`；检查 `meta["diagnostics"]["last_progress"]`、
  `["timeouts"]` 和 `["stalls"]`。Provider 或最终响应卡住时，使用
  `OpenAICompatible.stream_idle_timeout`、
  `OpenAIResponsesCompatible.stream_idle_timeout` 和
  `response.materialization_idle_timeout`，不要在应用外层加长期保留的轮询 wrapper。
  provider 首事件和 stream idle 卡住都应该是 typed runtime stall，而不是靠解析
  `TimeoutError` 文本判断。高频 public delta 可在 `agent.create_execution(...)`
  传 `output_policy={"delta_emit_interval": ..., "delta_max_chars": ...,
  "delta_max_items": ...}`，或配置 `runtime.output`；需要逐条 delta 兼容时保持
  `delta_emit_interval=0`。
- Agently runtime 调试：开发阶段可以挂 EventCenter observation hook，或临时调用
  `.set_settings("debug", True)` / `.set_settings("debug", "detail")` 检查 route
  selection、model request、ActionRuntime 和 Workspace 写入。定位问题后，要从示例和
  生产代码中移除临时 debug hook/settings。
- AgentOrchestrator：把自动编排保持在 plugin protocol 边界内；不要把 route-owned
  Skills 或 Dynamic Task 执行逻辑直接放进 core，也不要把 facade/mixin 耦合描述成
  扩展契约。
- 过程流式：Executor 层应组合 TriggerFlow runtime stream 与 ModelRequest
  `instant` checkpoint，输出 route decision、plan/graph readiness、
  task/stage/action 进度、选定模型字段 delta 和最终 semantic outputs。字段
  delta 应使用 `task_dag.tasks.<task_id>.fields.<field_path>` 这类稳定结构化
  path，而不是直接暴露 provider 原始 token event。

## 标准项目形态

当一个 Agently 项目需要保持可维护性时，初始化或重构都应该围绕明确的能力
边界来做，而不是把所有东西继续塞进一个巨大的 `app.py`。

默认建议拆成这些层：

- `SETTINGS.yaml` 或独立 settings 层，负责 provider 配置、`${ENV.xxx}` 占位、
  workflow/search/browse 参数和其他部署期开关
- `app/` 或应用装配层，负责加载 settings、按需校验必需环境变量、明确异步
  边界，并完成 tools 与主流程的装配
- `prompts/`，负责 YAML / JSON Prompt contract，承载 `input`、`info`、
  `instruct`、`output`
- `services/`，负责请求封装、结果规范化和业务适配
- `domain/` 或 `schemas/`，负责枚举、输入输出协议和共享值对象
- `workflow/`，负责 TriggerFlow 图和 chunk 实现
- `dynamic_task/` 或 service-level modules，用于 Dynamic Task facade、
  提交式 DAG contract、resolver handlers 和 planner constraints
- `tools/`，负责可替换的 search、browse、MCP 或其他外部适配层
- `tests/`，负责 settings smoke check、Prompt/响应检查、API 或 flow 验证
- `outputs/` 和 `logs/`，负责运行产物，而不是把这些内容混进源码目录
- app 或 observability 层里的可选 `agently-devtools` 接入，用于本地
  observation、evaluation、playground 与 logs

更完整的公开规范可以看
[`skills/agently-playbook/references/project-framework.md`](skills/agently-playbook/references/project-framework.md)。

## 安装

先明确目标 agent。推荐把一个 bundle 安装到一个 agent 对应的 skills 目录里，
例如 Codex：

```bash
export AGENT=codex
```

如果目标是 Claude、Cursor 或其他受支持 agent，把 `AGENT` 换成对应名称。

`app`
开发新 Agently 应用的默认 bundle：

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
从 LangChain、LangGraph、LlamaIndex、CrewAI 或类似系统迁移到 Agently 的 bundle。
先安装 `app` bundle，再补充迁移 skill：

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently-migration -y
```

如果只想最小化安装入口 router：

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently-playbook -y
```

查看默认公开 catalog：

```bash
npx skills add . --list
```

默认列表和常规安装路径只暴露当前 6-skill catalog。

## Legacy V1 回退

上一代 12-skill catalog 已归档到 `legacy/v1/`。

- 路径：`legacy/v1/skills/`
- bundle manifest：`legacy/v1/bundles/manifest.json`
- compatibility manifest：`legacy/v1/compatibility/support.json`
- 最后支持的 Agently 主框架版本：`4.1.1`
- 状态：frozen

V1 只用于明确回退和历史项目。它不再跟随 Agently `4.1.2+` compatibility
manifests、新 Action Runtime 指引、Execution Environment 重构或未来 catalog
protocol 演进。不要把 V1 当成新项目推荐路径。

## 可选配套包

Agently 继续将 `agently-devtools` 作为可选开发者工具配套包。

```bash
pip install agently-devtools
agently-devtools init my_project
```

- 安装：`pip install -U agently agently-devtools`
- 兼容线：按当前 Agently release 或 development target 的 compatibility registry
  为准
- 公共入口：`ObservationBridge`、`EvaluationBridge`、`EvaluationRunner`、
  `create_local_observation_app`
- 推荐启动命令：`agently-devtools start`

当 Agently 应用在开发、调试阶段需要本地 runtime observation、评测、日志或
playground 时，应把它当作可选扩展能力接入。Skills 包把它视为可选
observability tooling，而不是源码仓库依赖。

推荐 observation 接入在创建 bridge 时绑定 Agently，再用 `watch(...)` 选择监听范围：

```python
from agently import Agently
from agently_devtools import ObservationBridge

bridge = ObservationBridge(Agently, app_id="your_app_id")
bridge.watch(agent)
```

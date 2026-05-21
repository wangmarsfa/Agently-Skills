# Agently Skills

面向 coding agents 的 Agently 官方可安装 Skills 仓库。

主仓库：<https://github.com/AgentEra/Agently>  
官方文档：<https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## 兼容性

默认公开 catalog 是当前 Agently-Skills generation `v2`，已按 Agently 4.1.2.3
版本线和新的 6-skill 结构对齐。

机器可读兼容声明位于 `compatibility/support.json`。未发布跨仓协作应匹配
当前 Agently development compatibility target。

未发布工作应优先匹配 companion protocols 和 catalog generation：

- authoring protocol：`agently-skills.authoring.v1`
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
- Agently `Skills Executor` —— Agently app / agent 在真实任务里安装并应用外部 skills 的 runtime 能力

当前框架开发线中的运行时 facade 是 `Agently.skills_executor`，底层是 core facade
加 builtin `SkillsExecutor` plugin 实现。框架侧 Skills Executor 尚未发布，
因此不保留 `Agently.skills` 兼容别名。
单个 Agent Skills package 使用 `install_skills(...)`，包含多个 Skills 的仓库
使用 `install_skills_pack(...)`；链式请求可以用
`agent.use_skills(...).input(...).start()` 让模型自动决策是否使用 skills。

伴生仓仍然是 coding-agent 包，不会变成 Agently 应用的运行时依赖。

单个 skill 目录本身仍然是纯文本包。Agently 框架内的 Skills Executor 也
可以在明确需要时，把这些目录当作 **guidance-only runtime skill source**
安装进去，用于运行时设计引导或策略注入。此时它贡献的是 guidance 资产，
不是独立可执行 runtime。

当运行时 Skill 引用 helper scripts 或 shell 类能力时，框架侧执行器应通过
受控 Actions 或 ExecutionEnvironment 管理的工具来解析能力，而不是直接执行
第三方包里的任意 scripts。当前开发线行为包括：在 policy 允许时，把 Bash/shell
类型需求自动绑定到受控 Bash sandbox；如果找不到受控替代能力，则 fail closed，
返回面向用户的自然语言说明和修复建议。

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
  `ensure_keys` 只用于条件路径或运行时决定的路径
- 模型输出测试：内容级语义校验应使用带 output control 的 Agently model judge。
  把候选输出、显式规则、预期契约和上下文传给 judge；要求每条规则先输出
  evidence 和简短 reason，再输出最终布尔字段；测试断言这些布尔字段。避免把
  关键字、substring、regex 或文本 snapshot 作为模型语义内容正确性的主要信号。
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

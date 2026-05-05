# Agently Skills

面向 coding agents 的 Agently 官方可安装 Skills 仓库。

主仓库：<https://github.com/AgentEra/Agently>  
官方文档：<https://agently.tech/docs/en/> | <https://agently.cn/docs/>

## 适配版本

本技能目录已按 Agently 4.1.1 发布线对齐，并跟随当前 TriggerFlow execution lifecycle 指导。

## 什么是 Agently？

Agently 是一个用于构建模型应用和工作流的框架。

它提供的原生能力面包括：

- 异步优先的模型请求、streaming 消费与服务集成
- 模型接入和 provider settings
- Prompt 组合与 prompt config
- 结构化输出与 required keys 约束
- 响应复用、metadata 读取与 streaming 消费
- Action Runtime、tools、MCP、memory、knowledge-base 等扩展能力
- 基于 TriggerFlow 的 lifecycle-aware 工作流编排
- 通过 `agently-devtools` 提供的可选开发者工具能力

## 什么是 Agently-Skills？

Agently-Skills 是面向 coding agents 的 Agently 官方 Skills 套件。

它解决的不只是 API 用法说明，还包括：

- 如何从自然语言产品诉求里识别出适合 Agently 的场景
- 如何选择正确的 skill 或 skill 组合
- 如何按 Agently 原生能力边界来组织项目
- 如何落地最佳实践目录结构、编排方案和性能优化重构
- 如何让 coding agent 避免泛泛地拼接局部能力，而是写出符合 Agently 设计哲学的完整项目

目标不是让 coding agent 只会生成零散代码片段，而是让它能写出真正符合 Agently 设计范式的项目。

例如，像 `基于本地 Ollama 服务做一个旅行计划梳理工具` 这种没有明确技术约束的自然语言请求，不应该只被理解成“一次本地模型调用”。官方 Skills 会帮助 coding agent 进一步判断模型接入方式、Prompt 组织方式、工作流形态和项目结构。

## 为什么要用官方 Skills？

- 它更擅长捕获宽泛、没有明确约束的模型应用开发诉求。
- 它沉淀的是 Agently 原生最佳实践，而不是泛用框架式的局部技巧。
- 它不仅覆盖功能调用，还覆盖目录规划、设计哲学、性能优化和编排重构。
- 它会针对真实场景表达做校验，而不是只靠少量手写示例。

## 路由心智模型

选 skill 时，先按这个顺序想：

- 如果用户请求从业务目标、产品行为、重构诉求，或者一个“还没定 owner layer”的问题出发，先走 `agently-playbook`
- 如果用户请求已经足够具体，直接命中拥有该能力面的 leaf skill
- 优先使用 Agently 原生能力，不要先发明自定义 parser、retry loop、状态机、事件总线或 orchestration 外壳

最重要的路由规则如下：

- 未定层级的产品、助手、自动化、工作流、项目重构请求 -> `agently-playbook`
- 模型接入、env vars、模型配置分离 -> `agently-model-setup`
- Prompt 结构、prompt config、YAML 化 prompt 行为、配置文件桥接 -> `agently-prompt-management`
- 稳定结构化输出、required keys、值级校验、机器可消费结果 -> `agently-output-control`
- 一个响应结果需要被文本、数据、metadata、stream 多次消费 -> `agently-model-response`
- session 连续性与 restore-after-restart -> `agently-session-memory`
- Action Runtime、tools、MCP、FastAPIHelper、`auto_func`、`KeyWaiter`、带 Playwright / PyAutoGUI 的 Browse，或可选 `agently-devtools` observation/evaluation tooling -> `agently-agent-extensions`
- embeddings、索引、检索、KB-to-answer -> `agently-knowledge-base`
- 显式工作流编排、TriggerFlow、execution lifecycle 控制、混合同异步执行、事件驱动 fan-out、流程清晰化重构、图可视化友好的流程定义、可恢复多阶段流程 -> `agently-triggerflow`
- LangChain / LangGraph 迁移 -> `agently-migration-playbook`，再进入对应迁移 leaf

执行方式上，默认应采用 async-first 心智：

- 面向服务、streaming、TriggerFlow、tool 并发、长连接消费的场景，优先选择异步 API
- 同步 API 更适合作为本地脚本、教学最小示例或兼容桥接层
- 如果目标形态是 HTTP、SSE、WebSocket、后台 worker 或任何需要重叠执行的系统，除非有明确限制，否则默认按异步优先设计

## 标准项目形态

当一个 Agently 项目需要保持可维护性时，初始化或重构都应该围绕明确的能力边界来做，而不是把所有东西继续塞进一个巨大的 `app.py`。

默认建议拆成这些层：

- `SETTINGS.yaml` 或独立 settings 层，负责 provider 配置、`${ENV.xxx}` 占位、workflow/search/browse 参数和其他部署期开关
- `app/` 或应用装配层，负责加载 settings、按需校验必需环境变量、明确异步边界，并完成 tools 与主流程的装配
- `prompts/`，负责 YAML / JSON Prompt contract，承载 `input`、`info`、`instruct`、`output`
- `services/`，负责请求封装、结果规范化和业务适配
- `domain/` 或 `schemas/`，负责枚举、输入输出协议和共享值对象
- `workflow/`，负责 TriggerFlow 图和 chunk 实现
- `tools/`，负责可替换的 search、browse、MCP 或其他外部适配层
- `tests/`，负责 settings smoke check、Prompt/响应检查、API 或 flow 验证
- `outputs/` 和 `logs/`，负责运行产物，而不是把这些内容混进源码目录
- app 或 observability 层里的可选 `agently-devtools` 接入，用于本地 observation、evaluation、playground 与 logs

这里有两个需要明确写进规范的源码级细节：

- Configure Prompt 支持对 prompt 的 key 和 value 做递归 placeholder 注入。像 `${topic}`、`${language}`、`${column_title}` 这类变量，应保留在 prompt 文件里，再通过 `load_yaml_prompt(..., mappings={...})` 或 `load_json_prompt(...)` 注入。
- 模型配置可以直接保留 `${ENV.NAME}` 占位；如果配置来自文件，优先用 `Agently.load_settings("yaml_file", path, auto_load_env=True)` 在运行时自动查找并加载本地 `.env` 后完成替换；如果配置来自 Python 内联映射，再使用 `Agently.set_settings(...)`。

还有两个容易踩坑、应当默认明确的规则：

- 稳定共享的 output contract 优先放进 Prompt config，例如 `.request.output`，而不是散落在多个 Python helper 里
- provider 配置应放在插件实际读取的命名空间下，例如 `plugins.ModelRequester.OpenAICompatible.*` 或 `plugins.ModelRequester.AnthropicCompatible.*`
- 可选 DevTools 端点和 bridge wiring 应放在 app 或 observability 层，而不是 Prompt 文件或 workflow helper 里；对外只写公共包 `agently-devtools` 的安装与入口，不写源码仓库接入说明

`Agently-Daily-News-Collector` 用的就是这个模式：settings 留在 `SETTINGS.yaml`，prompt contract 留在 `prompts/`，流程构造留在 `workflow/`，而 app 层负责 `.env` 加载和 Agently wiring。

项目初始化不建议拆成单独的 public skill。它应该属于 `agently-playbook` 的重要执行步骤：先决定 owner layers 和 skeleton，再把具体实现分发给对应 leaf skills。

更完整的公开规范可以看 [`skills/agently-playbook/references/project-framework.md`](skills/agently-playbook/references/project-framework.md)。

## 公开 Catalog

当前公开 catalog 一共 12 个 skills。

### 入口

- `agently-playbook`
  未定层级的模型应用、助手、内部工具、自动化、评估器、工作流、项目结构重构请求的统一入口。

### Request Side

- `agently-model-setup`
  模型连接、dotenv 配置、传输层设置，以及基于 settings 文件的模型配置分离。
- `agently-prompt-management`
  Prompt 组合、prompt config、YAML 化 prompt 行为、mappings 与可复用请求侧 prompt 结构。
- `agently-output-control`
  输出 schema、字段顺序、required keys、值级校验与结构化输出可靠性。
- `agently-model-response`
  `get_response()`、结果复用、metadata、streaming 消费与响应生命周期。
- `agently-session-memory`
  Session 连续性、memo、restore 与请求侧会话状态。

### Request Extensions

- `agently-agent-extensions`
  Action Runtime、tools、MCP、FastAPIHelper、`auto_func`、`KeyWaiter`、带 Playwright / PyAutoGUI 的 Browse，以及可选 `agently-devtools` observation/evaluation tooling。
- `agently-knowledge-base`
  embeddings、Chroma 索引、检索与 retrieval-to-answer。

### Workflow

- `agently-triggerflow`
  TriggerFlow 编排、execution lifecycle、运行时状态、runtime stream、工作流内模型执行、事件驱动 fan-out、流程清晰化重构、混合同异步编排，以及面向调试和可视化的图友好流程定义。

## 可选配套包

Agently 4.1.1 继续将 `agently-devtools` 作为可选开发者工具配套包。

```bash
pip install agently-devtools
agently-devtools init my_project    # 快速初始化 Agently 工程
```

- 安装：`pip install -U agently agently-devtools`
- 兼容线：`agently-devtools 0.1.x` 对应 `agently >=4.1.0,<4.2.0`
- 公共入口：`ObservationBridge`、`EvaluationBridge`、`EvaluationRunner`、`create_local_observation_app`
- 推荐启动命令：`agently-devtools start`

当 Agently 应用在开发、调试阶段需要本地 runtime observation、评测、日志或 playground 时，应把它当作可选扩展能力接入，而不是要求用户接触 DevTools 源码仓库。

### Migration

- `agently-migration-playbook`
  LangChain / LangGraph 迁移总入口。
- `agently-langchain-to-agently`
  LangChain agent 侧迁移。
- `agently-langgraph-to-triggerflow`
  LangGraph orchestration 侧迁移。

## 安装

先明确目标 agent。推荐把一个 bundle 安装到一个 agent 对应的 skills 目录里，例如 Codex：

```bash
export AGENT=codex
```

如果目标是 Claude、Cursor 或其他受支持 agent，把 `AGENT` 换成对应名称。

`app`
开发新 Agently 应用的默认 bundle。它合并了通常必然一起使用的能力：模型请求接入、TriggerFlow、service 与 tool 包装、响应处理、输出控制、session continuity 和知识库指导。

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
从 LangChain、LangGraph、LlamaIndex、CrewAI 或类似系统迁移到 Agently 的 bundle。先安装 `app` bundle，再补充迁移 skills：

```bash
for skill in \
  agently-migration-playbook \
  agently-langchain-to-agently \
  agently-langgraph-to-triggerflow
do
  npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill "$skill" -y
done
```

如果只想最小化安装入口 router：

```bash
npx skills add AgentEra/Agently-Skills --agent "$AGENT" --skill agently-playbook -y
```

高级多 agent 安装：

```bash
npx skills add AgentEra/Agently-Skills --all
```

`--all` 会有意安装到所有检测到的 agents。对于同时配置了多个 coding agents 的仓库，它可能创建 `.agents/`、`.claude/`、`.cursor/`、`.codex/` 等多个隐藏目录，所以不再作为默认推荐。

机器可读的 bundle 定义见 `bundles/manifest.json`。

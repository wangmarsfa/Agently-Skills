---
name: agently-agent-extensions
description: Use when the user wants Action Runtime or tool use, MCP access, HTTP or streaming API exposure, auto-function helpers, wait-for-key behavior, or optional `agently-devtools` observation, evaluation, and playground integration through Agently-native extension surfaces rather than custom wrappers first.
---

# Agently Agent Extensions

Use this skill when the problem is agent-side extension rather than prompt shape, output contract, or workflow control.

## Native-First Rules

- prefer the native Action Runtime, built-in action packages, legacy tool facades, and MCP surfaces before handwritten wrappers
- keep extension choice explicit: Action Runtime, Execution Environment, built-in capability Actions, Agent Components, tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, or `agently-devtools`
- treat `Agently.execution_environment` as an advanced framework/plugin surface, not the default app-development API
- for application developers, prefer built-in Actions and `agent.enable_*` component helpers before exposing core manager/provider concepts
- use `agent.enable_python(...)`, `agent.enable_shell(...)`, `agent.enable_workspace(...)`, `agent.enable_nodejs(...)`, and `agent.enable_sqlite(...)` for common Python, shell, workspace, Node.js, and SQLite access
- treat `enable_*` helper `desc=` values as optional extra guidance by default; use `desc_mode="override"` only when the app intentionally replaces the default capability description
- when changing public helper APIs, use explicit typing for IDE assistance; prefer `Literal` for finite options such as `desc_mode`
- use `@agent.action_func` and `agent.use_actions(...)` as the primary action APIs; `tool_func` and `use_tool` remain compatibility aliases
- use built-in Search/Browse through `from agently.builtins.actions import Search, Browse` and `agent.use_actions(Search(...))` / `agent.use_actions(Browse(...))`; do not invent `enable_search(...)` or `ActionTools`
- keep the permission profile explicit: search-only, local-files-only, network-read, install-capable shell, or trusted broad executor
- use Python sandbox for pure computation or small data shaping; do not use it for imports, filesystem mutation, network access, or dependency installation
- use Bash sandbox or a custom executor when the task needs shell access, package install, or broader command control
- treat MCP, Bash, Python sandbox, Node.js, Docker, SQLite, vector-store, browser, and remote-runner lifecycle as Execution Environment concerns when they need managed handles
- Action executors should declare or consume managed resources instead of hiding lifecycle ownership
- treat `agently-devtools` as an optional companion package installed from PyPI, not as a required source checkout
- keep observation or evaluation bridge wiring in the app layer through `Agently.event_center`
- combine with `agently-model-response` or `agently-triggerflow` only when the scenario needs those layers
- prefer built-in Browse support with Playwright or PyAutoGUI before writing browser or desktop-driving wrappers from scratch

## Anti-Patterns

- do not build a parallel action or tool dispatcher before checking native Action Runtime and MCP support
- do not hide MCP/sandbox/process lifecycle inside a custom ActionExecutor when `Agently.execution_environment` can own the dependency
- do not recommend core manager/provider APIs to ordinary app developers when a built-in Action or Agent Component is the right surface
- do not create a custom waiter or auto-function shim first
- do not ask users to clone or editable-install DevTools when `pip install agently-devtools` is the supported public path
- do not build a custom runtime upload bridge before checking `ObservationBridge`

## Read Next

- `references/overview.md`
- `references/devtools.md`

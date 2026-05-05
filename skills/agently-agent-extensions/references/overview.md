# Overview

This skill owns Agently-native extension surfaces: Action Runtime, tools, MCP, FastAPIHelper, `auto_func`, `KeyWaiter`, and optional `agently-devtools` observation/evaluation tooling.

Use it when:

- the user needs built-in actions or tools such as `Browse`, including `@agent.action_func`, `agent.use_actions(...)`, MCP, or sandbox-backed execution
- the user wants MCP or FastAPIHelper without hand-rolled wrappers
- the user wants local observation, evaluation, playground, or logs support through `agently-devtools`
- the app owner layer is already known and the work is about attaching tooling around that app instead of redesigning the workflow itself

For the public DevTools integration path, read `references/devtools.md`.

## Practical Permission Profiles

Choose the smallest surface that still fits the task. The current codebase supports these patterns directly:

### Search Only

Use `Search` when the task is only to discover web results and you do not need page rendering or local shell access.

```python
import asyncio

from agently.builtins.tools import Search

search = Search(timeout=15, backend="duckduckgo")

async def main():
    results = await search.search("agently action runtime sandbox")
    return results

results = asyncio.run(main())
```

Keep the agent on `agent.use_actions([search.search])` or `agent.use_actions([search.search_news])` only. Do not add `Browse` or any sandbox executor if the job is just retrieval.

### Local Files Only

Use Bash sandbox actions with a tight command allowlist and a root-scoped workspace.

```python
agent.action.register_bash_sandbox_action(
    action_id="repo_reader",
    allowed_cmd_prefixes=["pwd", "ls", "rg", "cat", "head", "tail"],
    allowed_workdir_roots=[repo_root],
    default_policy={
        "workspace_roots": [repo_root],
        "allowed_cmd_prefixes": ["pwd", "ls", "rg", "cat", "head", "tail"],
        "timeout_seconds": 10,
    },
)
```

This is the right profile for “read local files only” or “search the repo tree”. Keep `allow_unsafe=False` and do not include `curl`, `wget`, `pip`, `uv`, or `poetry`.

### Network Read Only

Use `Search` plus `Browse` when the task needs internet access but should not mutate the machine.

```python
import os

from agently.builtins.tools import Browse, Search

search = Search(proxy=os.getenv("BROWSE_PROXY"), timeout=15)
browse = Browse(
    proxy=os.getenv("BROWSE_PROXY"),
    enable_pyautogui=False,
    enable_playwright=True,
    enable_bs4=True,
    fallback_order=("playwright", "bs4"),
)
```

Prefer this for “read web pages”, “summarize docs”, or “verify an online page”. Keep shell sandboxes out of the path unless the task truly needs command execution.
Attach them with `agent.use_actions([search.search, browse.browse])` when you want the agent to call both.

### Dependency Install Or Other Broad Shell Work

If the user wants to install packages, run migrations, or do other shell-heavy work, do not route that through Python sandbox.

Use a bash sandbox action with a deliberate allowlist such as `["python", "pip", "uv", "poetry", "git"]` only for trusted flows, or move to a custom Docker executor when you need a stronger boundary.

```python
agent.action.register_bash_sandbox_action(
    action_id="package_runner",
    allowed_cmd_prefixes=["python", "pip", "uv", "poetry", "git"],
    allowed_workdir_roots=[repo_root],
    default_policy={
        "workspace_roots": [repo_root],
        "allowed_cmd_prefixes": ["python", "pip", "uv", "poetry", "git"],
        "timeout_seconds": 60,
    },
)
```

If you need internet-enabled package installation, prefer a custom Docker executor with `network_mode="enabled"` over relaxing the Python sandbox. The built-in Python sandbox is for code execution, not environment mutation.

### When You Really Want Big Permission

The current codebase does not have a single “full trust” switch for Python sandbox. The safe way to widen scope is to:

- use Bash sandbox or a custom executor, not Python sandbox
- broaden `allowed_cmd_prefixes` only for trusted flows
- keep `allowed_workdir_roots` narrow even when commands are broad
- use `allow_unsafe=True` only in explicitly trusted and reviewable execution paths

For the most permissive boundary, use a dedicated Docker-based executor with controlled network and filesystem settings, and keep that executor isolated from the default app path.

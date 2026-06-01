# Agently Model Setup

Use this skill for provider wiring and transport setup before request logic is discussed.

## Native-First Rules

- default to async-first guidance when the configured model will be used from services, streaming paths, or concurrent workflows
- when settings live in files, prefer `Agently.load_settings("yaml_file", path, auto_load_env=True)`
- use `Agently.set_settings(...)` or `agent.set_settings(...)` for inline mappings or host-owned overrides
- when inline settings benefit from editor hints, use typed helper classes from
  `agently.types.settings` (for example `OpenAICompatibleSettings`) and pass
  the instance directly to `Agently.set_settings(...)`; treat the helper as a
  constructor/validator over the same durable dict settings contract
- prefer settings files with `${ENV.xxx}` placeholders for base URL, model, and auth
- put provider settings under the namespace read by the owning plugin. For `OpenAICompatible`, prefer `plugins.ModelRequester.OpenAICompatible.*`; for `AnthropicCompatible`, prefer `plugins.ModelRequester.AnthropicCompatible.*`
- call the matching settings loader with `auto_load_env=True` when the payload may rely on `.env`
- if the app must fail fast, validate required env names in the integration layer before calling Agently
- after loading, verify the effective provider activation, base URL, model, and auth presence instead of assuming the file shape was correct
- keep provider setup outside business workflow logic and prompt files
- when an Agent must switch among multiple configured models, use
  `agent.activate_model("ollama-qwen2.5")` for subsequent Agent-owned requests
  and `agent.create_request(model_key="deepseek-v4")` for one-off overrides.
  Prefer concrete model aliases such as `ollama-qwen2.5` and `deepseek-v4`,
  then map them through the current layered shape: `model_pool` maps the alias
  to a profile id, `model_profiles` stores provider/model/request settings, and
  `api_key_pools` stores credential pools, request-time selection policy, and
  optional provider-error failover policy. Keep legacy
  `key_pool_strategy` and `key_pool` examples only when explaining existing
  compatibility-line code.
- explain API key pool behavior precisely: keys are selected at request time by
  `api_key_pools.<pool>.selection` (`fixed`, `random`, `round_robin`,
  `least_used`; legacy top-level `strategy` remains accepted). Provider-error
  failover is opt-in through `api_key_pools.<pool>.failover`; without it,
  Agently surfaces provider errors without trying another key. Failover handlers
  can inspect the provider error object and return `"try_next"`,
  `"retry_same"`, `"raise"`, a key id, a key entry dict, or a wrapper such as
  `{"key_id": "b"}` / `{"key_entry": context.keys[1]}`. Do not present
  `405` or `422` as universal credential failures; add them only when the
  specific provider uses those codes for key or quota problems.

## Anti-Patterns

- do not hardcode provider-specific parsing into request code
- do not bake secrets or environment-specific endpoints into committed Python code when settings plus env placeholders fit
- do not leave provider config at a root-level namespace that the active plugin will not read
- do not let sync-only samples dictate the architecture of async-capable services
- do not mix model setup with output parsing or workflow design
- do not use stage names such as `reason` as the main example for user-facing
  model switching; reserve those for internal stage routing docs. Use concrete
  switchable aliases such as `ollama-qwen2.5` and `deepseek-v4`.

## Read Next

- `references/overview.md`

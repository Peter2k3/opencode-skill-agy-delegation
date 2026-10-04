# agy CLI Integration Notes

The skill targets the Antigravity CLI executable named `agy`. Resolve it from `AGY_BIN` or `PATH`; do not depend on a machine-specific installation path.

## Useful Surface

- One-shot prompts: `--print` or `--prompt`.
- Interactive continuation: `--prompt-interactive`, `--continue`, and `--conversation`.
- Execution controls: `--mode plan`, `--mode accept-edits`, `--sandbox`, and repeatable `--add-dir`.
- Structured output: `--output-format text|json|stream-json`.
- Structured validation: `--json-schema` accepts an inline schema or a schema-file path.
- Delegation selection: `--agent` and `--model`; inspect choices with `agy agents` and `agy models`.
- Workspace/session selection: `--project` and `--new-project`.
- Integrations: `agy mcp ...`, `agy plugin ...`, and `agy remote-control ...`.

## Compatibility

Structured print output was introduced before the currently verified `agy` 1.2.x line. Always run `agy --help` and `agy --version` on the target machine before relying on a newer flag.

Agent and model names are installation-specific. Never hardcode the names observed on one machine into a portable workflow.

## Verified Gotchas

- Use `--print='prompt'` or `--print="$PROMPT"`; a separate prompt after `--print` can consume the next flag as prompt text.
- `--print-timeout` uses Go duration syntax, for example `120s` or `2m`.
- `stream-json` reads prompts from stdin and requires `--output-format stream-json`; do not also pass a command-line prompt.
- Stream input expects agy's event envelope; a generic `{type,message}` object is rejected with a missing `event` error.
- A headless JSON run returns an envelope containing `conversation_id`, `status`, `response`, `duration_seconds`, and `usage`.
- Avoid `--dangerously-skip-permissions`; headless permission prompts can block or deny tool calls.

## Recommended Baseline

```bash
AGY_BIN="${AGY_BIN:-agy}"
PROMPT='Analyze only the requested scope. Do not modify files. Return findings, evidence, and risks.'
"$AGY_BIN" --mode plan --output-format json --print-timeout 120s --print="$PROMPT"
```

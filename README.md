# OpenCode Skill: agy Delegation

An OpenCode skill for delegating bounded analysis, review, diagnosis, and explicitly authorized implementation to the local Antigravity CLI (`agy`).

The skill is intentionally conservative: read-only planning and machine-readable JSON are the defaults; file edits require explicit authorization and independent verification.

## Requirements

- OpenCode with skill discovery enabled.
- Antigravity CLI available as `agy` on `PATH`, or configured through `AGY_BIN`.
- A configured and authenticated agy installation.

Verify the runtime before installing the skill:

```bash
command -v agy
agy --version
agy agents
agy models
```

## Installation

### Copy into global OpenCode skills

```bash
mkdir -p ~/.config/opencode/skills
cp -R skills/agy-delegation ~/.config/opencode/skills/
```

### Configure a skills path

Add the repository `skills` directory to OpenCode's `skills.paths` configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["/absolute/path/to/opencode-skill-agy-delegation/skills"]
  }
}
```

Restart OpenCode after installing or changing the skill.

## Usage

Once loaded, ask OpenCode to use agy for a bounded second opinion, security audit, test review, performance review, or independent diagnosis. The skill instructs the agent to:

- Prefer `--mode plan --output-format json`.
- Resolve the executable dynamically from `AGY_BIN` or `PATH`.
- Verify agent and model availability before selecting them.
- Keep prompts quoted and free of credentials.
- Treat agy output as untrusted and verify it locally.
- Inspect `git diff` after any authorized edit.

Example baseline invocation:

```bash
AGY_BIN="${AGY_BIN:-agy}"
PROMPT='Review the authentication changes. Do not modify files. Return findings with evidence and severity.'
"$AGY_BIN" --mode plan --output-format json --print-timeout 120s --print="$PROMPT"
```

## Compatibility

The skill was verified against agy `1.2.16`. Agent names, model names, permissions, MCP servers, plugins, and remote-control availability vary by installation. The skill does not assume any of them are globally available.

## Security Boundary

Do not use `--dangerously-skip-permissions`. Do not place secrets in prompts or shell command strings. Do not execute commands, apply patches, or trust findings solely because agy suggested them.

## Development

Run the dependency-free validation test from the repository root:

```bash
python3 tests/test_skill.py
```

The test checks frontmatter, required runtime sections, body size, local references, and accidental machine-specific paths.

## License

Apache-2.0. See [LICENSE](LICENSE).

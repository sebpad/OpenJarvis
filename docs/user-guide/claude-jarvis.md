# Claude Jarvis

An Iron Man-style assistant that runs OpenJarvis's agent, tools, memory and
voice on Claude models from your Anthropic account.

## 1. Get an API key

OpenJarvis calls the Claude API, which is billed separately from a claude.ai
Pro or Max subscription. Create a key at
[console.anthropic.com](https://console.anthropic.com), add credits, then:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## 2. Install and pick the preset

```bash
uv sync --extra inference-cloud
uv run jarvis init --preset claude-jarvis --force
```

## 3. Talk to it

```bash
uv run jarvis chat --voice     # microphone in, spoken reply out
uv run jarvis chat             # typed chat
uv run jarvis gui              # browser interface
```

## Choosing a model

Edit `~/.openjarvis/config.toml`:

| Model | Price per 1M tokens (in / out) | Use for |
|---|---|---|
| `claude-opus-5-5` (default) | $4 / $20 | Hard reasoning, multi-step tool use |
| `claude-sonnet-5-5` | $2 / $10 | Fast everyday assistant |
| `claude-haiku-5-5` | $0.10 / $0.50 | Cheap, quick replies |

## What it can do

The preset turns on the `orchestrator` agent with web search, file
read/write, code execution, shell, long-term memory and text-to-speech. The
system prompt tells it to ask before deleting data, spending money or
contacting people. Remove `shell_exec` and `file_write` from `[tools]` if you
want a read-only assistant.

To have Jarvis check things for you on a schedule (inbox, calendar, news), see
the [Morning Digest](morning-digest.md) and scheduler docs.

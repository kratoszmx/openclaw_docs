# HANDOFF.md

This file is the continuity layer for the `openclaw_docs` repo.
Use it so future me / other agents do not need long chat history to continue.

## Repo purpose
- Store and sync content from `https://docs.openclaw.ai/`.
- Keep downloaded docs in repo structure for reuse by future agents.
- Read docs with a layered strategy instead of blindly reading everything.

## Current working rules
- Read `skills.txt` before working in this repo.
- Prefer user zsh environment when running commands.
- For docs reading:
  1. scan headings first,
  2. then inspect markdown links,
  3. only read full body when relevant.
- If a local `.md` is empty / truncated / has almost no body, re-download before trusting it.
- Relevant links:
  - if local exists, read local;
  - if local missing, download into this repo first, then read.

## Current helper scripts
- `docs_scan.py`
  - scans markdown headings
  - extracts markdown links
  - flags files as `empty_or_truncated`
- `patch_openclaw_config.py`
  - one-off local machine helper for OpenClaw config changes
  - not part of the generic docs-reading workflow

## Current documentation priorities
For the user's current setup, these pages are usually more relevant:
- `channels/telegram.md`
- `channels/whatsapp.md`
- `channels/imessage.md`
- `channels/pairing.md`
- `channels/troubleshooting.md`
- `install/index.md`
- `install/updating.md`
- `gateway/*`
- `help/*`

## Current known conclusions
- Keep update channel on `stable`.
- Do not switch gateway runtime to Bun for the current Telegram/WhatsApp setup.
- HTTP/2 fetch errors seen during bulk download appear to be transient fetch issues, not proof of a broken local setup.
- For bulk sync, prefer stable download behavior (HTTP/1.1 + retry).

## Context handling policy
- Do not rely on very old chat context when continuing work.
- Externalize important state into repo files (`skills.txt`, `HANDOFF.md`, scripts, tests).
- When the workflow or rules change, update this file.

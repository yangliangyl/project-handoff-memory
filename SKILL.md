---
name: project-handoff-memory
description: Maintain reusable project handoff memory across Codex, Claude Code, WorkBuddy, and other agents. Scans the whole project tree (not only chat context) and keeps every project on ONE standard structure — AGENTS.md (entry protocol) + CLAUDE.md (one-line @AGENTS.md) + README.md + handoff.md in the project root, with progress-log / 口径与数据源 / evidence / open-questions under docs/; legacy-named handoff files get migrated in, not kept in parallel; ships scripts/check_handoff.py to machine-verify structure compliance. Use when a project is not a quick one-off; when the user asks to "沉淀", "交接", "更新项目记忆", "handoff", "给下一个 agent 留文档", or "收尾"; when switching sessions/agents; after meaningful changes to code, SQL, analysis, content pipelines, skills, project structure, key decisions, data caliber, validation status, or next steps.
---

# Project Handoff Memory

Preserve project memory in files inside the project, not only in chat. Keep the handoff useful for the next agent: current state, decisions, constraints, changed artifacts, validation, risks, and next steps.

## Workflow

1. Identify the project root. Prefer the nearest directory containing `AGENTS.md`, `CLAUDE.md`, `README.md`, `SKILL.md`, `.git`, `package.json`, `pyproject.toml`, or the user's named project folder.
2. Scan the whole project tree from the root downward, not only the chat context. Recurse into subfolders and build an abstracted picture of the whole project. Follow [references/tree-scan.md](references/tree-scan.md):
   - Skip noise: `.git`, `node_modules`, `venv`/`.venv`, `__pycache__`, `dist`/`build`, large data dumps and binaries, caches, `.DS_Store`, lockfiles.
   - Summarize the files that future work depends on (code, SQL, scripts, `.md`, configs, data dictionaries). Abstract — do not transcribe.
   - For large files, read structure and head only; do not ingest line by line.
   - Goal: the memory reflects the real project on disk, not just what was mentioned in chat.
3. Read existing handoff signals before editing:
   - `AGENTS.md`, `CLAUDE.md`, `README.md`
   - `handoff.md` (root; also check legacy `docs/handoff.md`), `*交接*.md`, `*沉淀*.md`
   - `docs/progress-log.md`, `docs/decisions.md`, `docs/open-questions.md` when present
4. Classify the project using [references/project-types.md](references/project-types.md) — the type decides which files to recommend (core + optional).
5. If no handoff structure exists, bootstrap the **skeleton core only**, then grow optional files on demand. Follow [references/file-contract.md](references/file-contract.md) for each file's responsibility, update mode, and create/grow triggers:
   - Skeleton (first pass): `AGENTS.md` (sole entry / startup protocol — see Project Entry Files) + `CLAUDE.md` (`@AGENTS.md`) + `handoff.md` (project root) + `docs/progress-log.md`.
   - Content-gated core: `README.md` (once background/goal is settled, else keep it inside handoff) and `docs/open-questions.md` (first real open question).
   - Optional files (e.g. `docs/口径与数据源.md`, `docs/evidence.md`, architecture/interface notes, style/asset index): **never pre-create empty shells** — add per the trigger table, usually by splitting a block out of handoff/README once it grows and stabilizes. `docs/evidence.md` is optional but **recommended for reports/analysis with data or high rigor requirements**: map each key conclusion/number to its source (script/SQL/source file), computation, and verification result, so every claim is traceable and re-checkable. Entries are grouped by **report version / date stamp** (e.g. the run's STAMP): each rerun appends a new version block; old blocks stay, marked historical, never edited in place. Numbers in evidence.md are version-stamped evidence snapshots — the one sanctioned exception to "never hard-code numbers in prose"; an unstamped bare number is still a violation.
6. If a project already has handoff files under legacy or local names, migrate them into the standard structure: keep every content detail, but move it into the standard files and names (see "Migrating Legacy Handoff Files"). Do not maintain parallel non-standard files.
7. Update the right sections using [references/handoff-template.md](references/handoff-template.md), [references/file-contract.md](references/file-contract.md), and the project type rules.
8. Review and update `AGENTS.md` against what this session taught: new pitfalls, new caliber rules, read-order changes, files grown on demand. The entry protocol must track the project's current reality — it is a living file, not write-once (sync to other agents is automatic via the `CLAUDE.md` pointer).
9. Append a short dated entry to `docs/progress-log.md` or the existing progress section. Do not rewrite history unless correcting a factual error.
10. Run `scripts/check_handoff.py <project-root>` (in this skill's `scripts/`) — machine-verifies structure compliance: standard files present, CLAUDE.md is a pure pointer, no legacy files, Status heads, stale references, cross-project pointer integrity, handoff freshness. Fix reds before finishing.
11. Re-read the changed files and verify they answer:
   - What is this project doing now?
   - What changed recently?
   - What must not be broken?
   - What should the next agent do first?

## Update Policy

Write concise operational memory, not a meeting transcript.

- Keep stable facts in `handoff.md`; keep chronology in `progress-log.md`.
- Separate facts, user decisions, agent inferences, and unresolved questions.
- Preserve source-of-truth paths, file names, SQL/table names, data dates, commands, and validation status exactly.
- Mark uncertain items as `待核` or `未验证`; do not upgrade guesses into facts.
- For active work, make the next step concrete enough that another agent can start without asking the user to restate context.
- For one-off or archived work, write only a short index note if needed; do not build a heavy memory system.
- Never include secrets, tokens, cookies, private keys, credentials, or long private/copyrighted source excerpts.

Four rules that keep the memory from drifting (put them into the project's `AGENTS.md`):

- **Conflict arbitration** — when the same fact disagrees across files, trust in order: script live-computation > `口径/reference` > `handoff` > `README/background` > `progress-log/archived`. Numbers that a script recomputes should not be hard-coded in prose.
- **Sinking format** — every sunk item = decision + why + the **rejected alternative** + how to re-verify. Record rejections, not only what was chosen.
- **Domain-knowledge ownership** — cross-project mechanism knowledge (how a metric/star level is computed, rolling windows, settlement lag) lives in its **home project** (its background/口径, one copy), and other projects keep a **pointer**, never a copy. Home = the project that studies it as its core object. Instruction vs knowledge: `AGENTS.md` holds instructions; business background and domain knowledge go to `README`/口径, not into `AGENTS.md`.
- **Status tags** — head each memory file with `Status: current | reference | append-only | archived`, so history is never mistaken for the current state.

## Project Entry Files

Write two entry files that stay in sync from one source. Do not maintain two full copies — they drift.

- `AGENTS.md` — the sole **entry / startup protocol** (not the single store of all truth). Cross-agent standard that Codex, WorkBuddy, and other agents read. Put entry instructions here: read order, caliber rules, pitfalls, conflict arbitration, sinking rules. Keep business background and domain knowledge out — they live in `README`/口径; `AGENTS.md` points to them.
- `CLAUDE.md` — one line only: `@AGENTS.md`. Claude Code resolves this import and auto-loads `AGENTS.md` at the start of every session. A `CLAUDE.md`/`claude.md` carrying real content is a legacy file: migrate its content per "Migrating Legacy Handoff Files" — `CLAUDE.md` is always just the pointer, never a content store.

`AGENTS.md` is a **living file**, not write-once: every handoff pass must review and update it. New pitfalls, new caliber rules, read-order changes, and files grown on demand this session all belong in the entry protocol. Cross-agent sync happens automatically through the `CLAUDE.md` pointer — edit only `AGENTS.md`, never two copies.

Why two files, one source: each new session — interactive, agent switch, or a scheduled/cron run — auto-loads its own entry file (Claude Code reads `CLAUDE.md`, others read `AGENTS.md`). Pointing `CLAUDE.md` at `AGENTS.md` means "every execution reads the same memory" is satisfied by the loaders themselves; you never hand-sync two documents, and you edit memory in exactly one place.

`CLAUDE.md` content:

```md
@AGENTS.md
```

Recommended `AGENTS.md` shape:

```md
# Agent Instructions

This file is the entry / startup protocol, not the store of all truth.
Business background lives in README; data caliber lives in docs/口径与数据源.md.

Before working, read (in order):

1. README.md — what this project is and why (background)
2. handoff.md — current state, next step
3. docs/口径与数据源.md — data sources / caliber, if present
4. docs/progress-log.md — history
5. docs/open-questions.md — if present

Conflict rule: if the same fact disagrees, trust
script computation > 口径/reference > handoff > README > progress-log/archived.

After meaningful changes, sink to memory (decision + why + rejected alternative + how to re-verify):

- current state, changed files/artifacts
- changed decisions or caliber (record rejections too)
- validation status, next steps, risks/watch-outs

Grow files on demand (do not pre-create empty ones): add docs/口径与数据源.md when work
touches data; docs/evidence.md when report conclusions/numbers must be traceable
(recommended for data reports / high-rigor analysis); open-questions when a real open
question appears; split a block out of handoff/README once it grows and stabilizes. Cross-project domain knowledge → keep a
pointer to its home project, never a copy.
```

## Migrating Legacy Handoff Files

All projects use the same standard structure and file names (`AGENTS.md` / `CLAUDE.md` / `README.md` / `handoff.md` in the project root; `docs/progress-log.md` / … under `docs/`). If the project already has a handoff file under another name (e.g. `选店模型_交接说明.md`, `交接文档.md`, a content-bearing `claude.md`), migrate it:

1. Split its content by responsibility into the standard files (current state → `handoff.md` in the project root; dated history → `docs/progress-log.md`; caliber/data facts → `docs/口径与数据源.md`; background → `README.md`; entry rules → `AGENTS.md`).
2. **Before deleting anything**, grep for the legacy file name/path across projects — at minimum the sibling project directories and the global memory (MEMORY) directory — and repoint every external reference to the new location. This step is mandatory, not best-effort: a skipped grep is a silent broken pointer.
3. Then delete the legacy file (leave a one-line pointer stub only if an external dependency exists that cannot be edited).
4. Record the migration — including the cross-project grep result — as a dated entry in `docs/progress-log.md`.

Content is preserved verbatim in meaning; only names and layout are normalized. Chinese business vocabulary inside the files (口径, 待核, 分区 …) stays as is.

For analysis projects, preserve these details:

- data source tables/files
- metric definitions and caliber
- time windows and partitions
- SQL/script entry points
- validation queries/results
- known mismatches and pending checks

## References

- Read [references/tree-scan.md](references/tree-scan.md) when scanning the project tree (step 2).
- Read [references/project-types.md](references/project-types.md) when deciding what to emphasize and which files to recommend.
- Read [references/file-contract.md](references/file-contract.md) for each file's responsibility, update mode, Status, and the create/grow trigger table.
- Read [references/handoff-template.md](references/handoff-template.md) when creating or restructuring handoff files.
- Read [references/update-checklist.md](references/update-checklist.md) before finalizing substantial updates.

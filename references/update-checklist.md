# Update Checklist

Before finalizing a handoff update, check:

- The next agent can identify the project root and main files.
- The project tree was scanned, not just the chat context; anything on disk the chat never mentioned is captured.
- Both entry files exist and are sourced from one place: `AGENTS.md` holds the full instructions, `CLAUDE.md` is `@AGENTS.md` (or an existing `CLAUDE.md` with that line added). No two full copies to hand-sync.
- Files use the standard names and locations (`handoff.md` in the project root; `progress-log.md` / `口径与数据源.md` / `evidence.md` / `open-questions.md` under `docs/`). Legacy-named files (交接文档.md, content-bearing claude.md, docs/handoff.md …) were migrated and removed, not kept in parallel; the migration is logged in progress-log.
- The current state distinguishes completed, pending, and unverified work.
- The handoff names changed files/artifacts explicitly.
- Analysis projects include data caliber, source tables/files, partitions/time windows, and validation status.
- If the deliverable is a data report / high-rigor analysis, `docs/evidence.md` exists (conclusion → evidence map: every key number traceable to source + computation + verification) — or its absence was a deliberate, logged choice. Every evidence entry carries the report version/date stamp; reruns append new blocks instead of editing old ones.
- Any legacy-file migration did the mandatory cross-project grep for the old file name/path (sibling projects + global MEMORY directory) and repointed external references before deleting.
- `scripts/check_handoff.py` (in this skill) was run on the project and reports no red items.
- Product projects include run/test/build commands when relevant.
- Content projects distinguish source facts, user viewpoint, and agent inference.
- Skill projects include trigger conditions, references, guardrails, and install/share locations.
- Progress history is appended, not rewritten, unless correcting an error.
- `AGENTS.md` carries the conflict-arbitration order and stays instructions-only (background/domain knowledge live in README/口径, not here).
- `AGENTS.md` was reviewed and updated this pass: new pitfalls, caliber rules, read-order changes, and on-demand files learned this session are reflected in the entry protocol (it is a living file, not write-once).
- Cross-project domain knowledge is a pointer to its home project, not a copied duplicate.
- Key decisions record why, and rejected alternatives are captured (`[否决]`), not silently dropped.
- Each memory file heads with a `Status:` tag; optional files were grown on demand, not pre-created as empty shells.
- Analysis/product projects have a runnable state check when the pipeline/outputs justify it.
- No secrets, credentials, private keys, or excessive quoted source material are included.

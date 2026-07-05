# File Contract

Each memory file is defined by two axes: **responsibility** (what it holds) and **update mode** (how it changes). Files split into a universal **core** and a per-type **optional** layer. Always use the standard file names and layout below; migrate legacy/local file names into them (see SKILL.md "Migrating Legacy Handoff Files").

## Update modes

- **instruction** — stable action rules; revise in place.
- **pointer** — one-line reference to another file; rarely changes.
- **background·stable** — long-lived knowledge; strip volatile numbers.
- **state·overwrite** — always overwritten to the latest snapshot.
- **reference·stable** — caliber/data facts; change-based edits; **holds volatile numbers/filenames**.
- **history·append-only** — dated entries; never rewrite (except factual fixes).
- **todo·live** — add/remove freely; archive when resolved.

## Universal core

| File | Responsibility | Update mode | Status |
|---|---|---|---|
| `AGENTS.md` | Sole entry / startup protocol: read order, caliber rules (铁律), pitfalls, **conflict arbitration**, sinking rules. **No business background.** | instruction | current |
| `CLAUDE.md` | One line `@AGENTS.md` so Claude Code auto-loads the same memory. | pointer | current |
| `README.md` | Business background: why, evaluation framework, scope, boundaries; **if this project is the home project**, its domain-mechanism knowledge lives here too. | background·stable | reference |
| `handoff.md` (project root) | Current-state snapshot: one-line status / goal / outputs table / data-source table / **recent decisions & rejections** / next steps / watch-outs. One screen. | state·overwrite | current |
| `docs/progress-log.md` | Chronology; dated entries; tag `[决策]`/`[否决]`. | history·append-only | append-only |
| `docs/open-questions.md` | Open questions affecting conclusions; strike through when resolved. | todo·live | current |

## Optional, by project type

| Type | Add | Responsibility |
|---|---|---|
| analysis | `docs/口径与数据源.md` | data sources / caliber / verification hooks / pitfalls / glossary / **domain-knowledge pointer**; holds volatile numbers (reference·stable) |
| analysis | `docs/evidence.md` | **conclusion → evidence map**: each key claim/number in the deliverable, with its source (script/SQL/source file + where in it), computation, verification result and check date. Optional, but recommended whenever the deliverable is a report/analysis involving data or facing high rigor/scrutiny. **Append by report version**: entries grouped under the run's version/date stamp (e.g. STAMP); a rerun appends a new block, old blocks stay marked historical. Version-stamped numbers here are the one sanctioned exception to "no hard-coded numbers in prose" — unstamped bare numbers are still a violation |
| analysis | `scripts/check_project_state.py` | machine verify: sources exist / primary key unique / outputs recomputable |
| product | architecture note, interface/API contract, deploy note | run/build commands may fold into handoff |
| content | topic/outline, style guide, source/asset index | separate source-fact / user-view / agent-inference |
| skill | trigger list + references list, failure modes | do not copy full reference content |
| knowledge | taxonomy / index rules | inclusion/exclusion boundary |

Files count is alive: give the recommended set, let the user add/remove.

## Two relationship rules (responsibility is not only per-file)

1. **Conflict arbitration** — when the same fact disagrees across files, trust in order:
   script live-computation > `口径/reference` > `handoff` > `README/background` > `progress-log/archived`.
2. **Domain-knowledge ownership** — cross-project mechanism knowledge (e.g. how a star level is computed) lives in its **home project** (written into that project's background/口径, one copy only); other projects **keep a pointer**, not a copy. Home = the project that studies it as its core object.

## Create / grow strategy

Bootstrap the skeleton, grow optional files on demand — never pre-create empty shells.

- **Skeleton (create on first pass):** `AGENTS.md` + `CLAUDE.md` + `handoff.md` (root) + `docs/progress-log.md`.
- **Create when there is content:** `README.md` (create once background/goal is settled, else let it live inside handoff first); `docs/open-questions.md` (first real open question).
- **Optional files appear by trigger**, and usually **grow out of** handoff/README (when one block gets long, stabilizes, and is referenced repeatedly, split it into its own file):

| New file | Trigger |
|---|---|
| `README.md` | business background / goal has stabilized |
| `docs/口径与数据源.md` | work starts touching data / fixing取数口径 (analysis: almost always) |
| `docs/evidence.md` | deliverable is a data report / analysis with high rigor or scrutiny — key conclusions and numbers must be traceable to source + verification (optional otherwise); every entry carries the report version/date stamp |
| `docs/open-questions.md` | first open question that affects a conclusion |
| `scripts/check_project_state.py` | pipeline/outputs formed and need repeat verification |
| domain knowledge | never a new file — route to home project / keep pointer |
| architecture · interface contract (product) | code has multiple modules / an external interface |
| style guide · asset index (content) | material starts accumulating / style needs fixing |

Put this trigger table into the project's `AGENTS.md` sinking rules, so any agent grows the memory the same way.

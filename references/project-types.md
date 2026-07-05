# Project Type Rules

Classify by the artifact that future work depends on most. If mixed, choose the dominant risk.

Type decides two things: what to **emphasize**, and which **files** to recommend. Every type shares the
universal core; each adds its own optional files. See [file-contract.md](file-contract.md) for each file's
responsibility, update mode, and the create/grow triggers.

**Universal core (all types):** `AGENTS.md` + `CLAUDE.md` + `handoff.md` (root) + `docs/progress-log.md`
create on the first pass; `README.md` and `docs/open-questions.md` are core-but-content-gated (create when
there is real content). Never pre-create empty optional shells — grow them on demand per the trigger table.

## analysis

Use for SQL, data analysis, business reporting, model scoring, metrics, dashboards, and research backed by data.

Emphasize:

- business question and current analytical goal
- source tables/files and important paths
- metric definitions, denominator/numerator rules, time windows, partitions
- SQL/script entry points
- validation status and known data mismatches
- pending business/user decisions
- next verification query or report step

Avoid:

- vague insight summaries without source paths
- hiding uncertainty in confident language

Files (beyond core): `docs/口径与数据源.md` (on-demand, near-certain — created once work touches data/caliber); `docs/evidence.md` (optional — but recommended when the deliverable is a report/analysis involving data or high rigor: conclusion→evidence map so every key number is traceable); domain-knowledge pointer (never a copy); optional `scripts/check_project_state.py` once the pipeline/outputs stabilize.

## product

Use for apps, scripts, data pipelines, websites, automations, and software projects.

Emphasize:

- what the product does and current stage
- run/test/build commands
- architecture and key files
- recent changed files
- tests run and known gaps
- bugs, risks, and next implementation step

Avoid:

- replacing technical run instructions with high-level prose

Files (beyond core): architecture note, interface/API contract, deploy note — each on-demand when code gains multiple modules or an external interface. Run/build commands may stay folded into handoff until they grow.

## content

Use for articles, videos, course material, creator analysis, scripts, cards, or publishing workflows.

Emphasize:

- target audience and content job-to-be-done
- source material paths/URLs and evidence boundary
- current draft/asset status
- user-owned viewpoint versus agent inference
- claims to verify
- next production step

Avoid:

- turning provisional angles into final user opinions

Files (beyond core): topic/outline, style guide, source/asset index — on-demand once material accumulates or style needs fixing.

## skill

Use for reusable agent skills, prompts, workflows, templates, and operating procedures.

Emphasize:

- trigger situations
- workflow steps
- required references/scripts/assets
- guardrails and failure modes
- validation status from realistic usage
- where the skill is installed or shared

Avoid:

- duplicating full reference content in the handoff

Files (beyond core): trigger list + references/scripts list, failure modes — on-demand as the skill gains references or realistic-usage lessons.

## knowledge

Use for research folders, knowledge bases, reading notes, flomo/Obsidian organization, and personal archives.

Emphasize:

- organizing principle
- source boundary
- inclusion/exclusion rules
- taxonomy or index status
- unresolved classification decisions

Avoid:

- over-structuring one-time archives

Files (beyond core): taxonomy/index rules, inclusion/exclusion boundary — on-demand; for one-time archives a short index note is enough.

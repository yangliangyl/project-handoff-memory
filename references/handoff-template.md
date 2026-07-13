# Handoff Template

Use this template when creating a new `handoff.md` — it lives in the **project root** (not under `docs/`). Keep sections that are useful; omit empty sections.

```md
# Project Handoff

> Status: current
> Last updated: YYYY-MM-DD
> Project type: analysis | product | content | skill | knowledge

## One-Line Status

What is true right now in one or two sentences.

## Current Goal

What the project is trying to accomplish now.

## Current State

What is done, what is partially done, and what is not started.

## Key Files

| Path | Role | Status |
|---|---|---|
| `path/to/file` | why it matters | current status |

## Key Decisions / Caliber

- Decision or definition, with date/source if important.
- Mark uncertain items as `待核`.

## Decisions & Rejections

- `[决策]` decision — why in one line.
- `[否决]` rejected alternative — why rejected (so it is not reconsidered).

## Recent Changes

- YYYY-MM-DD: concise change summary.

## Validation Status

- What was checked.
- What passed.
- What remains unverified.

## Next Steps

<!-- 只写用户明确确认过的事项（用户提出的，或用户认可的 agent 建议）。
     Agent 自行推断的候选动作不写这里 → 记入 docs/open-questions.md 标「建议·未确认」。 -->

1. Concrete next action.
2. Concrete next action.

## Watch Outs

- Risk, pitfall, or thing not to change casually.
```

File names and section structure follow this standard template for every project. Chinese business vocabulary inside the content (`口径`, `待核`, `分区`, `调度`, `主交付`, `验证`) stays as is — normalize the structure, not the language.

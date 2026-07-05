# Project Tree Scan

The handoff must reflect the real project on disk, not only what came up in chat. Before writing memory, scan the project tree from the root downward and build an abstracted picture of the whole thing.

## Principle

Abstract, do not transcribe. The output of the scan is your understanding of what each part of the project is for — feed that into the handoff. Never paste large file bodies into the memory files.

## What to skip

Do not descend into or read:

- `.git`, `.svn`
- `node_modules`, `venv`, `.venv`, `__pycache__`, `.pytest_cache`, `.mypy_cache`
- `dist`, `build`, `.next`, `target`, `out`
- large data dumps and binaries: `*.csv`/`*.parquet`/`*.xlsx` over a few MB, `*.zip`, `*.png`/`*.jpg`, `*.mp4`/`*.mov`, `*.pdf`, model weights
- lockfiles (`package-lock.json`, `poetry.lock`, `uv.lock`) — note they exist, do not read
- `.DS_Store`, editor/OS junk, cache directories

When you skip a heavy directory, still record that it exists and what it is (e.g. "`data/` — raw exports, not read").

## What to summarize

Read enough of these to know their role, then abstract:

- code, SQL, scripts (`.py`, `.sql`, `.sh`, `.js`/`.ts`, notebooks)
- `.md` docs, READMEs, existing handoff/交接/沉淀 files
- configs, `pyproject.toml`/`package.json`, `.env.example` (never read real `.env`)
- data dictionaries, schema files, column-mapping sheets

## Depth and cost control

- Recurse into all non-skipped subfolders, but read lightly.
- For a large file, read its structure and head only (top of file, function/section names, table/column names) — do not ingest line by line.
- Prefer listing + targeted reads over reading every file in full.
- For a big project, a directory listing plus head-reads of the key files beats a full-text sweep. Coverage of the shape matters more than every line.

## Turn the scan into memory

From the scan, the handoff should be able to answer:

- What are the main moving parts and where do they live?
- Which files are entry points (SQL/script/run commands)?
- What changed recently versus what is stable?
- What on disk must not be broken?

If the scan surfaces something the chat never mentioned (an extra script, a second data source, an abandoned folder), record it — that gap is exactly what handoff memory is for.

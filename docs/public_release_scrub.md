# Public-release scrub report

Scope: every file selected for the public repository, including code, source text, JSON, CSV, documentation and the four actual local-demo screenshots. The reproducible scanner checks machine-specific absolute paths, secret-like API tokens, private-key blocks and prohibited generated artifacts. Source lineage, schema, links and numerical checks are recorded separately in the final validation report.

## Excluded

- API keys, environment values, credential files and local usernames/absolute paths.
- Original hidden synthetic ground truth and private case-specific evaluator criteria; their contents are not part of this release.
- Private notes, conversation recovery summaries and historical evaluator score reports.
- Nested frozen input copies, old development versions, source ZIP archives and duplicate Excel history.
- Local benchmark requests/responses, logs, audit events, replay outputs, prepared-context duplicates, caches and virtual environments.
- Development helper scripts outside the clean repository and browser installation files.

## Intentionally included

Synthetic source documents and historical observations, source-grounded diagnostic/design outputs, generic rubrics, deterministic tests, authored source-level controls and empty semantic-review preparation forms. Historical resolutions are descriptive data and are excluded from model case context. Public controls are not hidden benchmark labels; they make the development-set limitation explicit.

`.gitignore` covers secrets, `.env` variants, Streamlit secrets, local run output, caches, environments, logs, temporary files, ZIPs and OS junk. Four screenshots were visually checked; they show synthetic cases and a demonstration reviewer label, no credential or private machine path.

## Result

See the final validation report for the executed scan result and exact check counts. No scanner guarantees detection of every possible secret format. The manifest defines the reviewed upload scope; adding files later requires another scrub. No GitHub upload has occurred.

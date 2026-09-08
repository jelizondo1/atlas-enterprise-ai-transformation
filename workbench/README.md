# Read-only case and measurement logic

The workbench assembles twelve source-grounded dossiers. Source hashes and case versions bind review and measurement records to evidence. Historical outcomes are excluded from case facts; authored design questions and holds are separate from model generation.

```sh
python workbench/workbench.py replay --output runs/replay
```

`record-review` validates a cited assessment and writes a local hash-linked audit record. It does not authenticate identity or approve a payment. Use `python workbench/workbench.py --help` and `python workbench/measurements.py --help` for local commands. Measurement rejects duplicate cases, stale versions, overlapping effort intervals and unqualified observations. Synthetic fixtures never become measured pilot inputs.

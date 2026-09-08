# Deterministic process diagnostics

The 250 synthetic rows support descriptive metrics, not causal root-cause labels. Recompute from the repository root after creating the local `runs` directory:

```sh
python diagnostics/atlas_diagnostics.py source_pack/meridian_disputes_250.csv --json runs/diagnostics.json --markdown runs/diagnostics.md
```

Annual volume and staffing assumptions live in the impact-sizing folder. Exact annual handling is 23.984 minutes × 180,000 / 60 = 71,952 hours. Do not treat recorded historical resolutions as correct decisions.

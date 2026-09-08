# Source-grounded diagnosis

The diagnosis separates DIRECT evidence, DERIVED calculations and INFERRED interpretation. It is the completed source diagnosis, not a newly run public model benchmark.

To assemble its allowed evidence bundle from the repository root:

```sh
python reasoning/build_diagnosis_context.py source_pack diagnostics/meridian_quantitative_diagnostics.json --output runs/diagnosis_context.json
```

Create the local `runs` directory first. The bundle contains five client documents, twelve packets and separate quantitative sections. It excludes evaluator material. Use the supplied schema and prompt for any later diagnosis experiment; record model/version and evaluate separately. The live case-draft integration is a distinct capability.

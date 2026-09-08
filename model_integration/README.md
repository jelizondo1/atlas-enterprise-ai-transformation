# Bounded live validation

Status: integration ready, live benchmark pending. No API key was available; no model was selected or called. The Responses API adapter, strict structured output, source allowlist, citation gate, failure paths, semantic review and benchmark accounting are covered by local tests.

Privately configure `OPENAI_API_KEY` in the environment and select an available structured-output model. From the repository root:

```sh
python model_integration/live_batch.py --model YOUR_AVAILABLE_MODEL_ID
```

This is the only initial batch: 0018, 0139, 0184; maximum 3 cases, 4,096 output tokens each, 60-second timeout per request, no automatic retries, no tools, `store=false`. Input has a 100,000-character cap; oversized input is rejected rather than truncated. Refusal/incomplete/HTTP errors are recorded. An uncertain timeout must be reconciled before manually trying again. It stops early for credential/configuration/transport failures.

Ignored `runs/live/<batch>/<case>/` contains request, response when available, run metadata, structural evaluation and a semantic template for each admitted draft. Requested and returned model IDs, response/request IDs, prompt/schema/context/request hashes, latency and usage are preserved. A missing provider field stays unavailable. None of this is committed by default.

The independent reviewer completes `semantic_review.template.json` against actual source lines, after freezing their case criteria. Evaluate the completed file and recompute the batch summary:

```sh
python model_integration/evaluate_run.py runs/live/BATCH/CASE --review runs/live/BATCH/CASE/semantic_review.template.json
python model_integration/summarize_benchmark.py runs/live/BATCH --output runs/live/BATCH/benchmark_summary.json
```

Replace BATCH and CASE with the printed run identifiers. Do not edit run metadata or relabel a test transport as live. Local files are not tamper-proof; an enterprise benchmark requires controlled storage and authenticated reviewers. Public release preparation forms remain blank because there is no actual draft to bind to a review hash.

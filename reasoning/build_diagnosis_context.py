#!/usr/bin/env python3
import json
from pathlib import Path

CLIENT_DOCS = [
    "01_AP_Dispute_Resolution_SOP.md",
    "02_Vendor_Commercial_Terms_Policy.md",
    "03_NorthStar_Agreements.md",
    "04_Apex_Agreement.md",
    "05_Solara_Agreements_and_Email.md",
]

def build_context(source_pack_dir, quantitative_json_path):
    source_pack = Path(source_pack_dir)
    quant_path = Path(quantitative_json_path)
    sections = []

    for filename in CLIENT_DOCS:
        path = source_pack / filename
        if not path.exists():
            raise FileNotFoundError(path)
        sections.append({
            "source_id": f"DOC:{filename}",
            "source_type": "document",
            "content": path.read_text(encoding="utf-8"),
        })

    evidence_dir = source_pack / "06_Unstructured_Case_Evidence"
    if evidence_dir.exists():
        for path in sorted(evidence_dir.glob("*.md")):
            if "_evaluation_only_DO_NOT_INGEST" in str(path):
                continue
            sections.append({
                "source_id": f"CASE:{path.stem}",
                "source_type": "case_evidence",
                "content": path.read_text(encoding="utf-8"),
            })

    with open(quant_path, encoding="utf-8") as f:
        quant = json.load(f)

    # Expose deterministic sections separately so evidence citations are granular.
    for key, value in quant.items():
        sections.append({
            "source_id": f"QUANT:{key}",
            "source_type": "deterministic_quantitative_evidence",
            "content": value,
        })

    return {
        "case_name": "Meridian Retail Group — Supplier Invoice Dispute Transformation",
        "instructions": [
            "Diagnose current state only.",
            "Do not recommend AI, automation, software, organization redesign, or target state.",
            "Use DIRECT, DERIVED, and INFERRED evidence labels.",
            "Do not use evaluation-only files.",
            "Do not assume historical resolutions were correct.",
        ],
        "sources": sections,
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("source_pack_dir")
    parser.add_argument("quantitative_json_path")
    parser.add_argument("--output", default="atlas_diagnosis_context.json")
    args = parser.parse_args()
    bundle = build_context(args.source_pack_dir, args.quantitative_json_path)
    Path(args.output).write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    print(args.output)

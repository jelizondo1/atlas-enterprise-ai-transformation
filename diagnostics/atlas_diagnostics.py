#!/usr/bin/env python3
"""
ATLAS deterministic quantitative diagnostic analyzer.

Purpose
-------
Analyze Meridian Retail Group's client-facing historical AP dispute dataset
without using LLM reasoning or evaluation-only ground truth.

Inputs
------
A CSV with historical dispute cases.

Outputs
-------
1. JSON diagnostic summary for downstream LLM use.
2. Markdown quantitative report for human review.

Important design principle
--------------------------
This layer calculates facts. It does not recommend AI, automation, or target-state
solutions, and it does not use hidden evaluator answers.
"""

import csv
import json
import math
import statistics
from collections import Counter, defaultdict


def _to_float(value):
    if value in ("", None):
        return None
    return float(value)


def _to_int(value):
    if value in ("", None):
        return None
    return int(float(value))


def _pct(num, den):
    return (num / den) if den else None


def _mean(values):
    vals = [v for v in values if v is not None]
    return statistics.mean(vals) if vals else None


def _median(values):
    vals = [v for v in values if v is not None]
    return statistics.median(vals) if vals else None


def _pearson(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    xvals = [p[0] for p in pairs]
    yvals = [p[1] for p in pairs]
    xbar = statistics.mean(xvals)
    ybar = statistics.mean(yvals)
    num = sum((x-xbar)*(y-ybar) for x,y in pairs)
    denx = math.sqrt(sum((x-xbar)**2 for x in xvals))
    deny = math.sqrt(sum((y-ybar)**2 for y in yvals))
    if denx == 0 or deny == 0:
        return None
    return num / (denx * deny)


def load_cases(csv_path):
    cases = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["disputed_amount_usd"] = _to_float(row.get("disputed_amount_usd"))
            row["handling_minutes"] = _to_float(row.get("handling_minutes"))
            row["resolution_days"] = _to_float(row.get("resolution_days"))
            row["sla_target_days"] = _to_float(row.get("sla_target_days"))
            row["systems_accessed_count"] = _to_int(row.get("systems_accessed_count"))
            row["documents_reviewed_count"] = _to_int(row.get("documents_reviewed_count"))
            cases.append(row)
    return cases


def group_metrics(cases, key):
    grouped = defaultdict(list)
    for c in cases:
        grouped[c.get(key, "")].append(c)

    result = []
    for group, rows in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        n = len(rows)
        result.append({
            key: group,
            "cases": n,
            "case_share": n / len(cases),
            "avg_disputed_amount_usd": _mean([r["disputed_amount_usd"] for r in rows]),
            "median_disputed_amount_usd": _median([r["disputed_amount_usd"] for r in rows]),
            "avg_handling_minutes": _mean([r["handling_minutes"] for r in rows]),
            "avg_resolution_days": _mean([r["resolution_days"] for r in rows]),
            "sla_attainment": _pct(sum(r.get("sla_met") == "Yes" for r in rows), n),
            "reopen_rate": _pct(sum(r.get("reopened") == "Yes" for r in rows), n),
            "missing_evidence_rate": _pct(sum(r.get("missing_evidence") == "Yes" for r in rows), n),
            "avg_systems_accessed": _mean([r["systems_accessed_count"] for r in rows]),
            "avg_documents_reviewed": _mean([r["documents_reviewed_count"] for r in rows]),
        })
    return result


def binary_segment(cases, field, yes_value="Yes"):
    yes = [c for c in cases if c.get(field) == yes_value]
    no = [c for c in cases if c.get(field) != yes_value]

    def summarize(rows):
        n = len(rows)
        return {
            "cases": n,
            "avg_handling_minutes": _mean([r["handling_minutes"] for r in rows]),
            "avg_resolution_days": _mean([r["resolution_days"] for r in rows]),
            "sla_attainment": _pct(sum(r.get("sla_met") == "Yes" for r in rows), n),
            "reopen_rate": _pct(sum(r.get("reopened") == "Yes" for r in rows), n),
            "avg_systems_accessed": _mean([r["systems_accessed_count"] for r in rows]),
        }

    return {"yes": summarize(yes), "no": summarize(no)}


def complexity_bands(cases):
    bands = [
        ("2 systems", lambda x: x == 2),
        ("3 systems", lambda x: x == 3),
        ("4 systems", lambda x: x == 4),
        ("5+ systems", lambda x: x is not None and x >= 5),
    ]
    out = []
    for label, fn in bands:
        rows = [c for c in cases if fn(c["systems_accessed_count"])]
        if not rows:
            continue
        n = len(rows)
        out.append({
            "complexity_band": label,
            "cases": n,
            "avg_handling_minutes": _mean([r["handling_minutes"] for r in rows]),
            "avg_resolution_days": _mean([r["resolution_days"] for r in rows]),
            "sla_attainment": _pct(sum(r.get("sla_met") == "Yes" for r in rows), n),
            "reopen_rate": _pct(sum(r.get("reopened") == "Yes" for r in rows), n),
        })
    return out


def concentration(cases):
    by_supplier = Counter(c["supplier_name"] for c in cases)
    total = len(cases)
    top3 = by_supplier.most_common(3)
    return {
        "top_3_suppliers": [{"supplier": k, "cases": v, "share": v/total} for k,v in top3],
        "top_3_case_share": sum(v for _,v in top3)/total if total else None,
    }


def analyze(cases):
    n = len(cases)
    amounts = [c["disputed_amount_usd"] for c in cases]
    handling = [c["handling_minutes"] for c in cases]
    resolution = [c["resolution_days"] for c in cases]
    systems = [c["systems_accessed_count"] for c in cases]
    documents = [c["documents_reviewed_count"] for c in cases]

    reason_counter = Counter(c["system_reason_code"] for c in cases)

    overall = {
        "cases": n,
        "total_disputed_amount_usd": sum(v for v in amounts if v is not None),
        "avg_disputed_amount_usd": _mean(amounts),
        "median_disputed_amount_usd": _median(amounts),
        "avg_handling_minutes": _mean(handling),
        "median_handling_minutes": _median(handling),
        "avg_resolution_days": _mean(resolution),
        "median_resolution_days": _median(resolution),
        "sla_attainment": _pct(sum(c.get("sla_met") == "Yes" for c in cases), n),
        "reopen_rate": _pct(sum(c.get("reopened") == "Yes" for c in cases), n),
        "missing_evidence_rate": _pct(sum(c.get("missing_evidence") == "Yes" for c in cases), n),
        "avg_systems_accessed": _mean(systems),
        "avg_documents_reviewed": _mean(documents),
        "other_reason_code_share": _pct(reason_counter.get("OTHER", 0), n),
        "escalation_share": _pct(sum(c.get("resolution") == "ESCALATE" for c in cases), n),
    }

    correlations = {
        "systems_vs_handling_minutes": _pearson(systems, handling),
        "systems_vs_resolution_days": _pearson(systems, resolution),
        "documents_vs_handling_minutes": _pearson(documents, handling),
        "documents_vs_resolution_days": _pearson(documents, resolution),
        "handling_minutes_vs_resolution_days": _pearson(handling, resolution),
    }

    return {
        "overall": overall,
        "by_system_reason_code": group_metrics(cases, "system_reason_code"),
        "by_supplier": group_metrics(cases, "supplier_name"),
        "by_analyst": group_metrics(cases, "analyst_id"),
        "by_resolution": group_metrics(cases, "resolution"),
        "missing_evidence_impact": binary_segment(cases, "missing_evidence"),
        "reopened_case_profile": binary_segment(cases, "reopened"),
        "priority_supplier_profile": binary_segment(cases, "priority_supplier"),
        "system_complexity_bands": complexity_bands(cases),
        "correlations": correlations,
        "concentration": concentration(cases),
    }


def _fmt_pct(v):
    return "n/a" if v is None else f"{v:.1%}"


def _fmt_num(v, decimals=1):
    return "n/a" if v is None else f"{v:,.{decimals}f}"


def _fmt_usd(v):
    return "n/a" if v is None else f"${v:,.0f}"


def markdown_report(result):
    o = result["overall"]
    lines = [
        "# ATLAS — Meridian Quantitative Diagnostic",
        "",
        "## 1. Deterministic baseline",
        "",
        f"- Historical cases analyzed: **{o['cases']:,}**",
        f"- Total disputed value represented: **{_fmt_usd(o['total_disputed_amount_usd'])}**",
        f"- Average active handling time: **{_fmt_num(o['avg_handling_minutes'])} min**",
        f"- Average final resolution time: **{_fmt_num(o['avg_resolution_days'])} business days**",
        f"- SLA attainment: **{_fmt_pct(o['sla_attainment'])}**",
        f"- Reopen rate: **{_fmt_pct(o['reopen_rate'])}**",
        f"- Missing-evidence rate: **{_fmt_pct(o['missing_evidence_rate'])}**",
        f"- Average systems accessed per case: **{_fmt_num(o['avg_systems_accessed'])}**",
        f"- Average evidence types reviewed per case: **{_fmt_num(o['avg_documents_reviewed'])}**",
        f"- Cases coded OTHER at intake: **{_fmt_pct(o['other_reason_code_share'])}**",
        f"- Historical cases ending in ESCALATE: **{_fmt_pct(o['escalation_share'])}**",
        "",
        "## 2. Performance by system reason code",
        "",
        "| Reason code | Cases | Share | Avg handling | Avg resolution | SLA | Reopen | Missing evidence |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for x in result["by_system_reason_code"]:
        lines.append(
            f"| {x['system_reason_code']} | {x['cases']} | {_fmt_pct(x['case_share'])} | "
            f"{_fmt_num(x['avg_handling_minutes'])} min | {_fmt_num(x['avg_resolution_days'])} d | "
            f"{_fmt_pct(x['sla_attainment'])} | {_fmt_pct(x['reopen_rate'])} | {_fmt_pct(x['missing_evidence_rate'])} |"
        )

    lines += [
        "",
        "## 3. Supplier profile",
        "",
        "| Supplier | Cases | Avg handling | Avg resolution | SLA | Reopen | Avg systems |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for x in result["by_supplier"]:
        lines.append(
            f"| {x['supplier_name']} | {x['cases']} | {_fmt_num(x['avg_handling_minutes'])} min | "
            f"{_fmt_num(x['avg_resolution_days'])} d | {_fmt_pct(x['sla_attainment'])} | "
            f"{_fmt_pct(x['reopen_rate'])} | {_fmt_num(x['avg_systems_accessed'])} |"
        )

    me = result["missing_evidence_impact"]
    rp = result["reopened_case_profile"]
    lines += [
        "",
        "## 4. Observable complexity effects",
        "",
        "### Missing evidence",
        f"- Cases with missing evidence: **{me['yes']['cases']}**",
        f"- Avg resolution with missing evidence: **{_fmt_num(me['yes']['avg_resolution_days'])} days** vs "
        f"**{_fmt_num(me['no']['avg_resolution_days'])} days** without it.",
        f"- SLA attainment with missing evidence: **{_fmt_pct(me['yes']['sla_attainment'])}** vs "
        f"**{_fmt_pct(me['no']['sla_attainment'])}** without it.",
        "",
        "### Reopened cases",
        f"- Reopened cases: **{rp['yes']['cases']}**",
        f"- Avg handling when reopened: **{_fmt_num(rp['yes']['avg_handling_minutes'])} min** vs "
        f"**{_fmt_num(rp['no']['avg_handling_minutes'])} min** otherwise.",
        f"- Avg resolution when reopened: **{_fmt_num(rp['yes']['avg_resolution_days'])} days** vs "
        f"**{_fmt_num(rp['no']['avg_resolution_days'])} days** otherwise.",
        "",
        "### Systems touched",
        "",
        "| Systems accessed | Cases | Avg handling | Avg resolution | SLA | Reopen |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for x in result["system_complexity_bands"]:
        lines.append(
            f"| {x['complexity_band']} | {x['cases']} | {_fmt_num(x['avg_handling_minutes'])} min | "
            f"{_fmt_num(x['avg_resolution_days'])} d | {_fmt_pct(x['sla_attainment'])} | {_fmt_pct(x['reopen_rate'])} |"
        )

    c = result["correlations"]
    lines += [
        "",
        "## 5. Correlations (descriptive, not causal)",
        "",
        f"- Systems accessed vs handling time: **{_fmt_num(c['systems_vs_handling_minutes'], 2)}**",
        f"- Systems accessed vs resolution time: **{_fmt_num(c['systems_vs_resolution_days'], 2)}**",
        f"- Evidence types reviewed vs handling time: **{_fmt_num(c['documents_vs_handling_minutes'], 2)}**",
        f"- Evidence types reviewed vs resolution time: **{_fmt_num(c['documents_vs_resolution_days'], 2)}**",
        f"- Handling time vs resolution time: **{_fmt_num(c['handling_minutes_vs_resolution_days'], 2)}**",
        "",
        "These are descriptive relationships only. Atlas should not infer causality from them without additional evidence.",
        "",
        "## 6. Data-boundary notes",
        "",
        "- This analysis uses only client-facing historical case fields.",
        "- It does **not** use the `_evaluation_only_DO_NOT_INGEST` ground-truth folder.",
        "- It does **not** determine whether historical resolutions were correct.",
        "- It does **not** recommend AI, automation, or target-state solutions.",
        "- System reason codes are analyzed as recorded operational data; this layer cannot independently determine classification accuracy.",
        "",
        "This report is intended to be fed into Atlas' reasoning layer as deterministic quantitative evidence.",
    ]
    return "\n".join(lines)


def run(csv_path, json_output, markdown_output):
    cases = load_cases(csv_path)
    result = analyze(cases)

    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    with open(markdown_output, "w", encoding="utf-8") as f:
        f.write(markdown_report(result))

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--json", default="meridian_quantitative_diagnostics.json")
    parser.add_argument("--markdown", default="meridian_quantitative_diagnostics.md")
    args = parser.parse_args()
    run(args.csv_path, args.json, args.markdown)

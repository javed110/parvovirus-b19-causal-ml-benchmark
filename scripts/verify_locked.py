"""Independent aggregate checks; no protected workbook or modelling packages required."""
from pathlib import Path
import csv, hashlib, json, math, statistics
from collections import defaultdict

root=Path(__file__).resolve().parents[1]
def records(name):
    with (root/name).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def close(actual,expected,label,tol=1e-8):
    if not math.isclose(float(actual),float(expected),abs_tol=tol,rel_tol=tol):
        raise AssertionError(f"{label}: {actual} != {expected}")

# The legacy manifest includes pre-edit document hashes. Verify numerical/figure
# artifacts only; do not imply that unchanged manuscript metadata is current.
checked=0
for line in (root/"MANIFEST_SHA256.txt").read_text(encoding="utf-8-sig").splitlines():
    digest,name=line.split(None,1);name=name.strip()
    if Path(name).suffix.lower() in [".csv",".json",".png"]:
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest: raise AssertionError("Locked artifact changed: "+name)
        checked+=1
audit=json.loads((root/"cohort_audit_locked.json").read_text())
assert audit["positive"]+audit["negative"]==audit["definitive_records"]==359
assert audit["source_records"]-audit["borderline_excluded"]==359

groups=defaultdict(list)
for r in records("dml_raw_final.csv"): groups[(r["scenario"],r["n"],r["learner"])].append(r)
for summary in records("dml_summary_final.csv"):
    key=(summary["scenario"],summary["n"],summary["learner"]);g=groups[key]
    estimates=[float(x["estimate"]) for x in g];truth=float(summary["truth"])
    assert len(g)==int(summary["repetitions"])
    close(statistics.mean(estimates),summary["mean_estimate"],str(key)+" mean")
    close(statistics.mean(estimates)-truth,summary["bias"],str(key)+" bias")
    close(math.sqrt(statistics.mean((e-truth)**2 for e in estimates)),summary["rmse"],str(key)+" RMSE")
    close(statistics.mean(float(x["ci_low"])<=truth<=float(x["ci_high"]) for x in g),summary["coverage_95"],str(key)+" coverage")

synthetic=defaultdict(list)
for row in records("synthetic_benchmark_raw.csv"): synthetic[row["generator"]].append(row)
for summary in records("synthetic_benchmark_summary.csv"):
    group=synthetic[summary["generator"]];assert len(group)==int(summary["repetitions"])
    for metric in ["marginal_tv","age_ks","association_mae","holdout_auc","holdout_brier","dcr_ratio","exact_match_rate"]:
        close(statistics.mean(float(r[metric]) for r in group),summary[metric],summary["generator"]+" "+metric)
print(f"PASS: {checked} numerical/figure hashes, cohort totals, {len(groups)} DML summaries and three synthetic-generator summaries")
print("Scope: aggregate arithmetic and integrity; no new clinical or Monte Carlo fit, or privacy guarantee.")

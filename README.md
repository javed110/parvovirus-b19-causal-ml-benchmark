# Parvovirus B19 causal machine-learning benchmark

Reproducible research materials for **“DAG-guided benchmarking of causal machine learning for Parvovirus B19 IgG serostatus: a simulation study and data-quality audit.”**

**Authors:** Mehnaz Akhtar, Sobia Manzoor, and Javed Ashraf  
**Target journal:** *BMC Medical Research Methodology*  
**Repository status:** research artifact accompanying a manuscript prepared for submission; not yet peer reviewed.

## Why this project matters

Small, irregular hospital workbooks are a hostile environment for flexible causal machine learning. This project uses one such legacy Parvovirus B19 workbook as a realistic data-quality template, then separates what the observed data can support from what must be evaluated under known truth:

1. a privacy-preserving aggregate audit of the hospital workbook;
2. parametric simulations for DoubleMLIRM and CausalForestDML benchmarking; and
3. a train-synthetic/test-real benchmark for Gaussian copula, CTGAN, and TVAE generators.

The observed clinical strata were not treated as interventions. In particular, the “Unspecified” category lacks a defined clinical pathway and is not exchangeable with the named strata. No causal effect was estimated from the hospital cohort.

## Evidence layers

### Aggregate clinical audit

- 368 source records were audited.
- Nine borderline serology labels were excluded, leaving 359 definitive records.
- The definitive cohort contained 172 IgG-positive and 187 IgG-negative records (47.9% positive).
- The clinical data custodian verified that age was recorded in completed years.
- One missing age value was median-imputed only for the synthetic-data benchmark.
- Complete blood-count fields showed block-dependent RBC/TLC scale inconsistencies.
- Liver and renal fields had 89.1%–96.2% missingness and were excluded rather than imputed.

These data-quality features motivated the benchmark; they do not identify a clinical treatment effect.

### Causal estimator benchmark

The primary cohort-sized benchmark deliberately used **n = 359**, an exceptionally small sample for estimators that rely on asymptotic behavior. This is a stress test of their lower operating limits in constrained clinical settings.

- Seven prespecified scenarios covered null, homogeneous and heterogeneous effects, limited overlap, selective missingness, unmeasured confounding, and outcome misclassification.
- Logistic-nuisance DoubleML used 1,000 repetitions per n=359 scenario; boosted-tree nuisance models used 50.
- Selected n=1,000 and n=5,000 scenarios evaluated scaling behavior.
- CausalForestDML used 20 repetitions at n=359 and n=1,000.
- Repeated sample splitting used 30 partitions per nuisance learner.
- The locked analyses reported zero numerical failures.

At n=359, logistic DoubleML bias was 0.0012 for the homogeneous-effect scenario, while limited overlap approximately doubled RMSE from 0.0543 to 0.1053. Deliberate unmeasured confounding and outcome misclassification produced biases of 0.0161 and −0.0194, respectively. Mean CATE correlation for CausalForestDML was 0.093 at n=359 and 0.288 at n=1,000, which does not support patient-level effect interpretation.

### Synthetic-data benchmark

Generator rankings differed across marginal fidelity, association preservation, held-out predictive utility, and distance diagnostics. TVAE produced a **92.3% exact benchmark-field match rate**. Under the prespecified release screen, this is catastrophic overfitting and memorization—not a minor warning. No patient-level synthetic records from this study are released.

## Reproduce the checks

The default notebook mode verifies the locked outputs, repetition counts, checksums, figures, and reported claims without protected data.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m jupyter nbconvert --execute --to notebook --inplace Parvovirus_B19_DAG_DML_Reproducible_Analysis.ipynb --ExecutePreprocessor.timeout=600
```

Set `RUN_FULL_ANALYSIS=True` in the notebook only when a full Monte Carlo recomputation is intended. Source-dependent audit and synthetic-generator recomputation additionally require institutionally authorized access to the protected workbook through the `B19_WORKBOOK` environment variable. The workbook is not included here.

## Repository contents

- `Parvovirus_B19_DAG_DML_Reproducible_Analysis.ipynb` — complete, executed, public-safe analysis notebook.
- `dml_raw_final.csv`, `dml_summary_final.csv` — locked DoubleML simulation outputs.
- `forest_raw_full.csv`, `forest_summary_full.csv` — locked CausalForestDML outputs.
- `crossfit_stability_full.csv` — repeated sample-splitting results.
- `synthetic_benchmark_*.csv` and `synthetic_benchmark_metadata.json` — aggregate generator diagnostics only.
- `cohort_*` — non-disclosive aggregate cohort summaries and audit metadata.
- `figure1_dag.png` through `figure6_synthetic_benchmark.png` — final 300-dpi figures.
- `METHODS.md` — estimands, scenarios, estimators, and performance measures.
- `DATA_GOVERNANCE.md` — privacy boundaries and release decisions.
- `REPRODUCIBILITY.txt`, `requirements.txt`, and `MANIFEST_SHA256.txt` — environment and integrity information.

## Interpretation boundary

All estimator-performance claims arise from simulations with known truth. The hospital cohort contributes descriptive context and an aggregate data-quality audit only. Exact-match and nearest-neighbour diagnostics are release screens, not numerical re-identification probabilities or proof of anonymity.

## Responsible use

This repository contains no direct identifiers, patient-level source records, or patient-level synthetic records. Do not reconstruct or attempt to re-identify individuals. The authors remain responsible for confirming institutional approvals, journal requirements, and the final interpretation before publication.

## Citation

Use the metadata in `CITATION.cff`. Until a peer-reviewed article or DOI is available, cite this repository as a software and research artifact and include the accessed commit SHA.

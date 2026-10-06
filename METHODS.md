# Methods summary

## Study design

This methodological study separates three evidence layers: an aggregate audit of a legacy hospital workbook, simulations with known causal truth, and a tabular synthetic-data benchmark. The clinical workbook is not used to estimate a causal effect because it does not define a defensible treatment/control contrast.

## Observed-data audit

The source contained 368 records. Nine borderline serology labels were excluded, leaving 359 definitive observations. Age units were verified as completed years by the clinical data custodian. The audit evaluated outcome-label counts, optical-density arithmetic, missingness, clinical-stratum frequencies, and block-dependent RBC/TLC scale signatures.

One missing age value was handled by median imputation before the synthetic-data train/holdout split. Complete blood-count variables were excluded from synthesis because their scales changed across workbook blocks. Liver and renal variables were excluded rather than imputed because their missingness ranged from 89.1% to 96.2%.

## Causal estimand and data-generating mechanisms

The simulated exposure `A` is hypothetical and does not represent an observed diagnosis or clinical stratum. The target estimand is the average treatment effect on a binary outcome. Under heterogeneous effects, conditional effects depend on simulated age and sex covariates. Under outcome misclassification, performance is evaluated against the latent-outcome average treatment effect.

Seven scenarios were prespecified:

1. null effect;
2. homogeneous effect;
3. heterogeneous effect;
4. limited overlap;
5. selective missingness;
6. unmeasured confounding; and
7. outcome misclassification.

The n=359 benchmark intentionally probes a lower operating limit for DoubleML and causal forests. Selected n=1,000 and n=5,000 settings evaluate whether performance improves with sample size.

## Estimators

DoubleMLIRM used five-fold cross-fitting with either logistic-regression or gradient-boosted nuisance models. CausalForestDML evaluated average-effect recovery, conditional-effect RMSE, CATE rank correlation, and true subgroup separation. Repeated sample splitting assessed sensitivity to fold assignment.

## Performance measures

DoubleML performance measures include mean estimate, bias, Monte Carlo standard error of bias, empirical standard error, mean model-based standard error, RMSE, 95% interval coverage, numerical failure rate, and the fraction requiring non-orthogonal re-estimation. Forest measures include ATE bias and RMSE, CATE RMSE and correlation, and true-effect separation.

## Synthetic-data benchmark

Gaussian copula, CTGAN, and TVAE models were compared using three repetitions. The benchmark reports marginal total variation, age Kolmogorov–Smirnov distance, association-matrix error, train-synthetic/test-real predictive AUC and Brier score, distance-to-closest-record ratio, and exact benchmark-field match rate.

Exact-match and nearest-neighbour diagnostics are release screens rather than formal privacy guarantees. TVAE’s 92.3% exact benchmark-field match rate constitutes catastrophic overfitting and memorization under the prespecified release rule; patient-level synthetic data are therefore not released.

## Determinism and software

The base seed is `20260730`. The verified environment uses Python 3.12.13 with pinned package versions in `requirements.txt`. Exact output hashes appear in `MANIFEST_SHA256.txt`.

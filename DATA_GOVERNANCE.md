# Data governance and privacy boundary

## Publicly released

- Aggregate cohort counts, percentages, and missingness summaries.
- Aggregate audit metadata without direct or indirect patient identifiers.
- Parametric simulation outputs generated from known data-generating mechanisms.
- Aggregate synthetic-generator diagnostics.
- Analysis code, figures, environment specification, and integrity hashes.

## Deliberately excluded

- The hospital workbook.
- Patient identifiers, names, dates, free text, or patient-level clinical records.
- The internal de-identified patient-level extract.
- Patient-level synthetic records from every evaluated generator.
- Internal submission correspondence, reviewer-preparation documents, and authors’ private working files.

## Rationale

The real cohort is small and sparse. Off-the-shelf deep tabular synthesis did not make it safe for release: TVAE reproduced 92.3% of benchmark-field rows exactly. The study therefore treats this model as a catastrophic memorization failure and withholds every patient-level synthetic output.

The released distance and exact-match measures are screening diagnostics. They are not re-identification probabilities and do not establish anonymity. Access to the protected workbook remains subject to institutional authorization, ethics requirements, and applicable data-protection rules.

## Safe execution

The notebook runs in locked verification mode without protected data. Authorized users who need source-dependent recomputation must set `B19_WORKBOOK` to a locally governed workbook path. The loader verifies the identifier headers, discards those columns immediately, and never displays patient rows.

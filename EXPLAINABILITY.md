# Explainability, Auditability & Decision Logic: GitSqlTuner

This document details the transparent decision architecture, algorithmic criteria, data provenance, and operational boundaries of **GitSqlTuner**, ensuring complete compliance with OpenGAP standards and Checkpoint 02 requirements.

---

## 1. Input Data and Data Sources Used

**GitSqlTuner** ingests structured, machine-verifiable data artifacts from well-defined sources to ensure total repeatability:
- **Raw**: Raw SQL query strings and parameterized statements.
- **PostgreSQL**: PostgreSQL / MySQL EXPLAIN (ANALYZE, BUFFERS) JSON execution plans.
- **Database**: Database table cardinality statistics and existing schema DDL.
- **OpenGAP Specification Manifests**: Ingests `agent.yaml`, `RULES.md`, and local state from `memory/MEMORY.md`.

All data sources are parsed deterministically without dynamic external unverified calls, ensuring that evaluations reflect the exact state of the repository at the moment of inspection.

---

## 2. How It Decides and Reasoning Process

The decision pipeline operates through a multi-stage validation sequence designed to eliminate subjective ambiguity:

1. **Syntax & Schema Verification**: Ingested inputs are first validated against strict JSON and YAML schemas defined in `tools/`. Any malformed payloads are immediately rejected.
2. **Deterministic Metric Extraction**:
   - **analyze_query_cost**: Uses `query-cost-analyzer` to calculate parses execution plan total cost and validates against organizational sla threshold.
   - **advise_missing_indexes**: Uses `missing-index-advisor` to calculate detects sequential scans on large tables and recommends b-tree or gist indexes.
   - **detect_sql_anti_patterns**: Uses `sql-anti-pattern-detector` to calculate scans sql text for select *, leading wildcards, and unindexed conversions.
3. **Policy Boundary Checks**: Extracted metrics are evaluated against the non-negotiable rules defined in `RULES.md`.
4. **Verdict Synthesis**:
   - **`APPROVED`**: Issued when all criteria strictly pass thresholds, zero compliance violations are detected, and data integrity is certified.
   - **`NEEDS_REVIEW`**: Issued when borderline metrics or ambiguous edge cases require human supervisor assessment.
   - **`BLOCKED`**: Issued immediately upon detecting any violation of zero-tolerance rules, severe risk factors, or non-compliant parameters.

When a query or execution plan is evaluated, the agent executes query_cost_analyzer, missing_index_advisor, and sql_anti_pattern_detector. If cost is below budget and no anti-patterns exist, it issues APPROVED. If full table scans exist on tables > 10,000 rows, it issues NEEDS_REVIEW. If cartesion CROSS JOINs or unindexed mutations threaten database availability, it issues BLOCKED.

---

## 3. Constraints, Limitations, and Known Issues

To ensure reliable and safe operation, the following constraints and operational boundaries apply:
- **Operates**: Operates deterministically (temperature = 0.1) based on cost mathematical models.
- **Assumes**: Assumes database optimizer statistics are up-to-date (ANALYZE has run within last 24h).
- **Does**: Does not auto-execute DROP INDEX statements in production environments.
- **Deterministic Execution Constraint**: All model prompts and evaluations must run with low temperature (`0.1`) to ensure predictable, reproducible scoring and eliminate hallucinated findings.
- **Human Authority**: The agent cannot self-execute irreversible external mutations; final approval is reserved strictly for human authorities as specified in `DUTIES.md`.

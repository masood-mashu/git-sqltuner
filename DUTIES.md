# Separation of Duties (SOD) & Operational Boundaries

To ensure robust compliance, security, and verification, **GitSqlTuner** implements a strict tripartite Separation of Duties architecture.

---

### 1. Maker
* **Assigned Entity**: `GitSqlTuner Automation Engine`
* **Responsibilities**:
  * Parses SQL AST and execution plans, analyzes estimated rows and cost, and drafts targeted index recommendations.
  * Ingests raw repository data, configurations, and input artifacts.
  * Formulates candidate evaluations and structured recommendation summaries.
  * Records execution logs into `memory/audit.log`.

---

### 2. Checker
* **Assigned Entity**: `GitSqlTuner Verification & Policy Enforcer`
* **Responsibilities**:
  * Validates database write amplification trade-offs and checks existing index redundancy.
  * Audits calculations, parameter boundary limits, and zero-tolerance rule compliance.
  * Asserts schema validity on all output manifests.
  * Issues preliminary assessment: `APPROVED`, `BLOCKED`, or `NEEDS_REVIEW`.

---

### 3. Approver
* **Assigned Entity**: `Lead Database Administrator (DBA) / Principal Data Engineer (Reserved for human review).`
* **Responsibilities**:
  * Final sign-off authority for high-impact production actions.
  * Mandatory human oversight on security, legal, financial, or regulatory decisions.
  * Reviews unresolvable edge cases and policy override exceptions.

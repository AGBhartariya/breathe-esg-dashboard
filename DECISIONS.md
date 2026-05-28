# DECISIONS.md

# Major Design Decisions

---

# 1. SAP Format Choice

## Decision

Used CSV/flat-file SAP exports.

## Why

Real SAP systems expose:
- IDoc
- BAPI
- OData
- flat exports

For a 4-day prototype, CSV exports provided the best balance between:
- realism
- implementation speed
- ingestion flexibility

---

# 2. Utility Data Choice

## Decision

Used utility portal CSV exports.

## Why

Facilities teams commonly:
- export CSVs
- manually consolidate utility data

PDF parsing was intentionally avoided because:
- OCR complexity
- vendor-specific formats
- time constraints

---

# 3. Travel Data Representation

## Decision

Used normalized travel activity rows.

Examples:
- flights
- hotels
- ground transport

## Why

Real travel systems expose inconsistent schemas.

The prototype focused on:
- Scope 3 categorization
- normalization
- analyst reviewability

---

# 4. File Upload Instead of APIs

## Decision

Used CSV upload ingestion.

## Why

The assignment emphasized:
- messy enterprise data
- normalization
- analyst workflows

rather than OAuth/API integrations.

---

# 5. Flexible Header Mapping

## Decision

Implemented generalized header normalization.

## Why

Enterprise exports rarely use consistent headers.

Examples:
- qty
- quantity
- usage
- consumption

The backend maps multiple aliases dynamically.

---

# 6. Suspicious Data Strategy

## Decision

Flag suspicious rows instead of rejecting automatically.

## Why

ESG workflows require:
- analyst review
- human verification
- audit defensibility

Suspicious does not always mean invalid.

---

# 7. Why No Emissions Engine

## Decision

Did not implement emissions calculations.

## Why

The assignment focused primarily on:
- ingestion
- normalization
- reviewability

A production emissions engine would require:
- emission factor databases
- geography logic
- methodology frameworks

which were outside the intended scope.

---

# 8. Multi-Tenancy Strategy

## Decision

Used logical tenant separation via:

```python
company_name
```

## Why

Full enterprise tenancy requires:
- RBAC
- auth systems
- organization models
- row-level permissions

The simplified approach demonstrates intended architecture.

---

# 9. What I Would Ask the PM

Questions:

1. Expected ingestion scale?
2. Analyst-only uploads or automated pipelines?
3. Required audit retention duration?
4. Required emissions methodology?
5. Is utility PDF support mandatory?
6. Do analysts need row editing?
7. Should approvals become immutable?
8. Is row versioning required?

---

# 10. Intentionally Ignored

The prototype intentionally did not fully implement:

- OCR utility extraction
- live SAP connectors
- airport-code distance resolution
- currency FX conversion
- emissions calculations
- authentication systems
- async ingestion queues

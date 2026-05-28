# MODEL.md

## Overview

The system was designed to solve the core ESG ingestion problem:

- ingest messy enterprise data
- normalize inconsistent formats
- preserve auditability
- support analyst review workflows

The architecture prioritizes:
- traceability
- normalization
- suspicious data detection
- source tracking
- multi-source ingestion

---

# Core Models

## UploadBatch

Represents one ingestion event.

Examples:
- SAP upload
- Utility upload
- Travel upload

### Fields

| Field | Purpose |
|---|---|
| source_type | SAP / Utility / Travel |
| company_name | Multi-tenant isolation |
| uploaded_at | Audit timestamp |
| total_rows | Rows received |
| processed_rows | Successfully parsed rows |
| failed_rows | Invalid rows |
| suspicious_rows | Flagged rows |
| batch_status | review_pending / approved / rejected |

---

## Activity

Represents one normalized ESG activity row.

Examples:
- fuel purchase
- electricity usage
- travel activity

### Fields

| Field | Purpose |
|---|---|
| batch | Links row to upload batch |
| source_type | Source provenance |
| company_name | Tenant/company |
| activity_type | Fuel / electricity / travel |
| scope | Scope 1 / 2 / 3 |
| vendor | Vendor/provider |
| quantity | Original quantity |
| unit | Original unit |
| normalized_quantity | Standardized quantity |
| normalized_unit | Standardized unit |
| amount | Monetary amount |
| currency | Currency |
| review_status | Pending / approved / rejected |
| is_suspicious | Suspicious flag |
| uploaded_at | Audit timestamp |

---

## DataIssue

Stores suspicious or invalid row information.

### Fields

| Field | Purpose |
|---|---|
| activity | Linked activity |
| issue_type | Type of issue |
| severity | low / medium / high |
| issue_message | Human-readable explanation |
| created_at | Audit timestamp |

---

# Scope Categorization

| Activity | ESG Scope |
|---|---|
| Fuel | Scope 1 |
| Electricity | Scope 2 |
| Travel | Scope 3 |

---

# Unit Normalization

Supported conversions:

| Original | Standardized |
|---|---|
| gallons | liters |
| miles | km |
| MWh | kWh |

Normalization occurs during ingestion.

---

# Suspicious Data Detection

Implemented checks:

- negative quantity
- extremely high quantity
- missing vendor
- negative monetary amount

Suspicious rows are flagged instead of auto-rejected.

---

# Multi-Tenancy

Multi-tenancy is handled logically through:

```python
company_name
```

Every batch and activity belongs to a company.

In production:
- RBAC
- tenant permissions
- organization tables

would be added.

---

# Auditability

The system preserves:

- source system
- upload batch
- upload timestamp
- analyst decision
- suspicious issue metadata

This creates an auditable ESG review pipeline.

---

# Why This Model

The model was intentionally optimized for:

- realistic ingestion
- explainability
- audit traceability
- normalization correctness

instead of over-engineering.

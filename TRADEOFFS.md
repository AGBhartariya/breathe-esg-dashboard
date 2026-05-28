# TRADEOFFS.md

# Deliberate Tradeoffs

---

# 1. No Authentication System

## Not Built

- login/signup
- RBAC
- organization permissions

## Why

The assignment prioritized:
- ingestion
- normalization
- analyst workflows

A full auth system would significantly increase complexity without improving ESG ingestion quality.

---

# 2. No Live External APIs

## Not Built

- SAP APIs
- Concur integrations
- Utility provider APIs

## Why

The assignment focused on:
- realistic data handling
- messy exports
- normalization

CSV uploads better demonstrated those challenges.

---

# 3. No Emissions Calculation Engine

## Not Built

- emission factor matching
- carbon calculations
- regionalized methodologies

## Why

The hardest ESG problem operationally is:
- ingestion quality
- auditability
- normalization

The prototype intentionally focused there.

---

# Additional Simplifications

| Simplification | Reason |
|---|---|
| SQLite instead of Postgres | Faster prototyping |
| Manual uploads instead of queues | Simpler workflow |
| Static normalization rules | Faster implementation |
| Logical tenancy only | Avoid RBAC complexity |
| No OCR parsing | Focus on structured ingestion |

---

# Final Reflection

The prototype intentionally optimized for:

- explainability
- realistic ingestion
- normalization quality
- analyst reviewability

instead of maximizing feature count.

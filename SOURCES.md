# SOURCES.md

# Source Research and Ingestion Choices

---

# 1. SAP Fuel and Procurement Data

## Research

SAP ecosystems commonly expose data through:
- IDoc
- BAPI
- OData
- flat-file exports

Research showed many sustainability teams still rely heavily on:
- CSV exports
- Excel extracts
- manually generated operational reports

---

# Chosen Format

CSV/flat-file uploads.

---

# Why

This best represented:
- inconsistent enterprise exports
- operational analyst workflows
- messy ingestion realities

while remaining feasible within the assignment timeline.

---

# SAP Challenges Modeled

The prototype handles:
- shuffled columns
- inconsistent headers
- inconsistent units
- missing vendors
- suspicious quantities

Examples:
- qty vs quantity
- gallons vs liters
- reordered schemas

---

# Sample Data Characteristics

Included:
- fuel procurement rows
- inconsistent units
- negative quantities
- missing vendors
- suspiciously large values

These were intentionally added to simulate real onboarding issues.

---

# What Would Break in Production

Real SAP production challenges include:
- plant code lookups
- localization issues
- multilingual headers
- deeply nested exports
- custom ERP schemas

---

# 2. Utility Electricity Data

## Research

Utility data commonly arrives via:
- portal CSV exports
- PDF bills
- vendor APIs

---

# Chosen Format

Portal CSV exports.

---

# Why

This reflects common operational workflows where facilities teams:
- manually export reports
- consolidate spreadsheets
- upload monthly consumption files

---

# Utility Challenges Modeled

The prototype handles:
- inconsistent units
- billing quantities
- normalization

Examples:
- kWh
- MWh

---

# Sample Data Characteristics

Included:
- electricity usage rows
- unit variations
- suspicious usage anomalies

---

# What Would Break in Production

Real utility systems introduce:
- PDF parsing complexity
- tariff calculations
- meter hierarchies
- billing periods misaligned with months

---

# 3. Corporate Travel Data

## Research

Corporate travel systems like:
- Concur
- Navan

commonly expose:
- flight data
- hotel bookings
- ground transport

through exports or APIs.

---

# Chosen Format

CSV uploads.

---

# Why

The assignment prioritized:
- ingestion quality
- normalization
- reviewability

rather than OAuth/API integrations.

---

# Travel Challenges Modeled

The prototype handles:
- distance normalization
- category-based travel rows
- Scope 3 categorization

Examples:
- miles → km

---

# Sample Data Characteristics

Included:
- flights
- hotels
- ground transport
- suspicious travel distances

---

# What Would Break in Production

Real travel ingestion would require:
- airport-code resolution
- itinerary parsing
- duplicate booking handling
- FX normalization
- emissions factor matching

---

# Final Design Philosophy

The prototype intentionally focused on:

- realistic ingestion
- normalization quality
- suspicious data handling
- analyst review workflows
- audit traceability

rather than attempting full enterprise-scale integrations.

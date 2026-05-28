# Real-World Assumptions

This project intentionally models a realistic subset of enterprise ESG operations rather than attempting full ERP-grade integration.

Chosen assumptions include:
- SAP ingestion via flat-file exports
- Utility ingestion via portal CSV exports
- Corporate travel ingestion via downloadable expense reports

The project prioritizes:
- governance
- auditability
- normalization
- provenance tracking
- suspicious data detection

over production-scale ERP synchronization complexity.

The ingestion layer was intentionally designed to tolerate:
- shuffled columns
- inconsistent headers
- partial schemas
- operational formatting inconsistencies

because real-world ESG operational systems rarely produce perfectly standardized exports.

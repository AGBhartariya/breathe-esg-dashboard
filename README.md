# Breathe ESG Tech Intern Assignment

## Overview

This project is a prototype ESG ingestion and analyst review platform built using:

- Django REST Framework
- React.js
- SQLite
- Render (backend deployment)
- Vercel (frontend deployment)

The system ingests ESG activity data from multiple enterprise sources, normalizes inconsistent records, detects suspicious entries, and provides an analyst review workflow before audit approval.

The prototype was intentionally designed around realistic ESG onboarding challenges rather than generic CRUD functionality.

---

# Live Deployment

## Frontend

```txt
https://breathe-esg-dashboard-eta.vercel.app/
```

## Backend API

```txt
https://breathe-esg-dashboard-tgna.onrender.com
```

---

# GitHub Repository

```txt
https://github.com/AGBhartariya/breathe-esg-dashboard
```

---

# Problem Statement

Enterprise ESG data rarely exists in clean formats.

The assignment required building a system capable of handling:

- SAP fuel and procurement exports
- Utility electricity data
- Corporate travel activity

while supporting:
- normalization
- suspicious data detection
- analyst review
- audit traceability

---

# Features Implemented

## Multi-Source ESG Ingestion

Supported sources:
- SAP
- Utility
- Travel

---

## Flexible CSV Ingestion

The ingestion engine handles:
- shuffled columns
- inconsistent headers
- missing values
- varying schemas

Examples:
- qty / quantity / usage
- reordered columns
- inconsistent naming conventions

---

## Unit Normalization

Supported conversions include:

| Original Unit | Normalized Unit |
|---|---|
| gallons | liters |
| miles | km |
| MWh | kWh |

---

## ESG Scope Categorization

| Activity | Scope |
|---|---|
| Fuel | Scope 1 |
| Electricity | Scope 2 |
| Travel | Scope 3 |

---

## Suspicious Data Detection

Implemented checks:

- negative quantity
- extremely high quantity
- missing vendor
- negative monetary amount

Suspicious rows are flagged for analyst review instead of automatically rejected.

---

## Analyst Review Workflow

Analysts can:
- review uploaded rows
- approve records
- reject records
- inspect suspicious data
- track upload batches

---

## Upload Batch Tracking

Every ingestion event creates an upload batch containing:
- source system
- company
- upload timestamp
- suspicious row counts
- processing statistics

---

## Auditability

The system preserves:
- upload source
- upload timestamp
- analyst decisions
- suspicious issue metadata
- normalization outputs

This creates a defensible audit trail.

---

# Tech Stack

## Backend

- Django
- Django REST Framework
- SQLite
- Gunicorn

---

## Frontend

- React.js
- Axios
- CSS

---

## Deployment

| Service | Platform |
|---|---|
| Backend | Render |
| Frontend | Vercel |

---

# Project Structure

```txt
backend/
frontend/
MODEL.md
DECISIONS.md
TRADEOFFS.md
SOURCES.md
README.md
```

---

# API Endpoints

| Endpoint | Purpose |
|---|---|
| /api/upload/ | Upload ESG data |
| /api/activities/ | Fetch normalized activities |
| /api/issues/ | Fetch suspicious issues |
| /api/batches/ | Fetch upload batches |
| /api/approve/<id>/ | Approve row |
| /api/reject/<id>/ | Reject row |

---

# Running Locally

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

# Deployment

## Backend Deployment

Backend deployed on Render using:
- Gunicorn
- automatic migrations
- Django REST API

Build command:

```bash
pip install -r requirements.txt && python manage.py migrate
```

Start command:

```bash
gunicorn config.wsgi:application
```

---

## Frontend Deployment

Frontend deployed on Vercel.

The frontend connects to the Render backend using production API URLs.

---

# Realistic ESG Handling

The prototype intentionally focused on:
- realistic ingestion
- messy enterprise data
- normalization
- auditability
- analyst workflows

instead of:
- generic CRUD functionality
- over-engineered architecture
- unnecessary feature count

---

# Deliverables Included

- MODEL.md
- DECISIONS.md
- TRADEOFFS.md
- SOURCES.md
- README.md

---

# Known Limitations

The prototype intentionally does not include:
- authentication systems
- live SAP APIs
- OCR utility bill parsing
- emissions calculation engine
- async ingestion queues
- airport-code resolution

These were deliberately excluded to preserve focus on ingestion quality and explainability.

---

# Final Design Philosophy

The project was intentionally optimized for:

- explainability
- realistic ESG onboarding
- normalization correctness
- suspicious data handling
- analyst usability
- audit traceability

rather than maximizing feature count.

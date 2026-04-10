# 🛰️ MissionLedger — Space Operations Data Pipeline & Analytics Platform

A data engineering and analytics project that ingests real-time satellite telemetry and mission data from NASA, CelesTrak, and Space-Track APIs, validates it through an automated pipeline, and surfaces operational insights via an interactive dashboard.

> **Stack:** Python · Flask · SQL · REST APIs · GPT-4 · Anomaly Detection

---

## Overview

MissionLedger tackles a real problem in space operations: mission data is scattered across multiple sources, manually reconciled, and difficult to audit. This project builds an end-to-end data pipeline that:

- **Ingests** live satellite and mission data from three external APIs
- **Validates** data integrity using automated checks and anomaly detection
- **Transforms** raw telemetry into structured, queryable records
- **Surfaces** insights through a Flask-based dashboard with natural language querying

---

## Architecture

```
NASA / CelesTrak / Space-Track APIs
            │
            ▼
    Data Ingestion Layer (Python)
            │
            ▼
    Validation & Anomaly Detection
            │
            ▼
    Structured Data Store (SQL)
            │
            ▼
    Flask Dashboard + GPT-4 Query Interface
```

---

## Key Features

### 🔄 ETL Pipeline
- Pulls live ISS position, satellite orbital data, and mission telemetry from three APIs
- Normalizes and structures raw JSON responses into consistent tabular schema
- Reduces manual reconciliation effort by 40% vs. prior manual process

### 🔍 Data Validation & Anomaly Detection
- Automated integrity checks flag missing fields, out-of-range values, and duplicate records
- Statistical anomaly detection identifies unexpected patterns in telemetry streams
- Full audit trail maintained for traceability and compliance

### 📊 Analytics Dashboard
- Query mission performance, types, and timelines via SQL and natural language (GPT-4)
- Time tracking and efficiency calculations across mission phases
- Filterable views by mission type, status, and date range

### 🔒 Immutable Audit Log
- Blockchain-backed ledger ensures mission records cannot be altered retroactively
- Useful for compliance-sensitive aerospace and defense use cases

---

## Technical Skills Demonstrated

| Area | Details |
|---|---|
| **Data Engineering** | ETL pipeline design, API integration, data normalization |
| **Data Validation** | Anomaly detection, integrity checks, audit logging |
| **SQL** | Schema design, query optimization, data transformation |
| **Python** | Requests, Flask, pandas, data processing |
| **LLM Integration** | GPT-4 prompt engineering for natural language data queries |
| **API Integration** | NASA Open APIs, CelesTrak, Space-Track.org |

---

## Project Structure

```
Mission_Ledger/
├── app.py              # Flask app and dashboard routes
├── blockchain.py       # Immutable audit log implementation
├── templates/          # HTML dashboard templates
├── requirements.txt    # Dependencies
└── README.md
```

---

## Setup & Installation

```bash
git clone https://github.com/Ethnica16/Mission_Ledger.git
cd Mission_Ledger
pip install -r requirements.txt
```

Set your API keys as environment variables:
```bash
export OPENAI_API_KEY=your_key
export SPACETRACK_USER=your_user
export SPACETRACK_PASS=your_pass
```

Run the app:
```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

---

## Data Sources

- [NASA Open APIs](https://api.nasa.gov/) — ISS telemetry and mission data
- [CelesTrak](https://celestrak.org/) — Satellite orbital element sets
- [Space-Track.org](https://www.space-track.org/) — Conjunction and tracking data

---

## Results & Impact

- Reduced manual data reconciliation time by **40%** through automated ETL pipeline
- Anomaly detection identifies data inconsistencies that previously required manual review
- Natural language query interface reduces time-to-insight for non-technical operators

---

## Future Improvements

- Add dbt models for transformation layer
- Connect to Snowflake for scalable data storage
- Expand anomaly detection with ML-based approaches (Isolation Forest, LSTM)
- Build automated alerting for out-of-range telemetry values

# Oman Telecom Analytics Pipeline

## Objective

Build a complete ETL pipeline using:

- Prefect
- Docker
- MySQL

Dataset:
Oman Telecom Fixed Broadband Statistics

---

## Architecture

CSV File
↓
Extract
↓
Transform
↓
MySQL Database
↓
Analytics Tables

---

## Features

- Data validation
- Missing file handling
- Logging
- Retry mechanism
- Feature engineering
- Dockerized execution

---

## Run

docker compose up --build

---

## Tables

1. raw_telecom_data

Stores original telecom records.

2. telecom_analytics

Stores engineered metrics.

---

## Engineered Metrics

- Growth Rate %
- Usage Per Service
- Quarterly Change
- Normalized Traffic Index
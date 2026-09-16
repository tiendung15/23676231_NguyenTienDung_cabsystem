# Human Mobility Operations API

The supplied GitHub repository `tiendung15/SRS.md` was empty on 2026-09-09, so this workspace contains an explicitly marked baseline derived from the requested domains (`customer` and `driver manager`). It models human workflows rather than only data storage.

## Functional requirements baseline

- FR-01 Customer registers, manages profile, requests a trip, views history, and cancels a trip.
- FR-02 Driver Manager onboards drivers, monitors availability, views dashboard/team, and assigns drivers.
- FR-03 Driver changes operational availability and receives assigned work.
- FR-04 Dispatcher or manager updates trip lifecycle from requested to completed/cancelled.
- FR-05 Customer pays for a trip and checks payment status.
- FR-06 Customer rates a completed trip.
- FR-07 Customer opens a support ticket and support staff resolves it.
- FR-08 Users read and acknowledge notifications.
- FR-09 Admin audits operational resources and service health.
- FR-10 System enforces validation and returns actionable errors.

## API specifications

The `specs/` directory contains 12 independent OpenAPI 3.0 YAML documents. Each document owns a functional area and includes multiple human-facing operations.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

The implementation is intentionally in-memory for traceability from FR to API to code. Replace `_store` with a database repository before production use.

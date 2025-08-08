# Rove Synthetic – Redemption Optimizer

Estimate value-per-mile and get ranked redemption recommendations via a simple web UI.

## Features
- Value-per-mile calculator for flight, hotel, gift card redemptions
- Synthetic routing with mock fallback if API creds are missing
- Recommendation engine, ranked by value-per-mile
- Flask UI to input trip details and collect feedback (SQLite)

## Setup
1. Python 3.10+
2. Create and activate venv, install deps:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure `.env` (see `.env.example`):
   - `APP_SECRET_KEY` (any value for dev)
   - Optional: `AMADEUS_API_KEY`, `AMADEUS_API_SECRET` (live calls); otherwise mock data is used

## Run
```bash
python app.py
```
Visit http://127.0.0.1:5000

## Files
- `value_calc.py` – VPM math and examples
- `routing.py` – Parse offers, compute VPM, rank routes (mock fallback)
- `recommender.py` – Orchestrates recommendations
- `app.py` – Flask web server
- `templates/` – UI templates
- `sql_lite.py` – Feedback storage in SQLite

## User Testing
See `USER_TESTS.md` for a quick test checklist and notes. 
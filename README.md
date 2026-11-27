# Ad Data Connector

A small Flask service that sits in front of an advertising platform's REST API and returns its data in a shape a data pipeline can load directly. It does two things:

- **`GET /api/accounts`**: lists ad accounts as `{accountName, accountId}`.
- **`GET /api/adData`**: returns one account's campaign metrics for a date range as `columns` + `rows`, so the result maps straight onto a table.

Requests are authenticated with a bearer token. Upstream HTTP errors are passed through with their status code, and every request and failure is logged.

## Quick start

Needs Python 3.11+.

```bash
git clone https://github.com/mpahlavan/ad-data-connector.git
cd ad-data-connector
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # set BASE_URL (the upstream API) and AUTH_TOKEN
cd app && python app.py       # serves on http://127.0.0.1:5555
```

```bash
curl -H "Authorization: Bearer $AUTH_TOKEN" http://127.0.0.1:5555/api/accounts
curl -H "Authorization: Bearer $AUTH_TOKEN" \
  "http://127.0.0.1:5555/api/adData?accountId=<id>&start=2024-05-01&end=2024-05-31"
```

## Tests

The tests mock the upstream API, so they run offline with no credentials:

```bash
pip install -r requirements-dev.txt
pytest -q                     # 8 tests: auth, both endpoints, validation, upstream errors, 404
```

## Endpoints

### `GET /api/accounts`

```json
[
  { "accountName": "Account1", "accountId": "4d2b35432947" },
  { "accountName": "Account2", "accountId": "e1f0c2a9b311" }
]
```

### `GET /api/adData?accountId=&start=&end=`

All three query parameters are required (`start` and `end` as `YYYY-MM-DD`); a missing one returns `400`.

```json
{
  "columns": ["campaign_id", "clicks", "conversions", "cost", "date", "impressions"],
  "rows": [
    ["2025", 21, 5, 34.47, "2024-05-01", 501],
    ["2025", 31, 5, 48.01, "2024-05-01", 448]
  ]
}
```

| Status | When |
|---|---|
| 200 | Success |
| 400 | Missing query parameter |
| 403 | Missing or wrong bearer token |
| 404 | Unknown route |
| 4xx/5xx | Passed through from the upstream API |

## Layout

```
app/app.py                          Flask app, token check, routes, error handlers
app/controllers/connector_controller.py   reshapes upstream responses
app/utils/respond.py                upstream HTTP client and JSON responses
tests/test_app.py                   endpoint tests with the upstream mocked
```

## Known limitations

- One token is used both to authenticate callers and to call the upstream API. A production version would separate them, so callers never hold the upstream credential.
- Calls are synchronous with no retry or pagination; large date ranges would need both.

# Funnel Connector

This project provides a connector for fetching advertising data from the Sultek Data In API. The connector is built using Flask and can handle two tasks: fetching account information and fetching advertising data for a specific account within a specified date range.

## Prerequisites 
- Python 3.11.2
- VSCode


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mpahlavan/funnel-connector.git
    cd funnel-connector
    python -m venv venv
    source venv/bin/activate 
    ```

2. Install the required packages:


    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. The application will start on port 5555. You can access the following endpoints:

### Endpoints

#### Fetch Account Information

- **URL:** `/api/accounts`
- **Method:** `GET`
- **Headers:**
  - `Authorization: **********`
- **Response:**
    ```json
  [
    {
        "accountId": "4**********`",
        "accountName": "Account1"
    },
    {
        "accountId": "e**********`",
        "accountName": "Account2"
    }
]
    ```

#### Fetch Advertising Data

- **URL:** `/api/adData`
- **Method:** `GET`
- **Headers:**
  - `Authorization: **********`
- **Query Parameters:**
  - `accountId` (required): The ID of the ad account.
  - `start` (required): The start date in YYYY-MM-DD format.
  - `end` (required): The end date in YYYY-MM-DD format.
- **Response:**
    ```json
    {
        "columns": [
        "campaign_id",
        "clicks",
        "conversions",
        "cost",
        "date",
        "impressions"
        ],
        "rows": [
            [
            "2025",
            21,
            5,
            34.47,
            "2024-05-01",
            501
            ],
            [
            "2025",
            31,
            5,
            48.01,
            "2024-05-01",
            448
            ]
        ]
    }
    ```

## Example Requests

### Fetch Account Information

```bash
curl -H "Authorization: Bearer bb6d467a123" http://127.0.0.1:5555/api/accounts
```

### Fetch Advertisement Data

```bash
curl -H "Authorization: Bearer bb6d467a123" http://127.0.0.1:5555/api/adData?accountId=4d2b35432947&start=2024-05-01&end=2024-05-31
```

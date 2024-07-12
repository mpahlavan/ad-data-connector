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
  - `Authorization: bb6d467a123`
- **Response:**
    ```json
    [
        {
            "accountName": "Account Name",
            "accountId": "Account Id"
        }
    ]
    ```

#### Fetch Advertising Data

- **URL:** `/api/adData`
- **Method:** `GET`
- **Headers:**
  - `Authorization: bb6d467a123`
- **Query Parameters:**
  - `accountId` (required): The ID of the ad account.
  - `start` (required): The start date in YYYY-MM-DD format.
  - `end` (required): The end date in YYYY-MM-DD format.
- **Response:**
    ```json
    {
        "columns": ["column1", "column2", ...],
        "rows": [
            ["row1column1Value", "row1column2Value", ...],
            ["row2column1Value", "row2column2Value", ...]
        ]
    }
    ```

## Example Requests

### Fetch Account Information

```bash
curl -H "Authorization: bb6d467a123" http://127.0.0.1:5555/api/accounts

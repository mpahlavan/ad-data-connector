from utils.respond import Responder, CallAPI

api_caller = CallAPI()
responder = Responder()

def get_account_info():
    """
    Fetches account information from the API and formats it.

    Returns:
        tuple: A tuple containing the formatted account information and the HTTP status code.
    """
    try:
        data = api_caller.get('adAccounts')
        if 'error' in data:
            return responder.error(data['error'], data.get('status_code', 500))

        formatted_accounts = [{'accountName': account['name'], 'accountId': account['id']} for account in data]
        return responder.success(formatted_accounts)
    except Exception as e:
        return responder.error(str(e), 500)

def get_ad_data(account_id, start_date, end_date):
    """
    Fetches advertising data for a specific account and date range from the API and formats it.

    Args:
        account_id (str): The ID of the account to fetch data for.
        start_date (str): The start date for the data range (YYYY-MM-DD).
        end_date (str): The end date for the data range (YYYY-MM-DD).

    Returns:
        tuple: A tuple containing the formatted advertising data and the HTTP status code.
    """
    params = {'start': start_date, 'end': end_date}
    try:
        data = api_caller.get(f'getData/{account_id}', params=params)
        if 'error' in data:
            return responder.error(data['error'], data.get('status_code', 500))

        if not data:
            return responder.success({"columns": [], "rows": []})

        columns = list(data[0].keys())
        rows = [[entry[column] for column in columns] for entry in data]

        return responder.success({"columns": columns, "rows": rows})
    except Exception as e:
        return responder.error(str(e), 500)

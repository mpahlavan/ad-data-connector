import requests
from flask import jsonify
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
TOKEN = os.getenv('TOKEN')

def get_account_info():
    headers = {'Authorization': TOKEN}
    response = requests.get(f'{BASE_URL}/demo/adAccounts', headers=headers)
    accounts = response.json().get('ad_accounts', [])
    formatted_accounts = [{'accountName': account['name'], 'accountId': account['id']} for account in accounts]
    return jsonify(formatted_accounts)

def get_ad_data(account_id, start_date, end_date):
    headers = {'Authorization': TOKEN}
    params = {'start': start_date, 'end': end_date}
    response = requests.get(f'{BASE_URL}/demo/getData/{account_id}', headers=headers, params=params)
    ad_data = response.json().get('data', [])

    if not ad_data:
        return jsonify({"columns": [], "rows": []})

    columns = list(ad_data[0].keys())
    rows = [[entry[column] for column in columns] for entry in ad_data]

    return jsonify({"columns": columns, "rows": rows})

from flask import Flask, request, jsonify
from controllers.connector_controller import get_account_info, get_ad_data
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

AUTH_TOKEN = os.getenv('AUTH_TOKEN')

def token_required(f):
    def wrap(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            if token == AUTH_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"message": "Token is missing or invalid!"}), 403
    wrap.__name__ = f.__name__
    return wrap


@app.route('/api/accounts', methods=['GET'])
@token_required
def accounts():
    return get_account_info()

@app.route('/api/adData', methods=['GET'])
@token_required
def ad_data():
    account_id = request.args.get('accountId')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    return get_ad_data(account_id, start_date, end_date)

if __name__ == '__main__':
    app.run(port=5555)


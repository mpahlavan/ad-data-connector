from flask import Flask, request, jsonify
from controllers.connector_controller import get_account_info, get_ad_data
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv(override=True)

app = Flask(__name__)

# Get the token from environment variables
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def token_required(f):
    """
    Decorator to check for the presence of a valid token in the request headers.

    Args:
        f (function): The view function to wrap.

    Returns:
        function: The wrapped function which includes token validation.
    """
    def wrap(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            if token == AUTH_TOKEN:
                return f(*args, **kwargs)
        logger.warning("Invalid or missing token.")
        return jsonify({"message": "Token is missing or invalid!"}), 403
    wrap.__name__ = f.__name__
    return wrap

@app.route('/api/accounts', methods=['GET'])
@token_required
def accounts():
    """
    Endpoint to fetch and return account information.

    Returns:
        Response: A JSON response containing account information or an error message.
    """

    try:
        return get_account_info()
    except Exception as e:
        logger.error(f"Error fetching account info: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/adData', methods=['GET'])
@token_required
def ad_data():
    """
    Endpoint to fetch and return advertising data for a specific account and date range.

    Returns:
        Response: A JSON response containing advertising data or an error message.
    """
    account_id = request.args.get('accountId')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if not account_id or not start_date or not end_date:
        logger.warning("Missing required query parameters.")
        return jsonify({"message": "Missing required query parameters!"}), 400
    try:
        return get_ad_data(account_id, start_date, end_date)
    except Exception as e:
        logger.error(f"Error fetching ad data: {e}")
        return jsonify({"error": str(e)}), 500

# Handle 404 errors
@app.errorhandler(404)
def not_found_error(error):
    """
    Handler for 404 Not Found errors.

    Args:
        error (Exception): The error that triggered this handler.

    Returns:
        Response: A JSON response with a 404 error message.
    """
    logger.warning(f"Endpoint not found: {request.url}")
    return jsonify({"error": "Endpoint not found"}), 404

# Handle 500 errors
@app.errorhandler(500)
def internal_error(error):
    """
    Handler for 500 Internal Server errors.

    Args:
        error (Exception): The error that triggered this handler.

    Returns:
        Response: A JSON response with a 500 error message.
    """
    logger.error(f"Internal server error: {request.url} - {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(port=5555)

import os
import requests
from dotenv import load_dotenv
import logging
from flask import jsonify

# Load environment variables from .env file
load_dotenv(override=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Responder:
    """
    A class to handle API response formatting and logging.
    """
    def __init__(self):
        """
        Initializes the Responder class with environment variables.
        """
        self.auth_token = os.getenv('AUTH_TOKEN')
        self.base_url = os.getenv('BASE_URL')
    
    def success(self, data):
        """
        Formats a successful JSON response.

        Args:
            data (dict): The data to include in the response.

        Returns:
            Response: A Flask JSON response with status code 200.
        """
        logger.info("Request successful.")
        return jsonify(data), 200
    
    def error(self, message, status_code=500):
        """
        Formats an error JSON response.

        Args:
            message (str): The error message to include in the response.
            status_code (int, optional): The HTTP status code for the response. Defaults to 500.

        Returns:
            Response: A Flask JSON response with the specified error message and status code.
        """
        logger.error(f"Error: {message}")
        return jsonify({"error": message}), status_code

class CallAPI:
    """
    A class to handle API calls with authorization and error handling.
    """
    def __init__(self) -> None:
        """
        Initializes the CallAPI class with environment variables.
        """
        self.BASE_URL = (os.getenv('BASE_URL') or '').rstrip('/') + '/demo/'
        self.auth_token = os.getenv('AUTH_TOKEN')
        self.headers = {'Authorization': f'Bearer {self.auth_token}'}
    
    def get(self, endpoint, headers: dict = None, params: dict = None):
        """
        Makes a GET request to the specified endpoint with optional headers and parameters.

        Args:
            endpoint (str): The API endpoint to make the request to.
            headers (dict, optional): Additional headers for the request.
            params (dict, optional): Query parameters for the request.

        Returns:
            dict: The JSON response from the API, or an error message if the request failed.
        """
        headers = headers or {}
        headers.update(self.headers)
        
        try:
            logger.info(f"Making GET request to {self.BASE_URL + endpoint} with params: {params}")
            response = requests.get(self.BASE_URL + endpoint, headers=headers, params=params)
            response.raise_for_status()

            logger.info(f"Response status code: {response.status_code}")
            return response.json().get('data', {})

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
            return {'error': str(http_err), 'status_code': response.status_code, 'response': response.text}
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request error occurred: {req_err}")
            return {'error': str(req_err)}

import requests
from flask_restful import Resource


class Summary(Resource):
    def __init__(self, log, config):
        """
        Initialize the Summary resource.

        Args:
            log (logging.Logger): Logger object.
            config (configparser.ConfigParser): ConfigParser object.
        """
        self.logger = log
        self.config = config

    def get(self):
        """
        Handle the GET request for the Summary resource.

        Retrieves the summary data from the specified URL and returns it as a
        JSON response.
        If the API response has a status code of 200 (successful), the data is
        returned along with a status code of 200.
        Otherwise, an error message and the response status code are returned.

        Returns:
            Returns the response data and the corresponding status code.
        """
        url = "https://api.bittrex.com/v3/markets/summaries"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data, 200
        else:
            error_message = {
                'error': 'Failed to retrieve data from the summary url'
                }
            return error_message, response.status_code


class SymbolSummary(Resource):
    def __init__(self, log, config):
        """
        Initialize the SymbolSummary resource.

        Args:
            log (logging.Logger): Logger object.
            config (configparser.ConfigParser): ConfigParser object.
        """
        self.logger = log
        self.config = config

    def get(self, marketSymbol):
        """
        Handle the GET request for the SymbolSummary resource.

        Retrieves the summary data for a specific market symbol from the
        specified URL and returns it as a JSON response.
        If the API response has a status code of 200 (successful), the data
        is returned along with a status code of 200.
        Otherwise, an error message and the response status code are returned.

        Args:
            marketSymbol (str): The market symbol to retrieve data for.

        Returns:
            Returns the response data and the corresponding status code.
        """
        url = f"https://api.bittrex.com/v3/markets/{marketSymbol}/summary"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data, 200
        else:
            msg = f'Failed to retrieve data for {marketSymbol} symbol'
            error_message = {'error': msg}
            return error_message, response.status_code

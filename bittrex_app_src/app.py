import logging
from flask import Flask
from flask_restful import Api
from bittrex_app_src.config_parse import ConfigParse
# from config_parse import ConfigParse
from bittrex_app_src.summary import Summary, SymbolSummary

logger = logging.getLogger("app")


def resources(api, logger, config):
    """
    This method will add resources to the Flask API.

    This function adds the specified resources to the Flask API object
    provided as an argument.
    It iterates through the `urls` dictionary, which maps resource classes
    to their corresponding URL paths.
    For each key-value pair in the dictionary, it calls the `api.add_resource`
    method to add the resource to the API with the given URL and
    resource_class_kwargs.

    Args:
        api (FlaskRestful.Api): Flask API object.
        logger (logging.Logger): Logger object.
        config (configparser.ConfigParser): ConfigParser object.
    """
    urls = {
        Summary: '/api.bittrex.com/v3/markets/summaries',
        SymbolSummary: '/api.bittrex.com/v3/markets/<marketSymbol>'
    }
    for key, value in urls.items():
        api.add_resource(
            key,
            value,
            resource_class_kwargs={'log': logger, 'config': config}
            )


def start_service():
    """
    This method will start the service.

    This function initializes the Flask application and starts the service.
    It reads the configuration from the 'config.cfg' file using the
    ConfigParse class.
    If the configuration is successfully loaded, it creates an instance of the
    Flask application, adds resources to the API, and runs the application.
    """
    config = ConfigParse().read_config('config.cfg')
    app = Flask(__name__)
    if config:
        api = Api(app)
        resources(api, logger, config)
        app.run(host='0.0.0.0')


if __name__ == '__main__':
    try:
        start_service()
    except Exception as exe:
        logger.error(f"Exception: {exe}")

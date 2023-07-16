from bittrex_app_src.config_parse import ConfigParse
from bittrex_app_src.summary import Summary, SymbolSummary
from bittrex_app_src.app import resources
from unittest.mock import MagicMock, patch


def test_config_parse():
    """
    Testing the ConfigParse class's read_config method.

    This function verifies the behavior of the read_config method
    in the ConfigParse class.
    It checks if the method correctly reads and returns a valid configuration
    file, and returns None for an invalid configuration file.
    """
    config_parser = ConfigParse()
    config = config_parser.read_config('config.cfg')
    assert config is not None
    invalid_config = config_parser.read_config('invalid.cfg')
    assert invalid_config is None


def test_resources(
        mock_api=MagicMock(),
        mock_logger=MagicMock(),
        mock_config_parse=MagicMock()
        ):
    """
    Testing the resources function.

    This function verifies that the resources function correctly adds
    the expected resources to the provided API object.
    It checks if the add_resource method is called the expected number of
    times and with the correct arguments.

    Args:
        mock_api (MagicMock): Mocked API object.
        mock_logger (MagicMock): Mocked logger object.
        mock_config_parse (MagicMock): Mocked ConfigParse object.
    """
    resources(mock_api, mock_logger, mock_config_parse)
    assert mock_api.add_resource.call_count == 2
    mock_api.add_resource.assert_any_call(
        Summary, '/api.bittrex.com/v3/markets/summaries',
        resource_class_kwargs={
            'log': mock_logger,
            'config': mock_config_parse
            })
    mock_api.add_resource.assert_any_call(
        SymbolSummary, '/api.bittrex.com/v3/markets/<marketSymbol>',
        resource_class_kwargs={
            'log': mock_logger,
            'config': mock_config_parse
            })


def test_summary_get_successful():
    """
    Testing the get method of the Summary class for a successful API response.

    This function tests the behavior of the get method in the Summary class
    when the API response has a status code of 200 (successful).
    It mocks the requests.get function to return a successful response with
    a sample JSON payload.
    The function verifies that the get method returns the expected response
    and status code.
    """
    mock_logger = MagicMock()
    mock_config = MagicMock()
    summary = Summary(mock_logger, mock_config)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "symbol": "ABYSS-BTC",
            "high": "0.000000410000",
            "low": "0.000000390000",
            "volume": "78365.07566750",
            "quoteVolume": "0.03192464",
            "percentChange": "-2.44",
            "updatedAt": "2023-07-15T15:36:41.713Z"
            }
            ]

    with patch('requests.get', return_value=mock_response) as mock_get:
        response, status_code = summary.get()

    assert response == [
        {
            "symbol": "ABYSS-BTC",
            "high": "0.000000410000",
            "low": "0.000000390000",
            "volume": "78365.07566750",
            "quoteVolume": "0.03192464",
            "percentChange": "-2.44",
            "updatedAt": "2023-07-15T15:36:41.713Z"
            }
            ]
    assert status_code == 200
    mock_get.assert_called_once_with(
        'https://api.bittrex.com/v3/markets/summaries'
        )


def test_summary_get_failed():
    """
    Testing the get method of the Summary class for a failed API response.

    This function tests the behavior of the get method in the Summary class
    when the API response has a status code of 404 (failed).
    It mocks the requests.get function to return a failed response with a
    status code of 404.
    The function verifies that the get method returns the expected error
    response and status code.
    """
    mock_logger = MagicMock()
    mock_config = MagicMock()
    summary = Summary(mock_logger, mock_config)

    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch('requests.get', return_value=mock_response) as mock_get:
        response, status_code = summary.get()

    assert response == {
        'error': 'Failed to retrieve data from the summary url'
        }
    assert status_code == 404
    mock_get.assert_called_once_with(
        'https://api.bittrex.com/v3/markets/summaries'
        )


def test_symbol_summary_get_successful():
    """
    Testing the get method of the SymbolSummary class for a successful
    API response.

    This function tests the behavior of the get method in the SymbolSummary
    class when the API response has a status code of 200 (successful).
    It mocks the requests.get function to return a successful response with
    a sample JSON payload.
    The function verifies that the get method returns the expected response
    and status code.
    """
    mock_logger = MagicMock()
    mock_config = MagicMock()
    symbol_summary = SymbolSummary(mock_logger, mock_config)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "symbol": "ADA-BTC",
        "high": "0.000011110000",
        "low": "0.000010210000",
        "volume": "440418.06052605",
        "quoteVolume": "4.71093042",
        "percentChange": "0.74",
        "updatedAt": "2023-07-15T17:54:07.5Z"
        }

    with patch('requests.get', return_value=mock_response) as mock_get:
        response, status_code = symbol_summary.get('ADA-BTC')

    assert response == {
        "symbol": "ADA-BTC",
        "high": "0.000011110000",
        "low": "0.000010210000",
        "volume": "440418.06052605",
        "quoteVolume": "4.71093042",
        "percentChange": "0.74",
        "updatedAt": "2023-07-15T17:54:07.5Z"
        }
    assert status_code == 200
    mock_get.assert_called_once_with(
        'https://api.bittrex.com/v3/markets/ADA-BTC/summary'
        )


def test_symbol_summary_get_failed():
    """"
    Testing the get method of the SymbolSummary class for a failed API
    response.

    This function tests the behavior of the get method in the SymbolSummary
    class when the API response has a status code of 404 (failed).
    It mocks the requests.get function to return a failed response with a
    status code of 404.
    The function verifies that the get method returns the expected error
    response and status code.
    """
    mock_logger = MagicMock()
    mock_config = MagicMock()
    symbol_summary = SymbolSummary(mock_logger, mock_config)

    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch('requests.get', return_value=mock_response) as mock_get:
        response, status_code = symbol_summary.get('ADA-BT')

    assert response == {
        'error': 'Failed to retrieve data for ADA-BT symbol'
        }
    assert status_code == 404
    mock_get.assert_called_once_with(
        'https://api.bittrex.com/v3/markets/ADA-BT/summary'
        )

import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.views import (fetch_currency_rates, fetch_stock_prices, get_greeting,
                       home_page_function, load_user_settings,
                       process_operations_data)


def test_get_greeting_morning():
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 6
        assert get_greeting() == "Доброе утро"


def test_get_greeting_afternoon():
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 13
        assert get_greeting() == "Добрый день"


def test_get_greeting_evening():
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 19
        assert get_greeting() == "Добрый вечер"


def test_get_greeting_night():
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 23
        assert get_greeting() == "Доброй ночи"


def test_load_user_settings_valid():
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = (
            '{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}'
        )
        result = load_user_settings("fake_path.json")
        assert result == {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN"],
        }


def test_fetch_currency_rates():
    with patch("src.views.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.85}}
        mock_get.return_value = mock_response

        result = fetch_currency_rates(["USD", "EUR"])
        assert result == {"USD": 1.0, "EUR": 0.85}


def test_fetch_stock_prices():
    with patch("src.views.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = fetch_stock_prices(["AAPL"])
        assert result == {"AAPL": "N/A"}


@patch("src.views.pd.read_excel")
def test_process_operations_data_valid(mock_read_excel):
    df_mock = pd.DataFrame(
        {
            "Номер карты": ["1234", "5678"],
            "Сумма": [100, 200],
            "Кешбэк": [1, 2],
            "Дата операции": ["2024-01-01", "2024-01-02"],
        }
    )
    mock_read_excel.return_value = df_mock

    result = process_operations_data("fake_path.xlsx", "2024-01-01", "2024-01-02")
    assert isinstance(result, dict)
    assert len(result["card_data"]) == 2
    assert len(result["top_transactions"]) == 2

import json
import os
import pytest
from datetime import datetime, timedelta
import pandas as pd
from unittest.mock import patch, mock_open
from src.utils import (
    get_date_range,
    filtered_operations,
    greetings,
    info_about_operations,
    top5_tran,
    currency_rates,
    sorted_by_month
)

def test_get_date_range():
    date_str = "2023-10-15 12:00:00"
    start_date, end_date = get_date_range(date_str)
    assert start_date == "01.10.2023"
    assert end_date == "15.10.2023"

    with pytest.raises(ValueError):
        get_date_range("invalid_date")

def test_filtered_operations():
    operations = [
        {"Дата операции": "01.10.2023"},
        {"Дата операции": "15.10.2023"},
        {"Дата операции": "20.10.2023"}
    ]
    with patch("src.utils.operations_df", operations):
        filtered_ops = filtered_operations("2023-10-15 12:00:00")
        assert len(filtered_ops) == 2

def test_greetings():
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 8
        assert greetings() == "Доброе утро"

        mock_datetime.now.return_value.hour = 14
        assert greetings() == "Добрый день"

        mock_datetime.now.return_value.hour = 20
        assert greetings() == "Добрый вечер"

        mock_datetime.now.return_value.hour = 23
        assert greetings() == "Доброй ночи"

def test_info_about_operations():
    operations = [
        {"Номер карты": "1234", "Сумма операции с округлением": 100, "Кэшбэк": 1},
        {"Номер карты": "5678", "Сумма операции с округлением": 200, "Кэшбэк": 2}
    ]
    cards, amounts, cashbacks = info_about_operations(operations)
    assert cards == ["1234", "5678"]
    assert amounts == [100, 200]
    assert cashbacks == [1, 2]

def test_top5_tran():
    operations = [
        {"Сумма операции с округлением": 100},
        {"Сумма операции с округлением": 200},
        {"Сумма операции с округлением": 300},
        {"Сумма операции с округлением": 400},
        {"Сумма операции с округлением": 500},
        {"Сумма операции с округлением": 600}
    ]
    top5 = top5_tran(operations)
    assert len(top5) == 5
    assert top5[0]["Сумма операции с округлением"] == 600

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"user_currencies": ["USD"], "user_stocks": ["AAPL"]}))
@patch("requests.get")
def test_currency_rates(mock_get, mock_file):
    mock_get.return_value.json.return_value = {
        "quotes": {"USDRUB": 75.5}
    }

    currency_info, stocks_info = currency_rates("fake_path.json")
    assert len(currency_info) == 1
    assert currency_info[0]["currency"] == "USD"
    assert currency_info[0]["rate"] == 75.5



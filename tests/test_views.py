from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import (analyze_data, fetch_data_from_api, load_operations_data,
                       parse_datetime)


def test_parse_datetime_valid():
    date_str = "2024-01-01 12:00:00"
    result = parse_datetime(date_str)
    assert isinstance(result, datetime)
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 1


def test_parse_datetime_invalid():
    with pytest.raises(ValueError):
        parse_datetime("invalid-date")


def test_fetch_data_from_api():
    test_date = datetime(2024, 1, 1)
    result = fetch_data_from_api(test_date)
    assert isinstance(result, list)
    assert all('value' in record and 'date' in record for record in result)


def test_analyze_data_valid():
    raw_data = [
        {"value": 100, "date": "2024-01-01"},
        {"value": 200, "date": "2024-01-01"}
    ]
    result = analyze_data(raw_data)
    assert result["average_value"] == 150
    assert result["records_count"] == 2


def test_analyze_data_missing_value_column():
    raw_data = [
        {"amount": 100, "date": "2024-01-01"}
    ]
    result = analyze_data(raw_data)
    assert result["average_value"] is None
    assert result["records_count"] == 1


@patch('src.views.pd.read_excel')
def test_load_operations_data_valid(mock_read_excel):
    df_mock = pd.DataFrame({
        "Дата операции": ["2024-01-01", "2024-01-02"]
    })
    mock_read_excel.return_value = df_mock

    result = load_operations_data("fake_path.xlsx")
    assert isinstance(result, pd.DataFrame)
    assert "Дата операции" in result.columns


@patch('src.views.pd.read_excel')
def test_load_operations_data_missing_column(mock_read_excel):
    df_mock = pd.DataFrame({
        "Другой столбец": ["2024-01-01"]
    })
    mock_read_excel.return_value = df_mock

    with pytest.raises(ValueError):
        load_operations_data("fake_path.xlsx")
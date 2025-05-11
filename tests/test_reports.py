import json

import pandas as pd

from src.reports import get_expenses_by_weekday


def test_get_expenses_by_weekday_success():
    data = pd.DataFrame({
        'Дата операции': ['2024-04-01', '2024-04-02', '2024-04-03', '2024-04-04', '2024-04-05'],
        'Сумма': [200, 150, 300, 250, 100]
    })

    expected_result = {
        "results_count": 5,
        "results": [
            {"День недели": "Monday", "Сумма": 200},
            {"День недели": "Tuesday", "Сумма": 150},
            {"День недели": "Wednesday", "Сумма": 300},
            {"День недели": "Thursday", "Сумма": 250},
            {"День недели": "Friday", "Сумма": 100}
        ]
    }

    result_json = get_expenses_by_weekday(data)
    result = json.loads(result_json)

    assert result == expected_result


def test_get_expenses_by_weekday_empty_dataframe():
    data = pd.DataFrame({
        'Дата операции': [],
        'Сумма': []
    })

    result_json = get_expenses_by_weekday(data)
    result = json.loads(result_json)

    expected_result = {"error": "Передан пустой DataFrame"}

    assert result == expected_result


def test_get_expenses_by_weekday_no_date():
    data = pd.DataFrame({
        'Дата операции': ['2024-04-01', '2024-04-02', '2024-04-03', '2024-04-04', '2024-04-05'],
        'Сумма': [200, 150, 300, 250, 100]
    })
    result_json = get_expenses_by_weekday(data)
    result = json.loads(result_json)
    assert result is not None
    assert 'results_count' in result
    assert 'results' in result


def test_get_expenses_by_weekday_with_date_filter():
    data = pd.DataFrame({
        'Дата операции': ['2024-04-01', '2024-04-02', '2024-04-03', '2024-04-04', '2024-04-05'],
        'Сумма': [200, 150, 300, 250, 100]
    })

    filter_date = '2024-04-03'

    expected_result = {
        "results_count": 3,
        "results": [
            {"День недели": "Monday", "Сумма": 200},
            {"День недели": "Tuesday", "Сумма": 150},
            {"День недели": "Wednesday", "Сумма": 300}
        ]
    }

    result_json = get_expenses_by_weekday(data, date=filter_date)
    result = json.loads(result_json)

    assert result == expected_result


def test_get_expenses_by_weekday_error():
    data = pd.DataFrame({
        'Дата операции': ['invalid_date', 'another_invalid_date'],
        'Сумма': [200, 150]
    })

    result_json = get_expenses_by_weekday(data)
    result = json.loads(result_json)

    assert 'error' in result
    assert "Invalid comparison between dtype=datetime64[ns] and date" in result['error']
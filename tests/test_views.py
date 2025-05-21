import json
import os
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
import pandas as pd  # Добавлен импорт pandas
from src.views import (
    get_greeting,
    load_user_settings,
    fetch_currency_rates,
    fetch_stock_prices,
    process_operations_data,
    home_page_function
)

# Тест для функции get_greeting
def test_get_greeting():
    with patch('src.views.datetime') as mock_datetime:
        # Устанавливаем фиктивное время для тестирования
        mock_datetime.now.return_value.hour = 8
        assert get_greeting() == "Доброе утро"

        mock_datetime.now.return_value.hour = 14
        assert get_greeting() == "Добрый день"

        mock_datetime.now.return_value.hour = 20
        assert get_greeting() == "Добрый вечер"

        mock_datetime.now.return_value.hour = 2
        assert get_greeting() == "Доброй ночи"

# Тест для функции load_user_settings
def test_load_user_settings(tmp_path):
    # Создаем временный файл для тестирования
    settings = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}
    settings_path = tmp_path / "user_settings.json"
    with open(settings_path, "w") as f:
        json.dump(settings, f)

    # Проверяем загрузку настроек
    result = load_user_settings(settings_path)
    assert result == settings

    # Проверяем ошибку при отсутствии файла
    with pytest.raises(FileNotFoundError):
        load_user_settings("nonexistent_file.json")

# Тест для функции fetch_currency_rates
@patch('requests.get')
def test_fetch_currency_rates(mock_get):
    # Создаем фиктивный ответ от API
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"USD": 1.0, "EUR": 0.85}}
    mock_get.return_value = mock_response

    # Проверяем получение курсов валют
    result = fetch_currency_rates(["USD", "EUR"])
    assert result == [{"currency": "USD", "rate": 1.0}, {"currency": "EUR", "rate": 0.85}]

# Тест для функции fetch_stock_prices
@patch('requests.get')
def test_fetch_stock_prices(mock_get):
    # Создаем фиктивный ответ от API
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Проверяем получение цен на акции
    result = fetch_stock_prices(["AAPL", "AMZN"])
    assert result == [{"stock": "AAPL", "price": "N/A"}, {"stock": "AMZN", "price": "N/A"}]

# Тест для функции process_operations_data
def test_process_operations_data(tmp_path):
    # Создаем временный файл для тестирования
    data = {
        "Дата операции": ["2025-04-01", "2025-04-02"],
        "Номер карты": ["1234567890123456", "1234567890123456"],
        "Сумма": [100, 200],
        "Кешбэк": [1, 2],
        "Категория": ["Категория1", "Категория2"],
        "Описание": ["Описание1", "Описание2"]
    }
    df = pd.DataFrame(data)
    operations_path = tmp_path / "operations.xlsx"
    df.to_excel(operations_path, index=False)

    # Проверяем обработку данных операций
    result = process_operations_data(operations_path, "2025-04-01", "2025-04-02")
    assert len(result["card_data"]) == 1
    assert len(result["top_transactions"]) == 2

# Тест для функции home_page_function
@patch('src.views.datetime')
@patch('src.views.load_user_settings')
@patch('src.views.fetch_currency_rates')
@patch('src.views.fetch_stock_prices')
@patch('src.views.process_operations_data')
def test_home_page_function(mock_process_operations_data, mock_fetch_stock_prices, mock_fetch_currency_rates, mock_load_user_settings, mock_datetime):
    # Устанавливаем фиктивные данные для тестирования
    mock_datetime.strptime.return_value = datetime(2025, 4, 9, 14, 30)
    mock_datetime.now.return_value = datetime(2025, 5, 20, 12, 0)

    mock_load_user_settings.return_value = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}
    mock_fetch_currency_rates.return_value = [{"currency": "USD", "rate": 1.0}, {"currency": "EUR", "rate": 0.85}]
    mock_fetch_stock_prices.return_value = [{"stock": "AAPL", "price": "N/A"}, {"stock": "AMZN", "price": "N/A"}]
    mock_process_operations_data.return_value = {
        "card_data": [{"Номер карты": "1234567890123456", "Сумма": 100, "Кешбэк": 1}],
        "top_transactions": [
            {"Дата операции": datetime(2025, 4, 1), "Сумма": 100, "Категория": "Категория1", "Описание": "Описание1"},
            {"Дата операции": datetime(2025, 4, 2), "Сумма": 200, "Категория": "Категория2", "Описание": "Описание2"}
        ]
    }

    # Проверяем основную функцию
    result = home_page_function("2025-04-09 14:30:00")
    data = json.loads(result)
    assert data["status"] == "success"
    assert data["data"]["greeting"] == "Добрый день"
    assert len(data["data"]["cards"]) == 1
    assert len(data["data"]["top_transactions"]) == 2
    assert len(data["data"]["currency_rates"]) == 2
    assert len(data["data"]["stock_prices"]) == 2

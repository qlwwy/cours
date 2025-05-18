import json
import logging
from datetime import datetime, timedelta

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_greeting():
    """Возвращает приветствие в зависимости от текущего времени."""
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_user_settings(file_path: str) -> dict:
    """Загружает пользовательские настройки из файла."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as err:
        logger.error(f"Ошибка при загрузке пользовательских настроек: {err}")
        raise


def fetch_currency_rates(currencies: list) -> dict:
    """Получает курсы валют из внешнего API."""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        response.raise_for_status()
        data = response.json()
        return {currency: data["rates"].get(currency, "N/A") for currency in currencies}
    except Exception as err:
        logger.error(f"Ошибка при получении курсов валют: {err}")
        raise


def fetch_stock_prices(stocks: list) -> dict:
    """Получает цены на акции из внешнего API."""
    try:
        stock_prices = {}
        for stock in stocks:
            response = requests.get(f"https://finance.yahoo.com/quote/{stock}")
            response.raise_for_status()
            # Здесь нужно добавить парсинг HTML для получения цены акции
            stock_prices[stock] = "N/A"  # Замените на реальное значение
        return stock_prices
    except Exception as err:
        logger.error(f"Ошибка при получении цен на акции: {err}")
        raise


def process_operations_data(file_path: str, start_date: str, end_date: str) -> dict:
    """Обрабатывает данные из файла операций."""
    try:
        df = pd.read_excel(file_path)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])
        mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
        filtered_df = df.loc[mask]

        # Группировка по картам
        card_data = (
            filtered_df.groupby("Номер карты")
            .agg({"Сумма": "sum", "Кешбэк": "sum"})
            .reset_index()
        )

        # Топ-5 транзакций по сумме платежа
        top_transactions = filtered_df.nlargest(5, "Сумма")

        return {
            "card_data": card_data.to_dict(orient="records"),
            "top_transactions": top_transactions.to_dict(orient="records"),
        }
    except Exception as err:
        logger.error(f"Ошибка при обработке данных операций: {err}")
        raise


def home_page_function(datetime_str: str) -> str:
    """Основная функция для страницы «Главная»"""
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        start_date = dt.replace(day=1).strftime("%Y-%m-%d")
        end_date = dt.strftime("%Y-%m-%d")

        user_settings = load_user_settings("user_settings.json")
        currency_rates = fetch_currency_rates(user_settings["user_currencies"])
        stock_prices = fetch_stock_prices(user_settings["user_stocks"])
        operations_data = process_operations_data(
            "data/operations.xlsx", start_date, end_date
        )

        response = {
            "status": "success",
            "data": {
                "greeting": get_greeting(),
                "card_data": operations_data["card_data"],
                "top_transactions": operations_data["top_transactions"],
                "currency_rates": currency_rates,
                "stock_prices": stock_prices,
            },
            "timestamp": datetime.now().isoformat(),
        }

        return json.dumps(response, ensure_ascii=False, indent=2)

    except Exception as e:
        error_response = {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat(),
        }
        return json.dumps(error_response, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    test_datetime = "2025-04-09 14:30:00"
    result = home_page_function(test_datetime)
    print(result)

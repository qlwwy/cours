import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
API_KEY_CUR_USD = os.getenv("API_KEY_CUR_USD")
API_KEY_POS = os.getenv("API_KEY_STOCK")

try:
    df = pd.read_excel("data/operations.xlsx")
    operations_df = df.to_dict(orient="records")
    logger.info("Файл успешно загружен.")
except Exception as e:
    logger.error(f"Ошибка загрузки файла Excel: {e}")
    operations_df = []


def get_date_range(date: str) -> Tuple[str, str]:
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        start_of_month = date_obj.replace(day=1)
        return start_of_month.strftime("%d.%m.%Y"), date_obj.strftime("%d.%m.%Y")
    except ValueError as e:
        logger.error(f"Ошибка при разборе даты: {e}")
        raise


def filtered_operations(time: str) -> List[Dict]:
    try:
        start_date_str, end_date_str = get_date_range(time)
        start_date = pd.to_datetime(start_date_str, dayfirst=True)
        end_date = pd.to_datetime(end_date_str, dayfirst=True)

        filtered_op = [
            op for op in operations_df
            if start_date <= pd.to_datetime(op["Дата операции"], dayfirst=True) <= end_date
        ]
        logger.info(f"Отфильтровано операций: {len(filtered_op)}")
        return filtered_op
    except Exception as e:
        logger.error(f"Ошибка фильтрации операций: {e}")
        return []


def greetings() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def info_about_operations(operations: List[Dict]) -> Tuple[List, List, List]:
    cards, amounts, cashbacks = [], [], []
    for op in operations:
        cards.append(op.get("Номер карты", "Неизвестно"))
        amounts.append(op.get("Сумма операции с округлением", 0))
        cashbacks.append(op.get("Кэшбэк", 0))
    return cards, amounts, cashbacks


def top5_tran(operations: List[Dict]) -> List[Dict]:
    try:
        sorted_ops = sorted(
            operations,
            key=lambda x: x.get("Сумма операции с округлением", 0),
            reverse=True
        )
        return sorted_ops[:5]
    except Exception as e:
        logger.error(f"Ошибка при сортировке транзакций: {e}")
        return []


def currency_rates(user_settings_path: str) -> Tuple[List[Dict], List[Dict]]:
    currency_info, stocks_info = [], []

    try:
        with open(user_settings_path, encoding="utf-8") as f:
            settings = json.load(f)

        # Курсы валют
        currencies = ",".join(settings.get("user_currencies", []))
        currency_url = f"http://api.currencylayer.com/live?access_key={API_KEY_CUR_USD}&currencies={currencies}"
        resp_cur = requests.get(currency_url).json()

        for currency in settings.get("user_currencies", []):
            key = f"{currency}RUB"
            rate = resp_cur.get("quotes", {}).get(key)
            if rate:
                currency_info.append({"currency": currency, "rate": round(rate, 2)})

        stocks = ",".join(settings.get("user_stocks", []))
        stocks_url = f"http://api.marketstack.com/v1/eod/latest?access_key={API_KEY_POS}&symbols={stocks}"
        resp_stocks = requests.get(stocks_url).json()

        for stock in resp_stocks.get("data", []):
            stocks_info.append({"stock": stock["symbol"], "price": float(stock["close"])})

        return currency_info, stocks_info

    except Exception as e:
        logger.error(f"Ошибка получения данных с API: {e}")
        return [], []


def sorted_by_month(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    try:
        if date is None:
            date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        start_date = end_date - timedelta(days=90)

        transactions["Дата платежа"] = pd.to_datetime(
            transactions["Дата платежа"], errors="coerce", dayfirst=True
        )

        filtered_df = transactions[
            (transactions["Дата платежа"] >= start_date) &
            (transactions["Дата платежа"] <= end_date)
        ]
        return filtered_df

    except Exception as e:
        logger.error(f"Ошибка фильтрации по месяцу: {e}")
        return pd.DataFrame()
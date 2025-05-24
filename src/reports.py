
from typing import List
import pandas as pd
from datetime import datetime


def spending_by_category(transactions: pd.DataFrame, category: str, date_str: str) -> pd.DataFrame:
    if transactions.empty:
        return pd.DataFrame()

    expected_columns = {"Дата операции", "Категория", "Сумма платежа"}
    if not expected_columns.issubset(transactions.columns):
        return pd.DataFrame()

    transactions = transactions.copy()
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    transactions = transactions[transactions["Дата операции"].notna()]

    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        start_date = date_obj.replace(day=1)
    except ValueError:
        return pd.DataFrame()

    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= date_obj) &
        (transactions["Категория"] == category)
    ]

    return filtered_transactions
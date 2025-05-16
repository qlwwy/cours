import json
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Optional

import pandas as pd


def save_report(file_name: Optional[str] = None):
    """
    Декоратор для сохранения результата функции в JSON-файл.
    Если имя файла не указано — формируется автоматически.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> str:
            result: str = func(*args, **kwargs)

            nonlocal file_name
            if file_name is None:
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"report_{func.__name__}_{now}.json"

            try:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(result)
                print(f"Отчет сохранен в файл: {file_name}")
            except Exception as e:
                print(f"Ошибка при сохранении отчета: {e}")

            return result
        return wrapper

    # Поддержка вызова как без скобок, так и с параметром
    if callable(file_name):
        return decorator(file_name)
    return decorator


@save_report  # Или можно @save_report("my_custom_report.json")
def get_expenses_by_category(df: pd.DataFrame, category: str, start_date: str) -> str:
    """Функция для получения отчета о тратах по категории за трехмесячный период."""
    try:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = start_date_dt + timedelta(days=90)
        df["date"] = pd.to_datetime(df["date"])

        filtered_df = df[
            (df["category"] == category) &
            (df["date"] >= start_date_dt) &
            (df["date"] <= end_date)
        ]

        if filtered_df.empty:
            return json.dumps({"error": "Нет данных для выбранной категории и периода."}, ensure_ascii=False, indent=4)

        category_expenses = filtered_df.groupby("category")["amount"].sum().reset_index()
        result = category_expenses.to_dict(orient="records")

        return json.dumps(result, ensure_ascii=False, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    raw_data = {
        "date": ["2025-01-15", "2025-02-20", "2025-03-10", "2025-03-25", "2025-04-05"],
        "category": ["Food", "Food", "Transport", "Food", "Food"],
        "amount": [100, 200, 50, 150, 100],
    }

    df = pd.DataFrame(raw_data)

    start_date = "2025-01-01"
    category = "Food"
    result = get_expenses_by_category(df, category, start_date)

    print(result)
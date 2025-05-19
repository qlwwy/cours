import json
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Optional
import os

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

            # Проверяем, является ли результат ошибкой
            result_dict = json.loads(result)
            if "error" in result_dict:
                print(f"Ошибка: {result_dict['error']}")
                return result

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

@save_report
def get_expenses_by_day_of_week(file_path: str, start_date: str) -> str:
    """Функция для получения отчета о тратах по дням недели за трехмесячный период."""
    try:
        # Используем абсолютный путь к файлу
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        operations_data_path = os.path.join(base_dir, "data", "operations.xlsx")

        df = pd.read_excel(operations_data_path)

        # Проверяем наличие столбца с датами
        if 'date' not in df.columns:
            # Если столбец называется по-другому, например, 'Дата операции'
            if 'Дата операции' in df.columns:
                df['date'] = df['Дата операции']
            else:
                return json.dumps(
                    {"error": "Столбец с датами не найден."},
                    ensure_ascii=False,
                    indent=4,
                )

        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = start_date_dt + timedelta(days=90)
        df["date"] = pd.to_datetime(df["date"])

        filtered_df = df[(df["date"] >= start_date_dt) & (df["date"] <= end_date)]

        if filtered_df.empty:
            return json.dumps(
                {"error": "Нет данных для выбранного периода."},
                ensure_ascii=False,
                indent=4,
            )

        # Группировка по дням недели
        filtered_df["day_of_week"] = filtered_df["date"].dt.day_name()
        day_of_week_expenses = (
            filtered_df.groupby("day_of_week")["amount"].sum().reset_index()
        )
        result = day_of_week_expenses.to_dict(orient="records")

        return json.dumps(result, ensure_ascii=False, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    start_date = "2025-01-01"
    result = get_expenses_by_day_of_week("data/operations.xlsx", start_date)

    print(result)

import json
import logging
from datetime import datetime

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_expenses_by_weekday(data: pd.DataFrame, date: str = None) -> str:
    """Функция для расчета трат по дням недели."""
    try:
        if data.empty:
            logger.warning("Передан пустой DataFrame.")
            return json.dumps({"error": "Передан пустой DataFrame"}, ensure_ascii=False)
        data['Дата операции'] = pd.to_datetime(data['Дата операции'], errors='coerce')

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        data = data[data['Дата операции'].dt.date <= pd.to_datetime(date).date()]
        data['День недели'] = data['Дата операции'].dt.day_name()
        expenses_by_weekday = data.groupby('День недели')['Сумма'].sum().reset_index()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        expenses_by_weekday['День недели'] = pd.Categorical(expenses_by_weekday['День недели'], categories=days_of_week, ordered=True)
        expenses_by_weekday = expenses_by_weekday.sort_values('День недели')
        result = expenses_by_weekday.to_dict(orient="records")
        logger.info(f"Отчет 'Траты по дням недели' успешно сгенерирован для даты: {date}")
        return json.dumps({"results_count": len(result), "results": result}, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Ошибка при генерации отчета 'Траты по дням недели': {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


data = pd.DataFrame({
    'Дата операции': ['2024-04-01', '2024-04-02', '2024-04-03', '2024-04-04', '2024-04-05'],
    'Сумма': [200, 150, 300, 250, 100]
})


result_json = get_expenses_by_weekday(data)
print(result_json)
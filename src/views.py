import logging
from datetime import datetime

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_datetime(date_str: str) -> datetime:
    """Преобразует строку с датой и временем в объект datetime."""
    try:
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        logger.info(f"Успешный парсинг: {parsed_date}")
        return parsed_date
    except ValueError as err:
        logger.error(f"Ошибка парсинга даты: {err}")
        raise


def fetch_data_from_api(date: datetime) -> list[dict]:
    """Получает данные с внешнего API по дате (заглушка)."""
    try:
        logger.info(f"Запрос данных с API для даты: {date.date()}")
        return [
            {"value": 100, "date": str(date.date())},
            {"value": 150, "date": str(date.date())},
            {"value": 200, "date": str(date.date())}
        ]
    except Exception as err:
        logger.error(f"Ошибка при запросе к API: {err}")
        raise


def analyze_data(raw_data: list[dict]) -> dict:
    """Обрабатывает данные с использованием pandas и возвращает статистику."""
    try:
        df = pd.DataFrame(raw_data)
        logger.info("Данные успешно преобразованы в DataFrame")

        if 'value' not in df.columns:
            logger.warning("Колонка 'value' не найдена")
            average = None
        else:
            average = df['value'].mean()

        return {
            "average_value": average,
            "records_count": len(df)
        }
    except Exception as err:
        logger.error(f"Ошибка при анализе данных: {err}")
        raise


def load_operations_data(file_path: str) -> pd.DataFrame:
    """Загружает данные из Excel-файла."""
    try:
        logger.info(f"Загрузка данных из файла: {file_path}")
        df = pd.read_excel(file_path)

        if 'Дата операции' not in df.columns:
            error_msg = "Не найдена колонка 'Дата операции' в файле."
            logger.error(error_msg)
            raise ValueError(error_msg)

        return df
    except Exception as err:
        logger.error(f"Ошибка при загрузке данных из файла: {err}")
        raise


if __name__ == "__main__":
    try:
        operations_df = load_operations_data("../data/operations.xlsx")
        print(operations_df)
    except Exception as e:
        logger.error(f"Не удалось загрузить данные: {e}")
import logging
from datetime import datetime
import pandas as pd


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_datetime(date_str: str) -> datetime:
    """Преобразует строку даты и времени в объект datetime."""
    try:
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        logger.info(f"Дата успешно распознана: {parsed_date}")
        return parsed_date
    except ValueError as error:
        logger.error(f"Ошибка при разборе даты: {error}")
        raise


def fetch_data_from_api(date: datetime) -> list[dict]:
    """Имитация получения данных с API на заданную дату."""
    try:
        logger.info(f"Получение данных с API на дату: {date.date()}")
        mock_data = [
            {"value": 100, "date": str(date.date())},
            {"value": 150, "date": str(date.date())},
            {"value": 200, "date": str(date.date())},
        ]
        return mock_data
    except Exception as error:
        logger.error(f"Ошибка API-запроса: {error}")
        raise


def analyze_data(data: list[dict]) -> dict:
    """Анализирует данные, рассчитывая среднее значение и количество записей."""
    try:
        df = pd.DataFrame(data)
        logger.info("Данные успешно преобразованы в DataFrame")

        if 'value' in df.columns:
            average = df['value'].mean()
        else:
            average = None
            logger.warning("Колонка 'value' отсутствует в данных")

        return {
            "average_value": average,
            "records_count": len(df)
        }
    except Exception as error:
        logger.error(f"Ошибка анализа данных: {error}")
        raise


def load_operations_data(filepath: str) -> pd.DataFrame:
    """Загружает данные из Excel-файла и возвращает DataFrame."""
    try:
        logger.info(f"Чтение Excel-файла: {filepath}")
        df = pd.read_excel(filepath)

        if 'Дата операции' not in df.columns:
            logger.error("Колонка 'Дата операции' не найдена в Excel-файле")
            raise ValueError("Ожидаемая колонка 'Дата операции' отсутствует")

        return df
    except Exception as error:
        logger.error(f"Ошибка загрузки данных: {error}")
        raise


if __name__ == "__main__":
    operations_df = load_operations_data("../data/operations.xlsx")
    print(operations_df)
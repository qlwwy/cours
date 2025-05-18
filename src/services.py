import json
import logging
from typing import Any

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_operations_data(file_path: str) -> pd.DataFrame:
    """Загружает данные из Excel-файла и возвращает DataFrame."""
    logger.info(f"Загрузка данных из файла: {file_path}")
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            raise ValueError("Файл пустой или не содержит данных.")
        logger.info(f"Успешная загрузка. Всего записей: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {e}")
        raise


def simple_search(query: str, file_path: str) -> str:
    """Выполняет простой поиск по всем полям файла на соответствие текстовому запросу."""
    logger.info(f"Поисковый запрос: {query}")
    try:
        query_lower = query.strip().lower()
        df = load_operations_data(file_path)

        matched = df[
            df.apply(
                lambda row: row.astype(str)
                .str.contains(query_lower, case=False, na=False)
                .any(),
                axis=1,
            )
        ]

        logger.info(f"Найдено совпадений: {len(matched)}")

        response: dict[str, Any] = {
            "query": query,
            "results_count": len(matched),
            "results": matched.to_dict(orient="records"),
        }

        return json.dumps(response, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Ошибка при поиске: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == "__main__":
    user_query = input("Введите запрос для поиска: ").title()
    result = simple_search(user_query, "../data/operations.xlsx")
    print(result)

import json
from datetime import datetime
import pandas as pd

from src.utils import analyze_data, fetch_data_from_api, load_operations_data, parse_datetime


def home_page_function(datetime_str: str) -> str:
    """Основная функция для страницы «Главная»"""
    try:
        dt = parse_datetime(datetime_str)
        api_data = fetch_data_from_api(dt)
        processed_data = analyze_data(api_data)
        operations_data = pd.read_excel("data/operations.xlsx")

        response = {
            "status": "success",
            "data": {
                "api_data": api_data,
                "processed_data": processed_data,
                "operations_data": operations_data.to_dict(orient='records')
            },
            "timestamp": datetime.now().isoformat()
        }

        return json.dumps(response, ensure_ascii=False, indent=2)

    except Exception as e:
        error_response = {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(error_response, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    test_datetime = "2025-04-09 14:30:00"
    result = home_page_function(test_datetime)
    print(result)
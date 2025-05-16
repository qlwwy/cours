import json
import unittest

import pandas as pd

from src.reports import get_expenses_by_category


class TestGetExpensesByCategory(unittest.TestCase):

    def setUp(self):
        """Настройка данных для тестов"""
        data = {
            "date": ["2025-01-15", "2025-02-20", "2025-03-10", "2025-03-25", "2025-04-05"],
            "category": ["Food", "Food", "Transport", "Food", "Food"],
            "amount": [100, 200, 50, 150, 100],
        }
        self.df = pd.DataFrame(data)

    def test_expenses_by_category(self):
        """Тест с обычными данными"""
        start_date = "2025-01-01"
        category = "Food"
        result = get_expenses_by_category(self.df, category, start_date)

        expected_result = [{"category": "Food", "amount": 450}]

        self.assertEqual(json.loads(result), expected_result)

    def test_no_data_for_category(self):
        """Тест, когда нет данных по категории"""
        start_date = "2025-01-01"
        category = "Transport"
        result = get_expenses_by_category(self.df, category, start_date)

        expected_result = [{"category": "Transport", "amount": 50}]

        self.assertEqual(json.loads(result), expected_result)

    def test_no_data_for_date_range(self):
        """Тест, когда нет данных по датам"""
        start_date = "2024-01-01"
        category = "Food"
        result = get_expenses_by_category(self.df, category, start_date)

        expected_result = {"error": "Нет данных для выбранной категории и периода."}

        self.assertEqual(json.loads(result), expected_result)

    def test_empty_dataframe(self):
        """Тест с пустым DataFrame"""
        empty_df = pd.DataFrame(columns=["date", "category", "amount"])
        start_date = "2025-01-01"
        category = "Food"
        result = get_expenses_by_category(empty_df, category, start_date)

        expected_result = {"error": "Нет данных для выбранной категории и периода."}

        self.assertEqual(json.loads(result), expected_result)

    def test_invalid_date_format(self):
        """Тест с ошибкой в формате даты"""
        start_date = "2025/01/01"
        category = "Food"
        result = get_expenses_by_category(self.df, category, start_date)
        self.assertIn("time data", json.loads(result)["error"])


if __name__ == "__main__":
    unittest.main()
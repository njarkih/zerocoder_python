import unittest
from unittest.mock import patch
from io import StringIO

# Импортируем функции из исходного кода
from task2 import get_age_suffix, main


class TestAgeSuffix(unittest.TestCase):
    def test_get_age_suffix(self):
        # Проверяем правильное склонение слова "год"
        self.assertEqual(get_age_suffix(1), "год")
        self.assertEqual(get_age_suffix(2), "года")
        self.assertEqual(get_age_suffix(4), "года")
        self.assertEqual(get_age_suffix(5), "лет")
        self.assertEqual(get_age_suffix(11), "лет")
        self.assertEqual(get_age_suffix(21), "год")
        self.assertEqual(get_age_suffix(22), "года")
        self.assertEqual(get_age_suffix(23), "года")
        self.assertEqual(get_age_suffix(24), "года")
        self.assertEqual(get_age_suffix(25), "лет")


class TestMainFunction(unittest.TestCase):
    @patch('builtins.input', side_effect=['Алексей', '25'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_output(self, mock_stdout, mock_input):
        # Тестируем вывод программы для возраста 25 лет
        main()
        expected_output = (
            'Привет, Алексей! Тебе 25 лет, это 300 месяцев, 9000 дней, 216000 часов.\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['Мария', '1'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_output_single_year(self, mock_stdout, mock_input):
        # Тестируем вывод программы для возраста 1 год
        main()
        expected_output = (
            'Привет, Мария! Тебе 1 год, это 12 месяцев, 360 дней, 8640 часов.\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
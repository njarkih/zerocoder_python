import unittest
from unittest.mock import patch, Mock
from io import StringIO

# Импортируем функции из исходного кода
from task5 import get_exchange_rate, convert_currency, convert_fixed_price, main


class TestCurrencyConverter(unittest.TestCase):

    @patch('task5.requests.get')
    def test_get_exchange_rate(self, mock_get):
        # Мокаем ответ от requests.get
        mock_response = Mock()
        mock_response.json.return_value = {
            "rates": {
                "USD": 1.1,
                "EUR": 0.9
            }
        }
        mock_get.return_value = mock_response

        # Проверяем правильность получения обменного курса
        self.assertEqual(get_exchange_rate("USD", "EUR"), 0.9)
        self.assertEqual(get_exchange_rate("USD", "USD"), 1.1)

    def test_convert_currency(self):
        # Мокаем get_exchange_rate для тестирования convert_currency
        with patch('task5.get_exchange_rate', return_value=0.9):
            converted_amount, exchange_rate = convert_currency(100, "USD", "EUR")
            self.assertAlmostEqual(converted_amount, 90.0)
            self.assertEqual(exchange_rate, 0.9)

    def test_convert_fixed_price(self):
        # Проверяем конвертацию с фиксированным курсом
        result = convert_fixed_price(100, "USD", "EUR", 0.9)
        self.assertAlmostEqual(result, 90.0)

    @patch('builtins.input', side_effect=['USD', 'EUR', '100'])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('task5.convert_currency', return_value=(90.0, 0.9))
    @patch('task5.convert_fixed_price', return_value=100.0)
    def test_main_output(self, mock_convert_fixed_price, mock_convert_currency, mock_stdout, mock_input):
        # Тестируем вывод программы
        main()
        output = mock_stdout.getvalue().strip()
        expected_output = (
            "Сумма в валюте EUR: 100.00 EUR по фиксированному курсу 100.0\n"
            "Сумма в валюте EUR: 90.00 EUR по реальному курсу 0.9"
        )
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()

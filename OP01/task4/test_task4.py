import unittest
from unittest.mock import patch
from io import StringIO

# Импортируем функции из исходного кода
from task4 import calculate_area, main

class TestCalculateArea(unittest.TestCase):
    def test_calculate_area(self):
        # Проверяем правильность вычисления площади прямоугольника
        self.assertAlmostEqual(calculate_area(5, 10), 50.0)
        self.assertAlmostEqual(calculate_area(3.5, 4.2), 14.7)
        self.assertAlmostEqual(calculate_area(0, 10), 0.0)
        self.assertAlmostEqual(calculate_area(7.1, 8.4), 59.64)
        self.assertAlmostEqual(calculate_area(10, 10), 100.0)

class TestMainFunction(unittest.TestCase):
    @patch('builtins.input', side_effect=['5', '10'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_output(self, mock_stdout, mock_input):
        # Тестируем вывод программы для длины 5 и ширины 10
        main()
        expected_output = (
            'Площадь прямоугольника с длиной 5.0 и шириной 10.0 равна 50.0\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['3.5', '4.2'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_output_decimal(self, mock_stdout, mock_input):
        # Тестируем вывод программы для длины 3.5 и ширины 4.2
        main()
        expected_output = (
            'Площадь прямоугольника с длиной 3.5 и шириной 4.2 равна 14.7\n'
        )
        actual_output = mock_stdout.getvalue().strip()
        self.assertEqual(actual_output, expected_output)

    @patch('builtins.input', side_effect=['0', '10'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_output_zero_length(self, mock_stdout, mock_input):
        # Тестируем вывод программы для длины 0 и ширины 10
        main()
        expected_output = (
            'Площадь прямоугольника с длиной 0.0 и шириной 10.0 равна 0.0\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()

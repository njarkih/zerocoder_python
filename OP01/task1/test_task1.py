import unittest
from unittest.mock import patch
from io import StringIO

# Импортируем функцию zero_division_check из исходного кода
from task1 import zero_division_check, main


class TestCalculator(unittest.TestCase):

    def test_zero_division_check(self):
        """
        Тестирует функцию zero_division_check на правильность определения деления на ноль.

        Эта функция тестирует, возвращает ли функция zero_division_check True для входного значения 0
        и False для входных значений, отличных от 0, включая положительные и отрицательные числа.

        Проверка включает следующие случаи:
        - Нулевая проверка: Проверяет, что zero_division_check возвращает True, если входное значение равно 0.
        - Положительное число: Проверяет, что zero_division_check возвращает False для положительного числа (например, 5).
        - Отрицательное число: Проверяет, что zero_division_check возвращает False для отрицательного числа (например, -3).
        """
        self.assertTrue(zero_division_check(0))
        self.assertFalse(zero_division_check(5))
        self.assertFalse(zero_division_check(-3))


class TestInputOutput(unittest.TestCase):
    # Так как основная часть программы использует input() и print(), для тестирования
    # применим подмену стандартных потоков ввода и вывода с помощью библиотеки unittest
    # и модуля unittest.mock для эмуляции ввода и проверки вывода

    @patch('builtins.input', side_effect=['5', '0'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_division_by_zero(self, mock_stdout, mock_input):
        # Тестируем сценарий деления на 0
        main()
        expected_output = (
            'Сумма: 5.0\n'
            'Разность: 5.0\n'
            'Перемножение: 0.0\n'
            'Нельзя делить на 0! Операции деления, целочисленного деления и поиск остатка от деления недопустимы!\n'
            'Возведение в степень: 1.0\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['9', '3'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_operations(self, mock_stdout, mock_input):
        # Тестируем корректное выполнение всех операций
        main()
        expected_output = (
            'Сумма: 12.0\n'
            'Разность: 6.0\n'
            'Перемножение: 27.0\n'
            'Деление: 3.0\n'
            'Целочисленное деление: 3.0\n'
            'Остаток от деления: 0.0\n'
            'Возведение в степень: 729.0\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()

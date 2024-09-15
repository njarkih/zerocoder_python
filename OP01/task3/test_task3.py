import unittest
from unittest.mock import patch
from io import StringIO

from task3 import main


class TestMainFunction(unittest.TestCase):
    @patch('builtins.input', side_effect=['молоко', 'воз'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_output(self,mock_stdout, mock_input):
        # Тестируем вывод программы для слов 'молоко' и  'воз'
        main()
        expected_output = (
            'Конкатенация двух строк: молоковоз\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()

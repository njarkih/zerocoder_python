"""
Создать калькулятор — программу, в которой мы вводим 2 числа,
и с ними производятся сразу все математические действия: +, -, *, /, //, %, **
"""


def zero_division_check(number):
    """
    Проверяет, является ли переданное число нулем.

    Аргументы:
        number (float): Число, которое нужно проверить.

    Возвращает:
        bool: True, если число равно 0, иначе False.
    """
    return number == 0


def main():
    number1 = float(input("Введите первое число: "))
    number2 = float(input("Введите второе число: "))

    print(f'Сумма: {number1 + number2}')
    print(f'Разность: {number1 - number2}')
    print(f'Перемножение: {number1 * number2}')
    if zero_division_check(number2):
        print(f'Нельзя делить на 0! Операции деления, целочисленного деления и поиск остатка от деления недопустимы!')
    else:
        print(f'Деление: {number1 / number2}')
        print(f'Целочисленное деление: {number1 // number2}')
        print(f'Остаток от деления: {number1 % number2}')
    print(f'Возведение в степень: {number1 ** number2}')


if __name__ == "__main__":
    main()

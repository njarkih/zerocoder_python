"""
Написать конвертер валюты. Эта программа будет конвертировать введённую пользователем сумму в другую валюту. Курс валюты можно ввести самостоятельно и один раз.

Чтобы курс валюты был настоящий и самостоятельно обновлялся, также можно использовать ChatGPT.
"""

import requests


def get_exchange_rate(base_currency, target_currency):
    response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base_currency}")
    data = response.json()
    return data["rates"][target_currency]


def convert_currency(amount, base_currency, target_currency):
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    return amount * exchange_rate, exchange_rate


def convert_fixed_price(amount, base_currency, target_currency, fixed_exchange_rate):
    return amount * fixed_exchange_rate


def main():
    fixed_exchange_rate = 100.0
    base_currency = input("Введите основную валюту: ").upper()
    target_currency = input("Введите целевую валюту: ").upper()
    amount = float(input("Введите сумму в валюте {}: ".format(base_currency)))

    converted_amount = convert_fixed_price(amount, base_currency, target_currency, fixed_exchange_rate)
    print("Сумма в валюте {}: {:.2f} {} по фиксированному курсу {}".format(target_currency, converted_amount,
                                                                           target_currency, fixed_exchange_rate))

    converted_amount, exchange_rate = convert_currency(amount, base_currency, target_currency)
    print("Сумма в валюте {}: {:.2f} {} по реальному курсу {}".format(target_currency, converted_amount,
                                                                      target_currency, exchange_rate))


if __name__ == "__main__":
    main()


import requests
import json
from config import currency, right_forms


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f'Нельзя перевести {base} в {base}')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Неизвестная валюта - {base}')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Неизвестная валюта - {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество - {amount}\n')

        if amount <= 0:
            raise APIException(f'Не могу обработать количество валюты меньше или равное 0')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total = float(json.loads(r.content)[currency[quote]]) * float(amount)
        return total


class Words:
    @staticmethod
    def morph(word, qty):
        qty = int(float(qty))
        if qty < 10:
            if qty == 1:
                return right_forms[word][0]
            elif qty in [2, 3, 4]:
                return right_forms[word][1]
            else:
                return right_forms[word][2]
        else:
            if qty % 10 == 1 and qty % 100 != 11:
                return right_forms[word][0]
            elif qty % 10 in [2, 3, 4] and qty % 100 not in [12, 13, 14]:
                return right_forms[word][1]
            else:
                return right_forms[word][2]

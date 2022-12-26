import requests
import json
from config import valuta

class ConvertionException(Exception):
    pass

class ConvertionErrors:
    @staticmethod
    def converter(base:str, quote:str, amount:str):
        try:
            base_v = valuta[base.lower()]
        except KeyError:
            raise ConvertionException(f'Неверно введена валюта {base}') 
        try:
            quote_v = valuta[quote.lower()]
        except KeyError:
            raise ConvertionException(f'Неверно введена валюта {quote}')     
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Неверно введено количество переводимых средств {amount}') 
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_v}&tsyms={quote_v}')
        apivalue = json.loads(r.content)[valuta[quote]]*int(amount)

        return round(apivalue,2)
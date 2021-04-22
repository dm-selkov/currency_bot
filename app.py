import telebot
import requests
import json
import config

bot = telebot.TeleBot(config.TOKEN)

currency = {'доллар': 'USD', 'евро': 'EUR', 'рубль': 'RUB'}


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = '''Введите сообщение в следующем формате:
<валюта которую переводим> <в какую валюту переводим> 
<количество переводимой валюты>
Пример: доллар рубль 100
Список доступных валют: /values'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def val(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    base, quote, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={currency[base]}&tsyms={currency[quote]}')
    total = float(json.loads(r.content)[currency[quote]]) * float(amount)
    text = f'Цена {amount} {base} - {total} {quote}'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

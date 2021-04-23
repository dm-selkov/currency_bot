import telebot
from config import currency, TOKEN
from extensions import APIException, CurrencyConverter, Words

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = '''Введите сообщение в следующем формате:
<валюта которую переводим> <в какую валюту переводим> 
<количество переводимой валюты>
Пример: доллар рубль 100
Список доступных валют: /values
Десятичные дроби вводите через точку'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def val(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        list_ = message.text.lower().split(' ')
        values = [_ for _ in list_ if _ != '']
        if len(values) != 3:
            raise APIException('Неверное количество параметров. Введите команду снова')
        base, quote, amount = values
        total = CurrencyConverter.get_price(base, quote, amount)
        base = Words.morph(base, amount)
        quote = Words.morph(quote, total)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка сервера.\n{e}')
    else:
        total = '{:.2f}'.format(total)
        text = f'Цена за {amount} {base} - {total} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

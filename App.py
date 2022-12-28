import telebot
from config import keys, TOKEN
from extensions import APIException
import requests
import json

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<В какую валюту перевести> \
<Количество переводимой валюты><Пример: Доллар Рубль 100> \n Чтобы увидеть список всех доступных валют : /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'

    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    value = message.text.split(' ')
    base, quote, amount = value

    r = requests.get(
        f'https://api.apilayer.com/currency_data/convert?to={keys[quote]}&from={keys[base]}&amount={amount}&apikey=yGY23DriqRRJcZkxdiyGCw4HoAR14zjD')
    resp = json.loads(r.content)
    converted = resp['result']
    text = f'{converted} {keys[quote]} в {keys[base]} {amount}'
    bot.send_message(message.chat.id, text)

    if len(value) > 3:
        raise APIException('Слишком много параметров. ')
    if base == quote:
        raise APIException(f'Невозможно перевести одинаковые валюты {quote}. ')

    try:
        amount = float(amount)
    except ValueError:
        raise Exception(f"Не удалось обработать количество {amount}")


bot.polling()

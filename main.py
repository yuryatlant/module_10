import telebot
from extensions import ConvertionErrors, ConvertionException
from config import TOKEN, valuta

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def instruction(message: telebot.types.Message):
    text="Чтобы увидеть список доступных валют введите: /values \
\nЧтобы начать работу введите команду формата: <имя валюты> \
<в какую валюту перевести> \
<количество переводимых стредств>"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text="Доступные валюты:"
    for q in valuta.keys():
        text = "\n".join((text,q))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        allvalues = message.text.split()
        if len(allvalues) > 3:
            raise ConvertionException('Неправильное количество входных данных')
        
        base, quote, amount = allvalues
        totalvalue = ConvertionErrors.converter(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка ввода пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось сервером обработать команду \n{e}')
    else:
        text = f'При переводе {amount} {base} в {quote} валюту получаем {totalvalue}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)



from requests import get
import telebot
from telebot import types
from TOKEN import Token as Tok

Token = Tok

url = "https://www.cbr-xml-daily.ru/daily_json.js"

response = get(url)

currency = response.json()['Valute']
date = response.json()['Date'][:10]
day, month, year = date[8:], date[5:7], date[:4]


emoji_dct = {"AMD": '🇦🇲', "AUD": '🇦🇺', "AZN": '🇦🇿',
             "BGN": '🇧🇬', "BRL": '🇧🇷', "BYN": '🇧🇾',
             "CAD": '🇨🇦', "CHF": '🇨🇭', "CNY": '🇨🇳',
             "CZK": '🇨🇿', "DKK": '🇳🇱', "EUR": '🇪🇺',
             "GBP": '🇬🇧', "HUF": '🇭🇺', "INR": '🇮🇳',
             "JPY": '🇯🇵', "KGS": '🇰🇬', "KRW": '🇰🇷',
             "KZT": '🇰🇿', "MDL": '🇲🇩', "NOK": '🇳🇴',
             "PLN": '🇵🇱', "RON": '🇷🇴', "SEK": '🇸🇪',
             "SGD": '🇸🇬', "TJS": '🇹🇯', "TMT": '🇹🇲',
             "TRY": '🇹🇷', "UAH": '🇺🇦', "USD": '🇺🇸',
             "UZS": '🇺🇿', "XDR": '💵', "ZAR": '🇿🇦'}


rise_and_fall = '📈📉'


# TELEBOT COMMANDS


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_photo(message.chat.id,
                       'https://avatars.mds.yandex.net/get-zen_doc/2814495'
                       '/pub_5f85eed13940476c66f965d8_5f85ef84ae6a9712bf416ade/scale_1200',
                       f"Привет <b>{message.from_user.first_name}</b>!\n"
                       f"Я бот, который покажет тебе курс валют как относительно рубля.\n"
                       f"Чтобы посмотреть курс валют - нажми /currency", parse_mode='html')

    @bot.message_handler(commands=['currency'])
    def get_currency(message):
        markup = types.ReplyKeyboardMarkup(row_width=6, resize_keyboard=True)
        buttons = []
        for em in emoji_dct:
            buttons.append(types.KeyboardButton(f'{emoji_dct[em]}{em}'))
        markup.add(*tuple(buttons))
        bot.send_message(message.chat.id, "Выбери одну из валют", reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def Specific(message):
        try:
            cur = message.text[-3:]

            change_value = currency[cur]['Value'] - currency[cur]['Previous']
            if change_value > 0:
                icon = rise_and_fall[0]
            else:
                icon = rise_and_fall[1]

            msg = f"Курс на {day}/{month}/{year}:\n" \
                  f"{emoji_dct[cur]}{currency[cur]['Nominal']} {currency[cur]['Name']}\n" \
                  f"{icon}{currency[cur]['Value']} руб. ({round(change_value, 4)})"

            bot.send_message(message.chat.id, msg)
        except Exception as exception:
            bot.send_message(message.chat.id, "Я вас не понимаю...")

    bot.polling()


if __name__ == '__main__':
    telegram_bot(Token)

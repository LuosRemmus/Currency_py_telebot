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


def create_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for em in emoji_dct:
        btn = types.InlineKeyboardButton(f'{emoji_dct[em]}{em}', callback_data=f'{em}')
        buttons.append(btn)
    markup.add(*tuple(buttons))
    return markup


# TELEBOT COMMANDS


def telegram_bot(token: str):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message: telebot.types.Message):
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFS9ti01Nn47Flb-wzmPga3eFhakLHZwACbgADwDZPE22H7UqzeJmXKQQ')
        bot.send_message(message.chat.id,
                       f"Привет <b>{message.from_user.first_name}</b>!\n"
                       f"Я бот, который покажет тебе курс валют как относительно рубля.\n"
                       f"Чтобы посмотреть курс валют - нажми /currency", parse_mode='html')

    @bot.message_handler(commands=['currency'])
    def get_currency(message: telebot.types.Message):
        # Создание кнопок с валютами и переадресация на функцию specific
        reply = bot.send_message(message.chat.id, "Выбери одну из валют", reply_markup=create_markup())
        bot.register_next_step_handler(reply, show_currency)

    @bot.callback_query_handler(func=lambda c: c.data and c.data in emoji_dct.keys())
    def show_currency(callback_query: types.CallbackQuery):
        try:
            cur = callback_query.data[-3:]

            change_value = currency[cur]['Value'] - currency[cur]['Previous']  # Изменение значения курса
            if change_value > 0:  # Выбор эмоджи в соответствии с характером изменения курса валюты (растёт/падает)
                icon = rise_and_fall[0]
            else:
                icon = rise_and_fall[1]

            msg = f"Курс на {day}/{month}/{year}:\n" \
                  f"{emoji_dct[cur]}{currency[cur]['Nominal']} {currency[cur]['Name']}\n" \
                  f"{icon}{currency[cur]['Value']} руб. ({round(change_value, 4)})"

            bot.answer_callback_query(callback_query.id, text=msg, show_alert=True)

        except KeyError as key_error:
            bot.send_message(callback_query.id, "Я вас не понимаю...")
            print(f'Key error. {key_error} - {type(key_error)}')

        except TypeError as type_error:
            bot.send_message(callback_query.id, 'Я вас не понимаю...')
            print(f'Type error. {type_error} - {type(type_error)}')

        except AttributeError as attribute_error:
            bot.send_message(callback_query.id, "Я вас не понимаю...")
            print(f'Attribute error. {attribute_error} - {type(attribute_error)}')

    bot.polling()


if __name__ == '__main__':
    telegram_bot(Token)

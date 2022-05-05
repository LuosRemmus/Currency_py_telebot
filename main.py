from datetime import datetime
import requests
import telebot
from telebot import types
from bs4 import BeautifulSoup
from TOKEN import Token as Tok

Token = Tok

date = datetime.now().strftime('%d/%m/%Y')

response = requests.get("https://finance.rambler.ru/currencies/")
soup = BeautifulSoup(response.text, 'lxml')

block = soup.find('div', class_='finance-currency-table__table')

header = block.find('div', class_='finance-currency-table__head').text.split()
header[3] += f' {header[4]}'
del header[4]

body = block.find('div', class_='finance-currency-table__body')

c_code = body.find_all('div', class_='finance-currency-table__cell--code')
c_denomination = body.find_all('div', class_='finance-currency-table__cell--denomination')
c_currency = body.find_all('div', class_='finance-currency-table__cell--currency')
c_value = body.find_all('div', class_='finance-currency-table__cell--value')
c_change = body.find_all('div', class_='finance-currency-table__cell--change')
c_percent = body.find_all('div', class_='finance-currency-table__cell--percent')

currency_dct = {}

for i in range(len(c_code)):
    currency_dct[c_code[i].text.rstrip().lstrip()] = (c_denomination[i].text.rstrip().lstrip(),
                                                      c_currency[i].text.rstrip().lstrip(),
                                                      c_value[i].text.rstrip().lstrip(),
                                                      c_change[i].text.rstrip().lstrip(),
                                                      c_percent[i].text.rstrip().lstrip())

emoji_list = ['🇦🇲', '🇦🇺', '🇦🇿', '🇧🇬', '🇧🇷', '🇧🇾', '🇨🇦', '🇨🇭', '🇨🇳', '🇨🇿', '🇳🇱', '🇪🇺', '🇬🇧',
              '🇭🇺', '🇮🇳', '🇯🇵', '🇰🇿',
              '🇰🇷', '🇰🇿', '🇲🇩', '🇳🇴', '🇵🇱', '🇷🇴', '🇸🇪', '🇸🇬', '🇹🇯', '🇹🇲', '🇹🇷', '🇺🇦', '🇺🇸',
              '🇺🇿', '💵', '🇿🇦']

Abbreviations = tuple(["AMD", "AUD", "AZN", "BGN", "BRL", "BYN", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR",
                       "GBP", "HUF", "INR", "JPY", "KGS", "KRW", "KZT", "MDL", "NOK", "PLN", "RON", "SEK",
                       "SGD", "TJS", "TMT", "TRY", "UAH", "USD", "UZS", "XDR", "ZAR"])


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
        btns = []
        for i in range(len(Abbreviations)):
            try:
                btns.append(types.KeyboardButton(f'{emoji_list[i]}{Abbreviations[i]}'))
            except KeyError as k:
                print(k)
        markup.add(*tuple(btns))
        bot.send_message(message.chat.id, "Выбери одну из валют", reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def Specific(message):
        if message.text[0] == '💵':
            cur = currency_dct[message.text[1:]]
            mes = f"{date}\n{'     '.join(header[1:])}\n{'     '.join(cur)}"
            bot.send_message(message.chat.id, mes)
        elif message.text[:2] in emoji_list:
            cur = currency_dct[message.text[2:]]
            mes = f"{date}\n{'     '.join(header[1:])}\n{'     '.join(cur)}"
            bot.send_message(message.chat.id, mes)
        else:
            bot.send_message(message.chat.id, "I don't understand u...")

    bot.polling()


if __name__ == '__main__':
    telegram_bot(Token)

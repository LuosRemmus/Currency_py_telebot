from datetime import datetime
import requests
import telebot
from bs4 import BeautifulSoup

Token = '5377279394:AAEo7i23FpDgPeI9FizGOhMUo24e0m_MMBU'

response = requests.get("https://finance.rambler.ru/currencies/")
soup = BeautifulSoup(response.text, 'lxml')

block = soup.find('div', class_='finance-currency-table__table')
head = block.find('div', class_='finance-currency-table__head')
body = block.find('div', class_='finance-currency-table__body')
currency = body.find_all('a', class_='finance-currency-table__tr')

header = "    ".join(head.text.split())

currency_dct = {}
emoji_dct = {}
emoji_list = ['🇦🇲', '🇦🇺', '🇦🇿', '🇧🇬', '🇧🇷', '🇧🇾', '🇨🇦', '🇨🇭', '🇨🇳', '🇨🇿', '🇳🇱', '🇪🇺', '🇬🇧',
              '🇭🇺', '🇮🇳', '🇯🇵', '🇰🇿',
              '🇰🇷', '🇰🇿', '🇲🇩', '🇳🇴', '🇵🇱', '🇷🇴', '🇸🇪', '🇸🇬', '🇹🇯', '🇹🇲', '🇹🇷', '🇺🇦', '🇺🇸',
              '🇺🇿', '💵', '🇿🇦']
for c in currency:
    currency_dct[c.text.split()[0]] = tuple(c.text.split()[1:])
    emoji_dct[c.text.split()[0]] = ''

cnt_v = 0
for value in emoji_dct:
    try:
        emoji_dct[value] = emoji_list[cnt_v]
    except IndexError as e:
        print(e)
    cnt_v += 1


def get_data():
    body_ = "\n".join(["    ".join(c.text.split()) for c in currency])
    return f"{datetime.now().strftime('%d/%m/%Y, %H:%M')}\n" \
           f"{header}\n" \
           f"{body_}"


def sorted_by_value():
    body_ = sorted([i.text.split() for i in currency], key=lambda x: float(x[-3]) / float(x[1]), reverse=True)
    s = "\n".join(["    ".join(b) for b in body_])

    return f"{datetime.now().strftime('%d/%m/%Y, %H:%M')}\n" \
           f"{header}\n" \
           f"{s}"


def sorted_by_ud_percent():
    body_ = sorted([i.text.split() for i in currency], key=lambda x: float(x[-1][1:-1]), reverse=True)
    s = "\n".join(["   ".join(b) for b in body_])

    return f"{datetime.now().strftime('%d/%m/%Y, %H:%M')}\n" \
           f"{header}\n" \
           f"{s}"


def sorted_by_ud_value_():
    body_ = sorted([i.text.split() for i in currency], key=lambda x: float(x[-2][1:]), reverse=True)
    s = "\n".join(["    ".join(b) for b in body_])

    return f"{datetime.now().strftime('%d/%m/%Y, %H:%M')}\n" \
           f"{header}\n" \
           f"{s}"


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет!\n"
                                          "Я бот, который покажет тебе курс валют относительно рубля.\n"
                                          "Чтобы посмотреть все команды - нажми /info")

    @bot.message_handler(commands=["info"])
    def info(message):
        bot.send_message(message.chat.id, "/info - Посмотреть все команды\n\n"
                                          "/sort_by_alphabet - Посмотреть курс валют относительно рубля"
                                          "(Сортировка по алфавиту)\n"
                                          "/sorted_by_value - сортировка от большего к меньшему (по значению)\n"
                                          "/sorted_by_ud_percent - сортировка по проценту изменения курса\n"
                                          "/sorted_by_ud_value - сортировка по значению изменения курса\n\n"
                                          "Чтобы посмотреть курс конеретной валюты "
                                          "введите её аббревиатуру в верхнем регистре через slash (например /USD)")

    @bot.message_handler(commands=["sort_by_alphabet"])
    def send_text(message):
        try:
            bot.send_message(message.chat.id, get_data())
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "Something goes wrong... Try later")

    @bot.message_handler(commands=["sorted_by_value"])
    def sort_currency_by_value(message):
        bot.send_message(message.chat.id, sorted_by_value())

    @bot.message_handler(commands=["sorted_by_ud_percent"])
    def sort_currency_by_ud_percent(message):
        bot.send_message(message.chat.id, sorted_by_ud_percent())

    @bot.message_handler(commands=["sorted_by_ud_value"])
    def sort_currency_by_ud_value(message):
        bot.send_message(message.chat.id, sorted_by_ud_value_())

    @bot.message_handler(commands=["AMD", "AUD", "AZN", "BGN", "BRL", "BYN", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR",
                                   "GBP", "HUF", "INR", "JPY", "KGS", "KRW", "KZT", "MLD", "NOK", "PLN", "RON", "SEK",
                                   "SGD", "TJS", "TMT", "TRY", "UAH", "USD", "UZS", "XDR", "ZAR"])
    def get_currency(message):
        crn = '    '.join(currency_dct[message.text[1:]])
        msg = f"{datetime.now().strftime('%d/%m/%Y, %H:%M')}\n{header}\n{emoji_dct[message.text[1:]]}{crn}"
        bot.send_message(message.chat.id, msg)

    bot.polling()


if __name__ == '__main__':
    telegram_bot(Token)

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


def get_data():
    a = "    ".join(head.text.split())
    b = "\n".join(["    ".join(c.text.split()) for c in currency])
    return f"{datetime.now().strftime('%d/%m/%Y, %H:%M')}\n" \
           f"{a}\n" \
           f"{b}"


def sorted_by_value():
    header = "    ".join(head.text.split())
    body_ = sorted([i.text.split() for i in currency], key=lambda x: float(x[-3]) / float(x[1]), reverse=True)
    s = "\n".join(["    ".join(b) for b in body_])

    return f"{datetime.now().strftime('%d/%m/%Y, %H:%M')}\n" \
           f"{header}\n" \
           f"{s}"


def sorted_by_ud():
    header = "   ".join(head.text.split())
    body_ = sorted([i.text.split() for i in currency], key=lambda x: float(x[-1][1:-1]), reverse=True)
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
        bot.send_message(message.chat.id, "/info - Посмотреть все команды\n"
                                          "/currency - Посмотреть курс валют относительно рубля\n"
                                          "/sorted_by_value - сортировка от большего к меньшему (по значению)\n"
                                          "/sorted_by_ud = сортировка по проценту изменения курса")

    @bot.message_handler(commands=["currency"])
    def send_text(message):
        try:
            bot.send_message(message.chat.id, get_data())
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "Something goes wrong... Try later")

    @bot.message_handler(commands=["sorted_by_value"])
    def sort_currency_by_value(message):
        bot.send_message(message.chat.id, sorted_by_value())

    @bot.message_handler(commands=["sorted_by_ud"])
    def sort_currency_by_ud(message):
        bot.send_message(message.chat.id, sorted_by_ud())

    bot.polling()


if __name__ == '__main__':
    telegram_bot(Token)

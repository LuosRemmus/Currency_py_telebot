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

emoji_dct = {"AMD": '๐ฆ๐ฒ', "AUD": '๐ฆ๐บ', "AZN": '๐ฆ๐ฟ',
             "BGN": '๐ง๐ฌ', "BRL": '๐ง๐ท', "BYN": '๐ง๐พ',
             "CAD": '๐จ๐ฆ', "CHF": '๐จ๐ญ', "CNY": '๐จ๐ณ',
             "CZK": '๐จ๐ฟ', "DKK": '๐ณ๐ฑ', "EUR": '๐ช๐บ',
             "GBP": '๐ฌ๐ง', "HUF": '๐ญ๐บ', "INR": '๐ฎ๐ณ',
             "JPY": '๐ฏ๐ต', "KGS": '๐ฐ๐ฌ', "KRW": '๐ฐ๐ท',
             "KZT": '๐ฐ๐ฟ', "MDL": '๐ฒ๐ฉ', "NOK": '๐ณ๐ด',
             "PLN": '๐ต๐ฑ', "RON": '๐ท๐ด', "SEK": '๐ธ๐ช',
             "SGD": '๐ธ๐ฌ', "TJS": '๐น๐ฏ', "TMT": '๐น๐ฒ',
             "TRY": '๐น๐ท', "UAH": '๐บ๐ฆ', "USD": '๐บ๐ธ',
             "UZS": '๐บ๐ฟ', "XDR": '๐ต', "ZAR": '๐ฟ๐ฆ'}

rise_and_fall = '๐๐'


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
                       f"ะัะธะฒะตั <b>{message.from_user.first_name}</b>!\n"
                       f"ะฏ ะฑะพั, ะบะพัะพััะน ะฟะพะบะฐะถะตั ัะตะฑะต ะบััั ะฒะฐะปัั ะพัะฝะพัะธัะตะปัะฝะพ ััะฑะปั.\n"
                       f"ะงัะพะฑั ะฟะพัะผะพััะตัั ะบััั ะฒะฐะปัั - ะฝะฐะถะผะธ /currency", parse_mode='html')

    @bot.message_handler(commands=['currency'])
    def get_currency(message: telebot.types.Message):
        # ะกะพะทะดะฐะฝะธะต ะบะฝะพะฟะพะบ ั ะฒะฐะปััะฐะผะธ ะธ ะฟะตัะตะฐะดัะตัะฐัะธั ะฝะฐ ััะฝะบัะธั specific
        reply = bot.send_message(message.chat.id, "ะัะฑะตัะธ ะพะดะฝั ะธะท ะฒะฐะปัั\nะ ะบะพะฝัะต ะฝะฐะถะผะธ ะฝะฐ ะบะพะผะฐะฝะดั /stop", reply_markup=create_markup())
        bot.register_next_step_handler(reply, show_currency)

    @bot.callback_query_handler(func=lambda c: c.data and c.data in emoji_dct.keys())
    def show_currency(callback_query: types.CallbackQuery):
        try:
            cur = callback_query.data[-3:]

            change_value = currency[cur]['Value'] - currency[cur]['Previous']  # ะะทะผะตะฝะตะฝะธะต ะทะฝะฐัะตะฝะธั ะบัััะฐ
            if change_value > 0:  # ะัะฑะพั ัะผะพะดะถะธ ะฒ ัะพะพัะฒะตัััะฒะธะธ ั ัะฐัะฐะบัะตัะพะผ ะธะทะผะตะฝะตะฝะธั ะบัััะฐ ะฒะฐะปััั (ัะฐัััั/ะฟะฐะดะฐะตั)
                icon = rise_and_fall[0]
            else:
                icon = rise_and_fall[1]

            msg = f"ะััั ะฝะฐ {day}/{month}/{year}:\n" \
                  f"{emoji_dct[cur]}{currency[cur]['Nominal']} {currency[cur]['Name']}\n" \
                  f"{icon}{currency[cur]['Value']} ััะฑ. ({round(change_value, 4)})"

            bot.answer_callback_query(callback_query.id, text=msg, show_alert=True)

        except AttributeError as a:
            print(f"Exception - {a}({type(a)})")

    bot.polling()


if __name__ == '__main__':
    telegram_bot(Token)

import telebot
from config import TG_API_KEY
from model_config import Model


class Bot_Messages:
    def __init__(self):
        self.welcome_message = 'Привет, Я Бот-помощник от "Росаккредитация"'
        self.information_message = 'Для взаимодейтсвтя со мной необходимо ввести наимнование продукта и качестве\n' \
                                   'Например: "Детские игрушки" -> Рекомендация по сертификации'
        self.help_message = 'Если возник экстренный вопрос - обратитесь за помощью по номеру +71112223344'
        self.check_product_message = 'Необходимо вводить полное наименование продукта:\n' \
                                     'Изделия детские санитарно-гигиенические из полимерных материалов (100% ' \
                                     'полипропилен) для ухода за детьми'
        self.incorrect_data = 'Были введены некорректные данные, попробуйте ввести данные в следующем формета:\n' \
                              '"Изделия детские санитарно-гигиенические из полимерных материалов (100% ' \
                              'полипропилен) для ухода за детьми"'


bot = telebot.TeleBot(TG_API_KEY)
model_name = 'multi-qa-MiniLM-L6-cos-v1'


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Инструкция по применению")
    btn2 = telebot.types.KeyboardButton("Проверить продукт")
    btn3 = telebot.types.KeyboardButton("Экстренная помощь")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, Bot_Messages().welcome_message, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def ask_question(message):
    if message.text == "Инструкция по применению":
        bot.send_message(message.chat.id, text=Bot_Messages().information_message)
    elif message.text == "Экстренная помощь":
        bot.send_message(message.chat.id, text=Bot_Messages().help_message)

    elif message.text == "Проверить продукт":
        bot.send_message(message.chat.id, text=Bot_Messages().check_product_message)

    # elif message.text == "Как меня зовут?":
    #     bot.send_message(message.chat.id, "У меня нет имени..")
    #
    # elif message.text == "Что я могу?":
    #     bot.send_message(message.chat.id, text="Поздороваться с читателями")
    #
    # elif message.text == "Вернуться в главное меню":
    #     markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     button1 = telebot.types.KeyboardButton("👋 Поздороваться")
    #     button2 = telebot.types.KeyboardButton("❓ Задать вопрос")
    #     markup.add(button1, button2)
    #     bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        model = Model(model_name=model_name)
        if len(message.text) > 0:
            bot.send_message(message.chat.id, text=f"Eqt list: {model.get_recommendation(query=message.text)}")
        else:
            bot.send_message(message.chat.id, text=Bot_Messages().incorrect_data)


bot.polling(none_stop=True)

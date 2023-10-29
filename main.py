import pandas as pd
import telebot
from config import TG_API_KEY
from model_config import Model


class Bot_Messages:
    def __init__(self):
        self.welcome_message = 'Привет, Я Бот-помощник от "Росаккредитация"'
        self.information_message = 'Для взаимодействия со мной необходимо ввести наименование продукта и качество\n' \
                                   'Например: "Детские игрушки" -> Рекомендация по сертификации.\n' \
                                   'Также можно загрузить файл в формате (.csv), в качестве ответа вы получите (.csv) с ' \
                                   'дополнительными столбцом рекомендаций.'
        self.help_message = 'Если возник экстренный вопрос - обратитесь за помощью по номеру +71112223344'
        self.check_product_message = 'Необходимо вводить полное наименование продукта:\n' \
                                     'Изделия детские санитарно-гигиенические из полимерных материалов (10% ' \
                                     'полипропилен) для ухода за детьми'
        self.incorrect_data = 'Были введены некорректные данные, попробуйте ввести данные в следующем формета:\n' \
                              '"Изделия детские санитарно-гигиенические из полимерных материалов (10% ' \
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
def handle_text_question(message):
    if message.text == "Инструкция по применению":
        bot.send_message(message.chat.id, text=Bot_Messages().information_message)
    elif message.text == "Экстренная помощь":
        bot.send_message(message.chat.id, text=Bot_Messages().help_message)

    elif message.text == "Проверить продукт":
        bot.send_message(message.chat.id, text=Bot_Messages().check_product_message)

    else:
        model = Model(model_name=model_name)
        if len(message.text) > 0:
            bot.send_message(message.chat.id, text=f"{model.get_recommendation_card(query=message.text)}")
        else:
            bot.send_message(message.chat.id, text=Bot_Messages().incorrect_data)


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = f'{file_info.file_path}'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    model = Model(model_name=model_name)
    file = model.preprocess_input_user_file(path=src)

    filepath = 'documents/new_uploading.csv'
    file.to_csv(filepath)
    nfile_uploading = open(filepath, 'rb')

    bot.send_document(message.chat.id, document=nfile_uploading)


bot.polling(none_stop=True)

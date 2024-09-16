# from aiogram import Bot, Dispatcher, types
from io import BytesIO
import json
import telebot
import webbrowser
from telebot import types
from helping_funcs import *
from logs_funcs import *
from model_funcs import *
from parsing_funcs import *
from translate import translate
from enum import Enum
import zlib
import os
import sqlite3
import nltk
from telebot.types import InputMediaPhoto

import logging
import time
import os


# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
from datetime import datetime
logging.basicConfig(level=logging.INFO, filename="logs_main.log", filemode="a")


TOKEN = '7057108680:AAG3D09tiRrPmYgvrz33CDVGU4G0IqinWf8'
bot = telebot.TeleBot(TOKEN)
stopwords = ['и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между', 'это']
chat_found_items = {}
chat_states = {}


@bot.message_handler(commands=['wildberries'])
def site(message):
    webbrowser.open('https://wildberries.ru')


@bot.message_handler(commands=['yamarket'])
def site(message):
    webbrowser.open('https://market.yandex.ru/')


@bot.message_handler(commands=['start'])
def main(message, first=True):
    ''' запускает стартовое окно '''

    conn = sqlite3.connect(f"base.sql")
    cur = conn.cursor()
    chat_id = 0
    try:
        chat_id = message.message.chat.id
    except:
        chat_id = message.chat.id

    # logging block
    timestamp = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    event_name = 'start'
    user_id = str(chat_id)
    event_value = 'none'
    info = ['info', timestamp, user_id, event_name, event_value]
    logging.info(';'.join(info))


    cur.execute(f'CREATE TABLE IF NOT EXISTS user_{chat_id} (id int auto_increment primary key, name TEXT, url TEXT)')
    conn.commit()
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Перейти к вишлисту", callback_data='list')
    btn2 = types.InlineKeyboardButton("Поиск по фото", callback_data='photo_search')
    btn3 = types.InlineKeyboardButton("Поиск по тексту", callback_data='text_search')
    markup.row(btn1)
    markup.row(btn2, btn3)
    if first:
        bot.send_message(chat_id, f'Привет, {message.from_user.first_name}, выбери дальнейшее действие',
                         reply_markup=markup)
    else:
        bot.send_message(chat_id, f'{message.from_user.first_name}, выбери дальнейшее действие', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    ''' нажимание кнопки '''

    # logging block

    timestamp = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    if callback.data == 'text_search':
        # logging block
        event_name = 'text_search'
        user_id = str(callback.message.chat.id)
        event_value = 'none'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        bot.send_message(callback.message.chat.id, "Введи интересующий запрос, пожалуйста")
        bot.register_next_step_handler(callback.message, enter_request)

        return
    elif callback.data == 'photo_search':
        # logging block
        event_name = 'photo_search'
        user_id = str(callback.message.chat.id)
        event_value = 'none'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        bot.send_message(callback.message.chat.id, "Отправь, пожалуйста, фото")
        chat_states[callback.message.chat.id] = 1
        bot.register_next_step_handler(callback.message, enter_photo)
    elif callback.data == "list":
        # logging block
        event_name = 'wishlist'
        user_id = str(callback.from_user.id)
        event_value = 'none'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        get_wishlist_comands(callback.message)
        return
    elif callback.data == "open_wishlist":
        # logging block
        event_name = 'open_wishlist'
        user_id = str(callback.message.chat.id)
        event_value = 'none'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        conn = sqlite3.connect(f"base.sql")
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM user_{callback.message.chat.id}')
        wish_list = cur.fetchall()
        cur.close()
        conn.close()
        keyboard = types.InlineKeyboardMarkup()
        for el in wish_list:
            url_button = types.InlineKeyboardButton(text=el[1], url=el[2])
            keyboard.add(url_button)
        if len(wish_list) == 0:
            bot.send_message(callback.message.chat.id, "Вы еще ничего не добавляли в вишлист")
        else:
            bot.send_message(callback.message.chat.id, "Здесь все ваши любимые товары", reply_markup=keyboard)
        main(callback, False)
        return
    elif callback.data == "add_to_wishlist":
        # logging block
        event_name = 'add_to_wishlist'
        user_id = str(callback.message.chat.id)
        event_value = 'none'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        bot.send_message(callback.message.chat.id, "Введите  название и ссылку на товар в формате name - url")
        bot.register_next_step_handler(callback.message, enter_item_wl)
        return
    elif "add_to_wl_after_search" in callback.data:
        # logging block
        event_name = 'add_to_wl_after_search'
        user_id = str(callback.message.chat.id)
        event_value = 'none'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        bot.send_message(callback.message.chat.id,
                         "Введите  номера понравившихся товаров через запятую, например 1, 2, 3")
        bot.register_next_step_handler(callback.message, lambda m: enter_item_wl_list(m))
    elif callback.data == "rm_from_wishlist":
        # logging block
        event_name = 'rm_from_wishlist'
        user_id = str(callback.message.chat.id)
        event_value = 'none'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        bot.send_message(callback.message.chat.id, "Введите  название и ссылку на товар в формате name - url")
        bot.register_next_step_handler(callback.message, lambda m: enter_item_wl(m, False))
    elif callback.data == "start":
        # logging block
        event_name = 'go_to_start'
        user_id = str(callback.message.chat.id)
        event_value = 'button'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        main(callback, False)
        return
    elif "serp: " in callback.data:
        # logging block
        event_name = 'serp'
        user_id = str(callback.message.chat.id)
        event_value = 'none'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))
        # Отправляем Даше логи
        return
    else:
        # logging block
        event_name = 'serp'
        user_id = str(callback.message.chat.id)
        event_value = 'none'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))
        pass


def enter_item_wl_list(message):
    ''' добавление айтема в вишлист '''

    timestamp = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    if message.text == "/start":
        # logging block
        event_name = 'go_to_start'
        user_id = str(message.chat.id)
        event_value = 'wish_list'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        main(message, False)
        return
    item_inds = []
    try:
        item_inds = [int(num) for num in message.text.split(", ")]
    except:
        # logging block
        event_name = 'wishlist_items_add'
        user_id = str(message.chat.id)
        event_value = 'error_format'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        bot.send_message(message.chat.id, "Кажется вы ввели номера в некорректном формате, попробуйте еще раз")
        bot.register_next_step_handler(message, lambda m: enter_item_wl_list(m))
        return

    # logging block
    event_name = 'wishlist_items_add'
    user_id = str(message.chat.id)
    event_value = '_'.join(list(map(str, item_inds)))
    info = ['info', timestamp, user_id, event_name, event_value]
    logging.info(';'.join(info))

    curr_found_list = chat_found_items[message.chat.id]
    for ind in item_inds:
        if ind > len(curr_found_list):
            bot.send_message(message.chat.id, f"Кажется, индекс {ind} слишком большой, попробуйте еще раз")
            bot.register_next_step_handler(message, lambda m: enter_item_wl_list(m))
            return
        if ind <= 0:
            bot.send_message(message.chat.id, f"Кажется, индекс {ind} <= 0, попробуйте еще раз")
            bot.register_next_step_handler(message, lambda m: enter_item_wl_list(m))
            return
        ind -= 1
        name = curr_found_list[ind][0]
        url = curr_found_list[ind][1]
        conn = sqlite3.connect(f"base.sql")
        cur = conn.cursor()
        cur.execute(f'DELETE FROM user_{message.chat.id} WHERE url == "{url}"')  # чтобы не было дубликатов
        cur.execute(f'INSERT INTO user_{message.chat.id} (name, url) values ("{name}", "{url}")')
        conn.commit()
        cur.close()
        conn.close()
    bot.send_message(message.chat.id, "товары успешно добавлены в вишлист")
    main(message, False)


def enter_photo(message):
    ''' приклепление фото '''

    timestamp = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    # message.chat.id
    if (message.text == "/start"):
        # logging block
        event_name = 'go_to_start'
        user_id = str(message.chat.id)
        event_value = 'photo_search'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        main(message)
        return
    file_id = 0
    try:
        # logging block
        event_name = 'wishlist_items_add'
        user_id = str(message.chat.id)
        event_value = 'none'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        file_id = message.photo[-1].file_id
    except:
        # logging block
        event_name = 'wishlist_items_add'
        user_id = str(message.chat.id)
        event_value = 'error'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        bot.send_message(message.chat.id, "Кажется вы отправили не фото, попробуйте еще раз")
        bot.register_next_step_handler(message, lambda m: enter_photo(m))
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
    response = requests.get(file_url)
    photo = Image.open(BytesIO(response.content))
    original_file_path = f"curr_photo_{message.chat.id}.jpg"
    photo.save(original_file_path)
    bot.send_message(message.chat.id, "Осуществляется поиск, надо немного подождать")
    text = get_text_res(original_file_path)

    text = translate(text).split(',')[0].split(' ')
    #global stopwords
    text_upd = ""
    i = 0
    while i < len(text) and text[i] in stopwords:
       i += 1
    for j in range(i, len(text)):
        text_upd += text[j] + " "
    products_wb = parse_top_wildberriest(text_upd)  # [url, name, price]
    products_lamoda = parse_top_lamoda(text_upd)
    products_alik = parse_top_aliexpress(text_upd)
    products = products_wb[:4] + products_lamoda[:3] + products_alik[:3]
    keyboard = types.InlineKeyboardMarkup()
    photos = []
    leng_wb = min(len(products_wb), 4)
    for el in products[:leng_wb]:
        url_button = types.InlineKeyboardButton(text=el[1], url=el[0], callback_data=f'serp: {message.text}')
        keyboard.add(url_button)
        photos.append(InputMediaPhoto(open(el[-1], 'rb')))
    for el in products_wb:
        os.remove(el[-1])
    for el in products[leng_wb:]:
        url_button = types.InlineKeyboardButton(text=el[1], url=el[0], callback_data=f'serp: {message.text}')
        keyboard.add(url_button)
        photos.append(InputMediaPhoto(el[-1]))
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Вернуться в начало", callback_data='start')
    btn2 = types.InlineKeyboardButton("Продолжить поиск по картинке", callback_data='photo_search')
    items = [[el[1], el[0]] for el in products]
    global chat_found_items
    chat_found_items[message.chat.id] = items
    btn3 = types.InlineKeyboardButton("Обновить вишлист", callback_data=f'add_to_wl_after_search')
    markup.row(btn2)
    markup.row(btn1, btn3)
    bot.send_media_group(chat_id=message.chat.id, media=photos)
    bot.send_message(message.chat.id, "Самое лучшее, что мы нашли: ", reply_markup=keyboard)
    bot.send_message(message.chat.id, "Выберите следующее действие", reply_markup=markup)


def enter_request(message):
    ''' ввод текстового запроса для поиска '''

    timestamp = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    if message.text == "/start":
        # logging block
        event_name = 'go_to_start'
        user_id = str(message.chat.id)
        event_value = 'text_search'
        info = ['info', timestamp, user_id, event_name, event_value]
        logging.info(';'.join(info))

        main(message)
        return
    bot.send_message(message.chat.id, "Осуществляется поиск, надо немного подождать")
    products_wb = parse_top_wildberriest(message.text)  # [url, name, price, pic_url]
    products_lamoda = parse_top_lamoda(message.text)
    products_alik = parse_top_aliexpress(message.text)
    products = products_wb[:4] + products_lamoda[:3] + products_alik[:3]
    # logging block
    event_name = 'text_search'
    user_id = str(message.chat.id)
    event_value = str(message.text).replace(' ', '-')
    info = ['info', timestamp, user_id, event_name, event_value]
    logging.info(';'.join(info))

    keyboard = types.InlineKeyboardMarkup()
    for el in products:
        url_button = types.InlineKeyboardButton(text=el[1], url=el[0], callback_data=f'serp: {message.text}')
        keyboard.add(url_button)
    items = [[el[1], el[0]] for el in products]
    leng_wb = min(len(products_wb), 4)
    photos = [InputMediaPhoto(open(el[-1], 'rb')) for el in products[:leng_wb]]
    for el in products_wb:
        os.remove(el[-1])
    for el in products[leng_wb:]:
        photos.append(InputMediaPhoto(el[-1]))
    chat_found_items[message.chat.id] = items
    btn3 = types.InlineKeyboardButton("Обновить вишлист", callback_data=f'add_to_wl_after_search')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Вернуться в начало", callback_data='start')
    btn2 = types.InlineKeyboardButton("Продолжить поиск по тексту", callback_data='text_search')
    markup.row(btn2)
    markup.row(btn1, btn3)
    bot.send_media_group(chat_id=message.chat.id, media=photos)
    bot.send_message(message.chat.id, "Самое лучшее, что мы нашли: ", reply_markup=keyboard)
    bot.send_message(message.chat.id, "Выберите следующее действие", reply_markup=markup)


def enter_item_wl(message, add=True):
    ''' выбор айтемов для виш-листа '''
    if (message.text == "/start"):
        main(message, False)
        return
    input = message.text.split(' - ') if message.text is not None else ' '
    if len(input) != 2 or ' ' in input[1]:
        bot.send_message(message.chat.id, "Вы ввели неправильный формат, попробуйте еще раз")
        bot.register_next_step_handler(message, lambda m: enter_item_wl(m, add))
    else:
        name = input[0]
        url = input[1]
        conn = sqlite3.connect(f"base.sql")
        cur = conn.cursor()
        cur.execute(f'DELETE FROM user_{message.chat.id} WHERE url == "{url}"')  # чтобы не было дубликатов
        if add:
            cur.execute(f'INSERT INTO user_{message.chat.id} (name, url) values ("{name}", "{url}")')
        conn.commit()
        cur.close()
        conn.close()
        if add:
            bot.send_message(message.chat.id, f"Товар {name} был успешно добавлен в вишлист")
        else:
            bot.send_message(message.chat.id, f"Товар {name} был успешно удален из вишлиста")
        get_wishlist_comands(message)


def get_wishlist_comands(message):
    ''' кнопки для выбора действия в виш-листе '''
    markup = types.InlineKeyboardMarkup()
    btn0 = types.InlineKeyboardButton("Вернуться в начало", callback_data='start')
    btn1 = types.InlineKeyboardButton("Посмотреть виш-лист", callback_data='open_wishlist')
    btn2 = types.InlineKeyboardButton("Добавить пункт в виш-лист", callback_data='add_to_wishlist')
    btn3 = types.InlineKeyboardButton("Удалить пункт из виш-листа", callback_data='rm_from_wishlist')
    markup.row(btn0, btn1)
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Выбери действие", reply_markup=markup)


def on_click(message):
    ''' вишлист хз что но лучше не трогать '''
    if message.text == 'Перейти к вишлисту':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Посмотреть виш-лист", callback_data='open_wishlist')
        btn2 = types.InlineKeyboardButton("Добавить пункт в виш-лист", callback_data='add_to_wishlist')
        markup.row(btn1, btn2)
        bot.reply_to(message, "Выберите действие с вишлистом", reply_markup=markup)


# @bot.message_handler()
# def info(message):
#     if message.text.lower() == "привет":
#         bot.reply_to(message, f'Привет, {message.from_user.first_name}')

# @bot.message_handler(content_types=['photo'])
# def get_photo(message):
#     bot.reply_to(message, 'Какое красивое фото!')


bot.polling(none_stop=True)

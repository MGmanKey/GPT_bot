import datetime
import time
import openai
import json
import pprint
import sqlite3
import os
import asyncio
import buttons as nav
import hours as hrs
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.markdown import quote_html

smi_list = []  # список всех юзеров для которых запущена функция0 send_message_interval

pid = 'Подписывайся на мою группу в тг: https://t.me/chatikbotikgpt'
creator = '@koshied'
donate = "Спасибо, что решил воспользоваться ботом!\nК сожалению, хостинг платный, поэтому, если у тебя есть возможность, помоги проекту:\nhttps://yoomoney.ru/fundraise/wLc0BQUhTo0.230414\n\nСпасибо!"
channelid = '@chatikbotikgpt'
notsubmessage = 'Для доступа к боту подпишитесь на канал'

file = open('config.json', 'r')
config = json.load(file)
photocarta = open('213.png', 'rb')

openai.api_key = config['openai']
bot = Bot(config['token'])
dp = Dispatcher(bot)

messages = [
    {"role": "system", "content": "Ты полная копия ChatGPT от OpenAi. К пользователю ты обращаешься по-дружески."},
    {"role": "user", "content": "Я русский пользователь. Мне интересно все, о чем я могу задать вопрос."},
    {"role": "assistant", "content": "Привет! Чем я могу вам помочь?"}
]

old_mesages = []

conn = sqlite3.connect('db1.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (user_id INTEGER PRIMARY KEY, user_name TEXT, user_surname TEXT, username TEXT, timee TEXT)''')


def update(messages, role, content, username=None):
    if role == "user":
        content = f"{quote_html(username)}: {content}"
    old_mesages.append({"role": role, "content": content})
    return messages


def db_table_val(user_id, user_name, user_surname, username, timee):
    cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    if result is None:
        timee = datetime.datetime.now(hrs.Moscow).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username, timee) VALUES (?, ?, ?, ?, ?)' , (user_id, user_name, user_surname, username, timee))
        conn.commit()
    else:
        timee = datetime.datetime.now(hrs.Moscow).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('UPDATE users SET user_name=?, user_surname=?, username=?, timee=? WHERE user_id=?', (user_name, user_surname, username, timee, user_id))
        conn.commit()


def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    timee = datetime.datetime.now(hrs.Moscow).strftime('%Y-%m-%d %H:%M:%S')
    db_table_val(user_id=user_id, user_name=user_name, user_surname=user_surname, username=username, timee=timee)
    
    if check_sub_channel(await bot.get_chat_member(chat_id=channelid, user_id=message.from_user.id)):
        await send_message_interval(message)  # Запускаем функцию отправки сообщений с интервалом

    else:
        await bot.send_message(message.from_user.id, notsubmessage, reply_markup=nav.checkSubMenu)
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    timee = datetime.datetime.now(hrs.Moscow).strftime('%Y-%m-%d %H:%M:%S')

    db_table_val(user_id=user_id, user_name=user_name, user_surname=user_surname, username=username, timee=timee)


async def send_message_interval(message: types.Message):
    user_id = message.from_user.id
    if user_id not in smi_list:
        smi_list.append(user_id)
        while True:
            # Отправляем сообщение
            with open('213.png', 'rb') as photo:
                #await bot.send_message(text = f'{message.from_user.first_name}, приветик! ✅', chat_id=message.from_user.id)
                #await bot.send_message(user_id, text=donate)
                #await bot.send_photo(user_id, photo=(photo))
                await bot.send_photo(chat_id=user_id, photo=photo,
                                     caption=f'{message.from_user.first_name}, приветик! ✅ \n\n{donate}')
            await asyncio.sleep(43200)

    else:
        with open('213.png', 'rb') as photo:
            #await bot.send_message(text=f'{message.from_user.first_name}, приветик! ✅', chat_id=message.from_user.id)
            #await bot.send_message(user_id, text=donate)
            #await bot.send_photo(user_id, photo=(photo))
            await bot.send_photo(chat_id=user_id, photo=photo,
                                 caption=f'{message.from_user.first_name}, приветик! ✅ \n\n{donate}')


@dp.message_handler(commands=['deletecontext'])
async def forget_context(message: types.Message):
    global messages
    messages = messages[-1:]  # оставляем только последнее сообщение в контексте
    await bot.send_message(message.from_user.id, 'Контекст общения был забыт.')


@dp.message_handler(commands=['creator'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, creator)

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    timee = datetime.datetime.now(hrs.Moscow).strftime('%Y-%m-%d %H:%M:%S')

    db_table_val(user_id=user_id, user_name=user_name, user_surname=user_surname, username=username, timee=timee)


@dp.message_handler(commands=['remind'])
async def start_hendler(message: types.Message):
    user_id = message.from_user.id
    file23 = open('213.png', 'rb')
    await bot.send_photo(user_id, photo=file23)
    await bot.send_message(user_id, pid)

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    timee = datetime.datetime.now(hrs.Moscow).strftime('%Y-%m-%d %H:%M:%S')

    db_table_val(user_id=user_id, user_name=user_name, user_surname=user_surname, username=username, timee=timee)


@dp.message_handler()
async def send(message : types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=channelid, user_id=message.from_user.id)):
        usrid = message.from_user.id
        if usrid == usrid:
            update(messages, "user", message.text, message.from_user.full_name)
        filename = message.from_user.username
        user_idss = message.from_user.id
        with open(f'users/{filename}.json', 'w', encoding='utf-8') as f:
            json.dump([{'context': msg['content']} for msg in messages if user_idss == user_idss and msg['role'] == 'user'], f, indent=1, ensure_ascii=False)
        wait_message = await bot.send_message(chat_id=message.chat.id, text="Подождите, бот думает...")
        wait_message_id = wait_message.message_id
        response = openai.ChatCompletion.create(
         model = "gpt-3.5-turbo",
            messages = messages
        
        )
        await bot.edit_message_text(chat_id=message.chat.id, message_id=wait_message_id,
                                    text=response['choices'][0]['message']['content'])
        
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        user_surname = message.from_user.last_name
        username = message.from_user.username
        timee = datetime.datetime.now(hrs.Moscow).strftime('%Y-%m-%d %H:%M:%S')

        db_table_val(user_id=user_id, user_name=user_name, user_surname=user_surname, username=username, timee=timee)
    else:
        await bot.send_message(message.from_user.id, notsubmessage, reply_markup=nav.checkSubMenu)

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    timee = datetime.datetime.now(hrs.Moscow).strftime('%Y-%m-%d %H:%M:%S')

    db_table_val(user_id=user_id, user_name=user_name, user_surname=user_surname, username=username, timee=timee)


@dp.callback_query_handler(text='subchanneldone')
async def subchanneldone(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if check_sub_channel(await bot.get_chat_member(chat_id=channelid, user_id=message.from_user.id)):
        await message.answer(f'{message.from_user.first_name}, приветик! ✅')
        await send_message_interval(message)  # Запускаем функцию отправки сообщений с интервалом
    else:
        await bot.send_message(message.from_user.id, notsubmessage, reply_markup=nav.checkSubMenu)
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    timee = datetime.datetime.now(hrs.Moscow).strftime('%Y-%m-%d %H:%M:%S')

    db_table_val(user_id=user_id, user_name=user_name, user_surname=user_surname, username=username, timee=timee)

executor.start_polling(dp, skip_updates=True)
    

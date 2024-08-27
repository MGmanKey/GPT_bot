from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


btnUrlChannel = InlineKeyboardButton(text='Подписаться', url='https://t.me/chatikbotikgpt')
btnDoneSub = InlineKeyboardButton(text='Подписался', callback_data='subchanneldone')

checkSubMenu = InlineKeyboardMarkup(row_width=1)
checkSubMenu.insert(btnUrlChannel)
checkSubMenu.insert(btnDoneSub)


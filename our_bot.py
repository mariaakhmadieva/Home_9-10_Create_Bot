from telebot import TeleBot,types
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='log_book'
)

load_dotenv()
secret_token = os.getenv('TOKEN')
bot = TeleBot(secret_token)
value = ''
old_value = ''

keyboard = types.InlineKeyboardMarkup()

keyboard.row(   types.InlineKeyboardButton('1', callback_data='1'),
                types.InlineKeyboardButton('2', callback_data='2'),
                types.InlineKeyboardButton('3', callback_data='3'),
                types.InlineKeyboardButton('4', callback_data='4'),
                types.InlineKeyboardButton('5', callback_data='5'))


keyboard.row(   types.InlineKeyboardButton('6', callback_data='6'),
                types.InlineKeyboardButton('7', callback_data='7'),
                types.InlineKeyboardButton('8', callback_data='8'),
                types.InlineKeyboardButton('9', callback_data='9'),
                types.InlineKeyboardButton('0', callback_data='0'))



keyboard.row(   types.InlineKeyboardButton('+', callback_data='+'),
                types.InlineKeyboardButton('-', callback_data='-'),
                types.InlineKeyboardButton('*', callback_data='*'),
                types.InlineKeyboardButton('/', callback_data='/'),
                types.InlineKeyboardButton('j', callback_data='j'))



keyboard.row(   types.InlineKeyboardButton('c', callback_data='c'),
                types.InlineKeyboardButton('<=', callback_data='<='),
                types.InlineKeyboardButton('.', callback_data='.'),
                types.InlineKeyboardButton('=', callback_data='='))

    

@bot.message_handler(commands=['start'])
def get_message(message):
    global value
    if value == '':
        bot.send_message(message.from_user.id, 'можно начинать', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def main(query):
    global value, old_value 
    data = query.data


    if data == 'c':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value)-1]
    elif data == '=':
        try:
            value = str( eval(value) )
        except:
            value = 'error'
    else:
        value += data

    if (value != old_value and value != '') or ('0' != old_value and value == ''):
        if value == '':
            bot.edit_message_text(chat_id=query.message.chat.id, 
            message_id=query.message.message_id, 
            text='0', reply_markup=keyboard)
            old_value = '0'
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, 
            message_id=query.message.message_id, 
            text=value, reply_markup=keyboard)
            old_value = value
    
    
    if value == 'error': value = ''



bot.polling()



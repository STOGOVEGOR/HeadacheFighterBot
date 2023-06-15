# use the https://uptimerobot.com/dashboard#mainDashboard for keep flask server alive
import os
from background import keep_alive
import pip

pip.main(['install', 'pytelegrambotapi'])
import telebot
import time
from replit import db
# i need to GIT this

# HF_BOT_API_KEY = '6074172437:AAEmk8TrN7iXA92nW-UVR8utfiQ6OXQvBYk'

API_KEY = os.environ['HF_BOT_API_KEY']
bot = telebot.TeleBot(API_KEY)

# echo-function
# @bot.message_handler(content_types=['text'])
# def get_text_message(message):
#   bot.send_message(message.from_user.id, message.text)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.send_message(
    message.chat.id, """\
Hi there, I am Headache Fighter Bot.
I am here to help you understand what is triggering your headache and keep some statistic for you.
So, lets start!\
""")
  ask_questions(message)


@bot.message_handler(commands=['begin'])
def ask_questions(message):
  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.row(
    telebot.types.InlineKeyboardButton('NO', callback_data='nottoday'),
    telebot.types.InlineKeyboardButton('YES', callback_data='howstrong'))

  bot.send_message(message.chat.id,
                   'Do you have a headache today?',
                   reply_markup=keyboard)


def howstrong(message):
  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.row(
    telebot.types.InlineKeyboardButton('1', callback_data='pain1'),
    telebot.types.InlineKeyboardButton('2', callback_data='pain2'),
    telebot.types.InlineKeyboardButton('3', callback_data='pain3'),
    telebot.types.InlineKeyboardButton('4', callback_data='pain4'),
    telebot.types.InlineKeyboardButton('5', callback_data='pain5'),
  )

  bot.send_message(message.chat.id, 'How bad it was?', reply_markup=keyboard)


### reply to buttons
@bot.callback_query_handler(func=lambda call: True)
def dialogue(call):
  if call.data == 'howstrong':
    bot.send_message(chat_id=call.message.chat.id, text='111')
    howstrong(call.message)
  if call.data == 'nottoday':
    bot.send_message(call.message.chat.id,
                     text='What do we say to the God of Death? Not today!')


keep_alive()  #load flask-server
bot.polling(non_stop=True, interval=0)  #load bot

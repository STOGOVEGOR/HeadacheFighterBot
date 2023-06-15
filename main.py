# use the https://uptimerobot.com/dashboard#mainDashboard for keep flask server alive
import os
from background import keep_alive
import pip

pip.main(['install', 'pytelegrambotapi'])
import telebot
import time

# HF_BOT_API_KEY = '6074172437:AAEmk8TrN7iXA92nW-UVR8utfiQ6OXQvBYk'

API_KEY = os.environ['HF_BOT_API_KEY']
bot = telebot.TeleBot(API_KEY)

# echo-function
# @bot.message_handler(content_types=['text'])
# def get_text_message(message):
#   bot.send_message(message.from_user.id, message.text)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(
    message, """\
Hi there, I am Headache Fighter Bot.
I am here to help you understand what is triggering your headache
and keep some statistic for you.
So, lets start!\
""")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)



keep_alive()  #load flask-сервер
bot.polling(non_stop=True, interval=0)  #load bot

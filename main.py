# use the https://uptimerobot.com/dashboard#mainDashboard for keep flask server alive
import os
from background import keep_alive
import pip

pip.main(['install', 'pytelegrambotapi'])
import telebot
import time
from datetime import date, timedelta

from replit import db

API_KEY = os.environ['HF_BOT_API_KEY']
bot = telebot.TeleBot(API_KEY)

# echo-function
# @bot.message_handler(content_types=['text'])
# def get_text_message(message):
#   bot.send_message(message.from_user.id, message.text)

# ======== CALC SECTION ==========
def items_by_date(username, item, howmanydays):
    print(username, item)
    item_sum = 0
    item_count = 0
    for i in range(howmanydays):
        date_x = date.today() - timedelta(days=i)
        date_x = date_x.strftime("%d-%m-%Y")
        try:
            item_sum += db[username][date_x][item]
            item_count += 1
        except:
            print('no data in DB')
            pass
    return item_sum, item_count


# ========= BOT LOGIC =============
@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.send_message(
    message.chat.id, """\
Hi there, I am Headache Fighter Bot.
I am here to help you understand what is triggering your headache and keep some statistic for you.
So, lets start!\
""")
  print('user_id: ' + str(message.from_user.id))
  print('username1: ' + str(message.from_user.username))
  ask_questions(message)


@bot.message_handler(commands=['menu'])
def mainmenu(message):
  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.row(
    # telebot.types.InlineKeyboardButton('WEEK', callback_data='nottoday'),
    telebot.types.InlineKeyboardButton('MONTH', callback_data='nottoday'),
    telebot.types.InlineKeyboardButton('STOP', callback_data='howstrong'))
  bot.send_message(message.chat.id,
                   'Do you have a headache today?',
                   reply_markup=keyboard)
  


@bot.message_handler(commands=['begin'])
def ask_questions(message):
  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.row(
    telebot.types.InlineKeyboardButton('NO', callback_data='nottoday'),
    telebot.types.InlineKeyboardButton('YES', callback_data='howstrong'))
  print('username2: ' + str(message.from_user.username))
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


def howsleep(message):
  keyboard = telebot.types.InlineKeyboardMarkup()
  keyboard.row(
    telebot.types.InlineKeyboardButton('5', callback_data='sleep5'),
    telebot.types.InlineKeyboardButton('6', callback_data='sleep6'),
    telebot.types.InlineKeyboardButton('7', callback_data='sleep7'),
    telebot.types.InlineKeyboardButton('8', callback_data='sleep8'),
    telebot.types.InlineKeyboardButton('9', callback_data='sleep9'),
  )
  bot.send_message(message.chat.id, 'How long do you sleep in hours?', reply_markup=keyboard)


### reply to buttons
@bot.callback_query_handler(func=lambda call: True)
def dialogue(call):
  user = call.from_user.username
  cur_date = date.today().strftime("%d-%m-%Y")
  print(cur_date, user)
  if call.data == 'howstrong':
    today_entry(user, cur_date)
    db[user][cur_date]['headache'] = 1
    howstrong(call.message)
  if call.data == 'nottoday':
    today_entry(user, cur_date)
    bot.send_message(call.message.chat.id,
                     text='What do we say to the God of Death? Not today!')
    howsleep(call.message)
  if call.data in ['pain1', 'pain2', 'pain3', 'pain4', 'pain5']:
    if call.data == 'pain1':
      db[user][cur_date]['pain_level'] = 1
    if call.data == 'pain2':
      db[user][cur_date]['pain_level'] = 2
    if call.data == 'pain3':
      db[user][cur_date]['pain_level'] = 3
    if call.data == 'pain4':
      db[user][cur_date]['pain_level'] = 4
    if call.data == 'pain5':
      db[user][cur_date]['pain_level'] = 5
    howsleep(call.message)
  if call.data == 'sleep5':
    db[user][cur_date]['sleep'] = 5


def today_entry(user, cur_date):
  del db[user]
  print(cur_date)
  db[user] = {cur_date: {
    'headache': 0,
    'sleep': 0,
    'pills': 0, 
    'pain_level': 0
  }}


@bot.message_handler(commands=['stat'])
def statistic(message):
  # cur_date = date.today().strftime("%d/%m/%Y")
  username = message.from_user.username
  print(username)
  print(db[username])
  days_with_pain = items_by_date(message.from_user.username, 'headache', 7)[1]
  days_with_pills = items_by_date(message.from_user.username, 'pills', 7)[1]
  print(days_with_pain, days_with_pills)
  stat_mess = f"About your week statistic:\n\
user_id: {message.from_user.id}\n\
username: {message.from_user.username}\n\
days with pain: {days_with_pain}\n\
days with pills: {days_with_pills}\n\
average pain level:"
  bot.send_message(message.chat.id, stat_mess)
  mainmenu()


keep_alive()  #load flask-server
bot.polling(non_stop=True, interval=0)  #load bot

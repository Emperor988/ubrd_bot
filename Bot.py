import telebot
import random
import config
from telebot import types

#calendar
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
import datetime
import calendar

bot = telebot.TeleBot(config.token)







def create_options_keyboard(options, cancel_msg):
    """
    Create an options keyboard with one line featuring each option
    """
    rows = []
    for i,op in enumerate(options):
        rows.append([InlineKeyboardButton(op,callback_data="CHOSEN;"+str(i))])
    if cancel_msg is not None:
        rows.append([InlineKeyboardButton(cancel_msg,callback_data="CANCEL;0")])
    return InlineKeyboardMarkup(rows)


def process_option_selection(bot, update):
    query = update.callback_query
    data = update.callback_query.data
    action, index = data.split(";")
    ret_data = (False,None)
    if action == "CHOSEN":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            )
        ret_data = True, int(index)
    elif action == "CANCEL":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = False, 0
    else:
        bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
    return ret_data



def create_callback_data(action,year,month,day):
    """ Create the callback data associated to each button"""
    return ";".join([action,str(year),str(month),str(day)])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=None,month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    #First row - Month and Year
    row=[]
    row.append(InlineKeyboardButton(calendar.month_name[month]+" "+str(year),callback_data=data_ignore))
    keyboard.append(row)
    #Second row - Week Days
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day),callback_data=create_callback_data("DAY",year,month,day)))
        keyboard.append(row)
    #Last row - Buttons
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_callback_data("PREV-MONTH",year,month,day)))
    row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",callback_data=create_callback_data("NEXT-MONTH",year,month,day)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_calendar_selection(bot,update):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    ret_data = (False,None)
    query = update.callback_query
    (action,year,month,day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id= query.id)
    elif action == "DAY":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True,datetime.datetime(int(year),int(month),int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(pre.year),int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(ne.year),int(ne.month)))
    else:
        bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data





@bot.message_handler(commands=['/start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рандомное число 🎲")
    item2 = types.KeyboardButton("Как дела? 😊")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
        if message.text == 'Рандомное число 🎲':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))

        elif message.text == '/start':
            bot.send_message(message.chat.id,
                                     text="Приветик, я бот-бронировщик, но для тебя я просто Броня! 🥰 ❤ ")
            bot.send_message(message.chat.id,
                                     text="Сейчас я нахожусь в разработке, потерпи немного 😔 ")


        elif message.text == 'Привет 😊':
            bot.send_message(message.chat.id,
                                     text="Приветик, я бот-бронировщик, но для тебя я просто Броня! 🥰 ❤ ")
            bot.send_message(message.chat.id,
                                     text="Сейчас я нахожусь в разработке, потерпи немного 😔 ")

        elif message.text == 'Как дела? 😊':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, а ты как?',reply_markup=markup)

        elif message.text ==  message.text:
             # keyboard
             keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
             item1 = types.KeyboardButton("Привет 😊")
             item2 = types.KeyboardButton("Рандомное число 🎲")
             item3 = types.KeyboardButton("Как дела? 😊")
             item4 = types.KeyboardButton("А что ты умеешь? 🤔")

             keybord.add(item1, item2, item3, item4)

             bot.send_message(message.chat.id, 'Пиу ✨', reply_markup=keybord)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')







@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Юхууу, это прекрасно 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Эх, надеюсь все наладится 😞')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отлично, а ты как?",
                                 reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

            # keyboard
            # keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # item1 = types.KeyboardButton("Привет 😊")
            # item2 = types.KeyboardButton("Рандомное число 🎲")
            # item3 = types.KeyboardButton("Как дела? 😊")
            # item4 = types.Keyb
            #             # keybord.add(item1, item2, item3, item4)
            #
            #     except Exception as e:
            #         print(repr(e))oardButton("А что ты умеешь? 🤔")
            #

# RUN
bot.polling(none_stop=True)
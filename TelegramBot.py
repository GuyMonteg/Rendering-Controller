import telegram
import logging
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from telegram.ext import CommandHandler

# https://telegram.me/TestRenderChecker_bot

token = '610148854:AAECjZpN_HZrwIUQwb0lQt_4SAyuzMVZfDE'

bot = telegram.Bot(token=token)

updater = Updater(token=token)
dispatcher = updater.dispatcher

job_queue = updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Write /help to see available commands")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# Показать список доступных команд и их описание
def help_me(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=commands)


commands = \
    '*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n \
    /help:   Show help\n \
    /info %ID%: Show information about files in path\n \
    /follow %ID%:   Start follow a project for receive notifications\n \
    /unfollow %ID%: Unfollow a project  for don\'t receive notifications\n \
    /my_id: Show your unique id, need write to the client\n \
    /schedule %ID% %TIME%:  Change project checking time\n \
    /list:  Show list of available project (shows project id)\n \
    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n'

help_handler = CommandHandler('help', help_me)
dispatcher.add_handler(help_handler)
updater.start_polling()


def send_info(bot, update, args):
    try:
        # args[0] - Айди который отправит пользователь
        filename = 'image.jpg'  # Метод который возвращает файл с инфой
        bot.send_document(chat_id=update.message.chat_id, document=open(filename, 'rb'))
    except FileNotFoundError:
        bot.send_message(chat_id=update.message.chat_id, text='FileNotFoundError, error on server')
    except FileExistsError:
        bot.send_message(chat_id=update.message.chat_id, text='FileExistsError, Raised when trying to create a file')
    except TypeError:
        bot.send_message(chat_id=update.message.chat_id, text='TypeError, send_document() missing 1 required '
                                                              'positional '
                                                              'argument: document')


info_handler = CommandHandler('info', send_info, pass_args=True)
dispatcher.add_handler(info_handler)


# updater.start_polling()


def follow(bot, update, args):
    try:
        cred = 'Follow on: ' + args[0]
        bot.send_message(chat_id=update.message.chat_id, text=cred)
        # args[0] - Айди который отправит пользователь
    except IndexError:
        bot.send_message(chat_id=update.message.chat_id, text='IndexError, write ID after /follow')


follow_handler = CommandHandler('follow', follow, pass_args=True)
dispatcher.add_handler(follow_handler)


def unfollow(bot, update, args):
    try:
        cred = 'Unfollow from: ' + args[0]
        bot.send_message(chat_id=update.message.chat_id, text=cred)
        # args[0] = логин который вписал пользователь
    except IndexError:
        bot.send_message(chat_id=update.message.chat_id, text='IndexError, write ID after logout')


unfollow_handler = CommandHandler('unfollow', unfollow, pass_args=True)
dispatcher.add_handler(unfollow_handler)


def my_id(bot, update):
    try:
        message = 'Your ID is: ' + str(update.message.from_user.id)
        bot.sendMessage(update.message.chat_id, text=message)
    except IndexError:
        bot.send_message(chat_id=update.message.chat_id, text='IndexError, write ID')


my_id_handler = CommandHandler('my_id', my_id)
dispatcher.add_handler(my_id_handler)


def schedule(bot, update, args):
    try:
        # args[1] - Время которое вписал пользователь
        # args[0] - Проект который вписал пользователь
        return_text = 'You are set ' + args[1] + ' minute checking on the project ' + args[0]
        if True:
            bot.send_message(chat_id=update.message.chat_id, text=return_text)
        # Для отрицательного ответа
        # if not True:
        #    bot.send_message(chat_id=update.message.chat_id, text="Some error, not True")
    except IndexError:
        bot.send_message(chat_id=update.message.chat_id, text='IndexError, try to write /schedule %ID% %TIME%')


schedule_handler = CommandHandler('schedule', schedule, pass_args=True)
dispatcher.add_handler(schedule_handler)


def show_list(bot, update):
    # Метод который возвращает текст или массив с проектами сюда
    project_list = []
    try:
        bot.send_message(chat_id=update.message.chat_id, text=project_list)
    except IndexError:
        bot.send_message(chat_id=update.message.chat_id, text='IndexError')


show_list_handler = CommandHandler('list', show_list)
dispatcher.add_handler(show_list_handler)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Sorry, I didn\'t understand that command. Write /help for '
                                                          'see available commands')


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

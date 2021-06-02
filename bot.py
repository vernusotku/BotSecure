import threading
from configReader import TOKEN_BOT
import telebot
from VideoAi import start_stream

print('bot starting')
bot = telebot.TeleBot(TOKEN_BOT)


@bot.message_handler(commands='start')
def starting(message):
    threading.Thread(start_stream(bot, message))


if __name__ == '__main__':
    bot.polling(none_stop=True)

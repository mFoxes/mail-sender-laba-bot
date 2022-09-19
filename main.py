from cmath import log
from distutils.log import Log
from threading import Thread
from datetime import datetime
import time
import telebot
import smtplib
import ssl
import re

mail = 'drega2010@gmail.com'
password = 'cqfwuqdvcudwufak'
bot_token = '5546911876:AAHKANq-M3GF7URMrb9PCyj8oLFqasFmYUM'
bot = telebot.TeleBot(bot_token)

mail_reg = r'[\w\S]*@[\w\S]*\.[\w]*'


def send_mess(config):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mail, password)
        mess = ''
        if (len(config["-t"]) != 0):
            mess += "Subject: " + config["-t"][0][3:] + '\n'
        mess += config['/send'][0][6:]
        for i in re.findall(mail_reg, config['-r'][0]):
            server.sendmail(mail, i, mess.encode("utf-8"))

        return 1
    except:
        print('error')
        return 0


def send_with_timer(config):
    try:
        now = datetime.now()
        conf_time = config['-w'][0][3:].split(':')
        current_time = now.hour * 60 * 60 + now.minute * 60
        send_time = int(conf_time[0]) * 60 * 60 + int(conf_time[1]) * 60
        if (current_time > send_time):
            current_time += 24 * 60 * 60
        time.sleep(abs(current_time - send_time))
        send_mess(config)
    except:
        print('error')


@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')


@bot.message_handler(commands=["send"])
def handle_text(message):
    config = {}
    commands = ['/send', '-t', '-r', '-w']
    for command in commands:
        result = re.findall(
            rf"{command}\s[a-zA-Zа-яА-Я0-9\W][^-]*", message.text)
        config[command] = result

    if (config['-w'][0][3:] == 'сейчас'):
        if (send_mess(config)):
            bot.send_message(message.chat.id, 'Отправил')
        else:
            bot.send_message(message.chat.id, 'Чего-то не хватает')
    else:
        th = Thread(target=send_with_timer, args=(config,))
        th.start()


bot.polling(none_stop=True, interval=0)

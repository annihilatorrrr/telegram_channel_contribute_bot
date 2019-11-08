#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import time
from telegram.ext import Updater, MessageHandler, Filters
import threading
import traceback as tb

START_MESSAGE = ('''
I will allow non-admin to submit channel post, send me any suggested post please.
''')

REPLY = '''
Thank you so much for your contribution! 
Your post suggestion is recorded. Please expect to see your post in the channel soon!'
'''

with open('CREDENTIALS') as f:
    CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)

debug_group = CREDENTIALS.get('debug_group') or -1001198682178


def command(update, context):
    try:
        msg = update.message
        if (not msg) or (msg.chat_id < 0):
            return
        msg.reply_text(START_MESSAGE)
    except Exception as e:
        updater.bot.send_message(chat_id=debug_group, text=str(e)) 
        print(e)
        tb.print_exc()

def getDisplayUser(user):
    result = ''
    if user.first_name:
        result += user.first_name
    if user.last_name:
        result += ' ' + user.last_name
    if user.username:
        result += ' (' + user.username + ')'
    return '[' + result + '](tg://user?id=' + str(user.id) + ')'

def manage(update, context):
    try:
        msg = update.message
        if (not msg) or (msg.chat_id < 0):
            return 
        context.bot.send_message(
            chat_id = debug_group, 
            text = getDisplayUser(update.effective_user) + ':',                 
            parse_mode='Markdown',
            disable_web_page_preview=True)
        msg.forward(debug_group)
        msg.reply_text(REPLY)
    except Exception as e:
        updater.bot.send_message(chat_id=debug_group, text=str(e)) 
        print(e)
        tb.print_exc()   

updater = Updater(CREDENTIALS['bot_token'], use_context=True)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.private and (Filters.command), command))
dp.add_handler(MessageHandler(Filters.private and (~Filters.command), manage))

updater.start_polling()
updater.idle()
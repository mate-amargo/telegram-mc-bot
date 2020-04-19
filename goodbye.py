#!/usr/bin/env python
import telebot

TOKEN = '245068642:AAFzgu14W2c_dmroDuNA1Kp1wELqQOLUasw'

bot = telebot.TeleBot(TOKEN)
bot.config['api_key'] = TOKEN

bot.send_message('-1001193384839', 'El servidor se ha cerrado! \xF0\x9F\x98\x95')

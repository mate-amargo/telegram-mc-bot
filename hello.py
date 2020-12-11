#!/usr/bin/env python
import telebot

TOKEN = 'TOKEN'

bot = telebot.TeleBot(TOKEN)
bot.config['api_key'] = TOKEN

ip_file = open('/var/tmp/public_ip','r')
ip = ip_file.read()

bot.send_message('-1001193384839', 'El servidor acaba de arrancar con la IP ' + ip)

ip_file.close()

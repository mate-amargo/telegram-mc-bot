#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MC64BOT - A telegram Bot to interact with a Minecraft Server

"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os.path
import subprocess
from subprocess import call
from mcstatus import MinecraftServer

server = MinecraftServer.lookup("127.0.0.1:25565")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

server_dir = "/srv/mc"

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Comandos disponibles:\nstatus - Devuelve el estado del servidor.\nuptime - Tiempo desde que el servidor se inició.\nlist - Lista los jugadores conectados.\nsay - Envia un mensaje a los jugadores que están en el servidor.\nversion - Muestra la versión del servidor.\nhelp - Ayuda.')

def status(bot, update):
    if (os.path.isfile(server_dir+"/logs/up")):
      bot.sendMessage(update.message.chat_id, text='El servidor está UP')
    else:
      bot.sendMessage(update.message.chat_id, text='El servidor está DOWN')

def uptime(bot, update):
    if (os.path.isfile(server_dir+"/logs/up")):
      with open(server_dir+"/logs/up", 'r') as myfile:
        server_time=myfile.read()
      p = subprocess.Popen(['date', '+%s'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      out, err = p.communicate()
      seconds = int(out) - int(server_time)
      m, s = divmod(seconds, 60)
      h, m = divmod(m, 60)
      d, h = divmod(h, 24)
      if (d > 0):
        message = "%2d días " % (d)
      else:
        message = ""
      message += "%02d:%02d:%02d" % (h, m, s)
    else:
      message='El servidor está DOWN'
    bot.sendMessage(update.message.chat_id, text=message)
      

def list_players(bot, update):
  if (os.path.isfile(server_dir+"/logs/up")):
     status = server.status()
     if (status.players.online <= 0):
       message = "No hay nadie conectado vieja! 😞"
     else:
       message = "Jugadores conectados (" + str(status.players.online) + "):\n"
       for player in status.players.sample:
         message += player.name + "\n"
  else:
    message='Imposible saber. El servidor está DOWN'
  bot.sendMessage(update.message.chat_id, text=message)

def version(bot, update):
  if (os.path.isfile(server_dir+"/logs/up")):
     status = server.status()
     message = "Versión " + status.version.name
  else:
     message='Imposible saber. El servidor está DOWN'
  bot.sendMessage(update.message.chat_id, text=message)

def say(bot, update):
  if (os.path.isfile(server_dir+"/logs/up")):
    status = server.status()
    if (status.players.online <= 0):
      message="No hay nadie conectado! ¿Con quién querés que hable? ¿Con las paredes?"
    else:    
      user_name=update.message.from_user.first_name
      user_message=update.message.text[5:]
      call(["tmux", "send-keys", "-t", "mc_srv", "/tellraw @a [\"\", {\"text\":\"", user_name, "\",\"color\":\"blue\"},{\"text\":\" dice: " , user_message, "\",\"color\":\"reset\"}]", "C-m"])
      message="Su mensaje ha sido enviado"
  else:
    message="El servidor está DOWN! ¿Con quién querés que hable? ¿Con las paredes?"
  bot.sendMessage(update.message.chat_id, text=message)

def craft(bot, uptdate):
  item=update.message.text[5:]
  if not item:
    message="Lista de bloques crafteables\n\
             piston\n"
    bot.sendMessage(update.message.chat_id, text=message)
  elif item == "piston":
    bot.sendPhoto(update.message.chat_id, photo='./crafting/piston.png')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it our bot's token.
    updater = Updater("245068642:AAFzgu14W2c_dmroDuNA1Kp1wELqQOLUasw")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("uptime", uptime))
    dp.add_handler(CommandHandler("list", list_players))
    dp.add_handler(CommandHandler("version", version))
    dp.add_handler(CommandHandler("say", say))
    dp.add_handler(CommandHandler("craft", craft))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

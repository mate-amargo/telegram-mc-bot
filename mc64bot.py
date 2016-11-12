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
    bot.sendMessage(update.message.chat_id, text='Comandos disponibles:\nstatus - Devuelve el estado del servidor.\nuptime - Tiempo desde que el servidor se inició.\nlist - Lista los jugadores conectados.\nsay - Envia un mensaje a los jugadores que están en el servidor.\ncraft - Muestra la receta para craftear un determinado bloque/item.\nversion - Muestra la versión del servidor.\nhelp - Ayuda.')

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

def craft(bot, update):
  item=update.message.text[7:]
  if item == "planks":
    bot.sendDocument(update.message.chat_id, document=open('crafting/planks.gif', 'rb'))
  elif item == "stick":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/stick.png', 'rb'))
  elif item == "torch":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/torch.png', 'rb'))
  elif item == "crafting_table":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/crafting_table.png', 'rb'))
  elif item == "chest":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/chest.png', 'rb'))
  elif item == "furnace":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/furnace.png', 'rb'))
  elif item == "ladder":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/ladder.png', 'rb'))
  elif item == "fence":
    bot.sendDocument(update.message.chat_id, document=open('crafting/fence.gif', 'rb'))
  elif item == "boat":
    bot.sendDocument(update.message.chat_id, document=open('crafting/boat.gif', 'rb'))
  elif item == "wooden_slab":
    bot.sendDocument(update.message.chat_id, document=open('crafting/wooden_slab.gif', 'rb'))
  elif item == "slab":
    bot.sendDocument(update.message.chat_id, document=open('crafting/slab.gif', 'rb'))
  elif item == "sign":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/sign.png', 'rb'))
  elif item == "door":
    bot.sendDocument(update.message.chat_id, document=open('crafting/door.gif', 'rb'))
  elif item == "painting":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/painting.png', 'rb'))
  elif item == "bed":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/bed.png', 'rb'))
  elif item == "pickaxe":
    bot.sendDocument(update.message.chat_id, document=open('crafting/pickaxe.gif', 'rb'))
  elif item == "shovel":
    bot.sendDocument(update.message.chat_id, document=open('crafting/shovel.gif', 'rb'))
  elif item == "axe":
    bot.sendDocument(update.message.chat_id, document=open('crafting/axe.gif', 'rb'))
  elif item == "hoe":
    bot.sendDocument(update.message.chat_id, document=open('crafting/hoe.gif', 'rb'))
  elif item == "fishing_rod":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/fishing_rod.png', 'rb'))
  elif item == "flint":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/flint.png', 'rb'))
  elif item == "shears":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/shears.png', 'rb'))
  elif item == "bucket":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/bucket.png', 'rb'))
  elif item == "clock":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/clock.png', 'rb'))
  elif item == "compass":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/compass.png', 'rb'))
  elif item == "map":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/map.png', 'rb'))
  elif item == "pressure_plate":
    bot.sendDocument(update.message.chat_id, document=open('crafting/pressure_plate.gif', 'rb'))
  elif item == "lever":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/lever.png', 'rb'))
  elif item == "button":
    bot.sendDocument(update.message.chat_id, document=open('crafting/button.gif', 'rb'))
  elif item == "trapdoor":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/trapdoor.png', 'rb'))
  elif item == "piston":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/piston.png', 'rb'))
  elif item == "sticky_piston":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/sticky_piston.png', 'rb'))
  elif item == "fence_gate":
    bot.sendDocument(update.message.chat_id, document=open('crafting/fence_gate.gif', 'rb'))
  elif item == "repeater":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/repeater.png', 'rb'))
  elif item == "dispenser":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/dispenser.png', 'rb'))
  elif item == "jukebox":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/jukebox.png', 'rb'))
  elif item == "minecart":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/minecart.png', 'rb'))
  elif item == "furnace_minecart":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/furnace_minecart.png', 'rb'))
  elif item == "chest_minecart":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/chest_minecart.png', 'rb'))
  elif item == "rail":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/rail.png', 'rb'))
  elif item == "powered_rail":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/powered_rail.png', 'rb'))
  elif item == "detector_rail":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/detector_rail.png', 'rb'))
  elif item == "redstone_torch":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/redstone_torch.png', 'rb'))
  elif item == "redstone_lamp":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/redstone_lamp.png', 'rb'))
  elif item == "tripwire_hook":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/tripwire_hook.png', 'rb'))
  elif item == "activator_rail":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/activator_rail.png', 'rb'))
  elif item == "daylight_sensor":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/daylight_sensor.png', 'rb'))
  elif item == "dropper":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/dropper.png', 'rb'))
  elif item == "hopper":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/hopper.png', 'rb'))
  elif item == "hopper_minecart":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/hopper_minecart.png', 'rb'))
  elif item == "tnt_minecart":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/tnt_minecart.png', 'rb'))
  elif item == "comparator":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/comparator.png', 'rb'))
  elif item == "trapped_chest":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/trappedchest.png', 'rb'))
  elif item == "weighted_pressure_plate":
    bot.sendDocument(update.message.chat_id, document=open('crafting/weighted_pressure_plate.gif', 'rb'))
  elif item == "iron_trapdoor":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/iron_trapdoor.png', 'rb'))
  elif item == "glowstone":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/glowstone.png', 'rb'))
  elif item == "snow_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/snow_block.png', 'rb'))
  elif item == "stone_brick":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/stone_brick.png', 'rb'))
  elif item == "bricks":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/bricks.png', 'rb'))
  elif item == "sandstone":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/sandstone.png', 'rb'))
  elif item == "smooth_sandstone":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/smooth_sandstone.png', 'rb'))
  elif item == "chiseled_sandstone":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/chiseled_sandstone.png', 'rb'))
  elif item == "gold_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/gold_block.png', 'rb'))
  elif item == "diamond_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/diamond_block.png', 'rb'))
  elif item == "iron_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/iron_block.png', 'rb'))
  elif item == "lapislazuli_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/lapislazuli_block.png', 'rb'))
  elif item == "emerald_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/emerald_block.png', 'rb'))
  elif item == "coal_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/coal_block.png', 'rb'))
  elif item == "white_wool":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/white_wool.png', 'rb'))
  elif item == "bookshelf":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/bookshelf.png', 'rb'))
  elif item == "note_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/note_block.png', 'rb'))
  elif item == "clay":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/clay.png', 'rb'))
  elif item == "jack-o-lantern":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/jack-o-lantern.png', 'rb'))
  elif item == "tnt":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/tnt.png', 'rb'))
  elif item == "wooden_stairs":
    bot.sendDocument(update.message.chat_id, document=open('crafting/wooden_stairs.gif', 'rb'))
  elif item == "stairs":
    bot.sendDocument(update.message.chat_id, document=open('crafting/stairs.gif', 'rb'))
  elif item == "cobblestone_wall":
    bot.sendDocument(update.message.chat_id, document=open('crafting/cobblestone_wall.gif', 'rb'))
  elif item == "redstone_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/redstone_block.png', 'rb'))
  elif item == "nether_brick":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/nether_brick.png', 'rb'))
  elif item == "red_nether_brick":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/red_nether_brick.png', 'rb'))
  elif item == "nether_brick_fence":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/nether_brick_fence.png', 'rb'))
  elif item == "nether_wart_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/nether_wart_block.png', 'rb'))
  elif item == "bone_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/bone_block.png', 'rb'))
  elif item == "magma_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/magma_block.png', 'rb'))
  elif item == "purpur_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/purpur_block.png', 'rb'))
  elif item == "end_rod":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/end_rod.png', 'rb'))
  elif item == "purpur_pillar":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/purpur_pillar.png', 'rb'))
  elif item == "quartz_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/quartz_block.png', 'rb'))
  elif item == "chiseled_quartz":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/chiseled_quartz.png', 'rb'))
  elif item == "quartz_pillar":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/quartz_pillar.png', 'rb'))
  elif item == "hay_bale":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/hay_bale.png', 'rb'))
  elif item == "stained_clay":
    bot.sendDocument(update.message.chat_id, document=open('crafting/stained_clay.gif', 'rb'))
  elif item == "stained_glass":
    bot.sendDocument(update.message.chat_id, document=open('crafting/stained_glass.gif', 'rb'))
  elif item == "granite":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/granite.png', 'rb'))
  elif item == "andesite":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/andesite.png', 'rb'))
  elif item == "diorite":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/diorite.png', 'rb'))
  elif item == "polished_granite":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/polished_granite.png', 'rb'))
  elif item == "polished_andesite":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/polished_andesite.png', 'rb'))
  elif item == "polished_diorite":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/polished_diorite.png', 'rb'))
  elif item == "prismarine":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/prismarine.png', 'rb'))
  elif item == "dark_prismarine":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/dark_prismarine.png', 'rb'))
  elif item == "prismarine_bricks":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/prismarine_bricks.png', 'rb'))
  elif item == "sea_lantern":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/sea_lantern.png', 'rb'))
  elif item == "coarse_dirt":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/coarse_dirt.png', 'rb'))
  elif item == "slime_block":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/slime_block.png', 'rb'))
  elif item == "moss_stone":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/moss_stone.png', 'rb'))
  elif item == "mossy_stone_bricks":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/mossy_stone_bricks.png', 'rb'))
  elif item == "chiseled_stone_brick":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/chiseled_stone_brick.png', 'rb'))
  elif item == "red_sandstone":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/red_sandstone.png', 'rb'))
  elif item == "smooth_red_sandstone":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/smooth_red_sandstone.png', 'rb'))
  elif item == "chiseled_red_sandstone":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/chiseled_red_sandstone.png', 'rb'))
  elif item == "helmet":
    bot.sendDocument(update.message.chat_id, document=open('crafting/helmet.gif', 'rb'))
  elif item == "chestplate":
    bot.sendDocument(update.message.chat_id, document=open('crafting/chestplate.gif', 'rb'))
  elif item == "leggings":
    bot.sendDocument(update.message.chat_id, document=open('crafting/leggings.gif', 'rb'))
  elif item == "boots":
    bot.sendDocument(update.message.chat_id, document=open('crafting/boots.gif', 'rb'))
  elif item == "sword":
    bot.sendDocument(update.message.chat_id, document=open('crafting/sword.gif', 'rb'))
  elif item == "bow":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/bow.png', 'rb'))
  elif item == "arrow":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/arrow.png', 'rb'))
  elif item == "cake":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/cake.png', 'rb'))
  elif item == "bread":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/bread.png', 'rb'))
  elif item == "cookie":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/cookie.png', 'rb'))
  elif item == "bowl":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/bowl.png', 'rb'))
  elif item == "mushroom_stew":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/mushroom_stew.png', 'rb'))
  elif item == "beetroot_soup":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/beetroot_soup.png', 'rb'))
  elif item == "golden_apple":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/golden_apple.png', 'rb'))
  elif item == "pumpkin_seeds":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/pumpkin_seeds.png', 'rb'))
  elif item == "melon_seeds":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/melon_seeds.png', 'rb'))
  elif item == "melon":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/melon.png', 'rb'))
  elif item == "sugar":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/sugar.png', 'rb'))
  elif item == "golden_carrot":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/golden_carrot.png', 'rb'))
  elif item == "pumpking_pie":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/pumpking_pie.png', 'rb'))
  elif item == "rabbit_stew":
    bot.sendDocument(update.message.chat_id, document=open('crafting/rabbit_stew.gif', 'rb'))
  elif item == "glass_bottle":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/glass_bottle.png', 'rb'))
  elif item == "cauldron":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/cauldron.png', 'rb'))
  elif item == "brewing_stand":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/brewing_stand.png', 'rb'))
  elif item == "glistering_melon":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/glistering_melon.png', 'rb'))
  elif item == "blaze_powder":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/blaze_powder.png', 'rb'))
  elif item == "fermented_spider_eye":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/fermented_spider_eye.png', 'rb'))
  elif item == "magma_cream":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/magma_cream.png', 'rb'))
  elif item == "paper":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/paper.png', 'rb'))
  elif item == "book":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/book.png', 'rb'))
  elif item == "book_and_quill":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/book_and_quill.png', 'rb'))
  elif item == "iron_bars":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/iron_bars.png', 'rb'))
  elif item == "gold_ingot":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/gold_ingot.png', 'rb'))
  elif item == "eye_of_ender":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/eye_of_ender.png', 'rb'))
  elif item == "enchantment_table":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/enchantment_table.png', 'rb'))
  elif item == "fire_charge":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/fire_charge.png', 'rb'))
  elif item == "ender_chest":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/ender_chest.png', 'rb'))
  elif item == "beacon":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/beacon.png', 'rb'))
  elif item == "anvil":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/anvil.png', 'rb'))
  elif item == "flower_pot":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/flower_pot.png', 'rb'))
  elif item == "item_frame":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/item_frame.png', 'rb'))
  elif item == "carrot_on_a_stick":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/carrot_on_a_stick.png', 'rb'))
  elif item == "firework_star":
    bot.sendDocument(update.message.chat_id, document=open('crafting/firework_star.gif', 'rb'))
  elif item == "firework_rocket":
    bot.sendDocument(update.message.chat_id, document=open('crafting/firework_rocket.gif', 'rb'))
  elif item == "lead":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/lead.png', 'rb'))
  elif item == "carpet":
    bot.sendDocument(update.message.chat_id, document=open('crafting/carpet.gif', 'rb'))
  elif item == "glass_pane":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/glass_pane.png', 'rb'))
  elif item == "leather":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/leather.png', 'rb'))
  elif item == "banner":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/banner.png', 'rb'))
  elif item == "armor_stand":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/armor_stand.png', 'rb'))
  elif item == "red_dye":
    bot.sendDocument(update.message.chat_id, document=open('crafting/red_dye.gif', 'rb'))
  elif item == "yellow_dye":
    bot.sendDocument(update.message.chat_id, document=open('crafting/yellow_dye.gif', 'rb'))
  elif item == "cyan_dye":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/cyan_dye.png', 'rb'))
  elif item == "pink_dye":
    bot.sendDocument(update.message.chat_id, document=open('crafting/pink_dye.gif', 'rb'))
  elif item == "purple_dye":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/purple_dye.png', 'rb'))
  elif item == "magenta_dye":
    bot.sendDocument(update.message.chat_id, document=open('crafting/magenta_dye.gif', 'rb'))
  elif item == "lime_dye":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/lime_dye.png', 'rb'))
  elif item == "light_blue_dye":
    bot.sendDocument(update.message.chat_id, document=open('crafting/light_blue_dye.gif', 'rb'))
  elif item == "orange_dye":
    bot.sendDocument(update.message.chat_id, document=open('crafting/orange_dye.gif', 'rb'))
  elif item == "light_gray_dye":
    bot.sendDocument(update.message.chat_id, document=open('crafting/light_gray_dye.gif', 'rb'))
  elif item == "gray_dye":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/gray_dye.png', 'rb'))
  elif item == "bone_meal":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/bone_meal.png', 'rb'))
  elif item == "dyed_wool":
    bot.sendDocument(update.message.chat_id, document=open('crafting/dyed_wool.gif', 'rb'))
  elif item == "spectral_arrow":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/spectral_arrow.png', 'rb'))
  elif item == "tipped_arrow":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/tipped_arrow.png', 'rb'))
  elif item == "shield":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/shield.png', 'rb'))
  elif item == "observer":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/observer.png', 'rb'))
  elif item == "shulker_box":
    bot.sendPhoto(update.message.chat_id, photo=open('crafting/shulker_box.png', 'rb'))
  elif item == "color_shulker_box":
    bot.sendDocument(update.message.chat_id, document=open('crafting/color_shulker_box.gif', 'rb'))
  else:  
    message="Lista de bloques crafteables:\nactivator_rail andesite anvil armor_stand arrow axe banner beacon bed beetroot_soup blaze_powder boat bone_block bone_meal book_and_quill book bookshelf boots bowl bow bread brewing_stand bricks bucket button cake carpet carrot_on_a_stick cauldron chest_minecart chestplate chest chiseled_quartz chiseled_red_sandstone chiseled_sandstone chiseled_stone_brick clay clock coal_block coarse_dirt cobblestone_wall comparator compass cookie crafting_table cyan_dye dark_prismarine daylight_sensor detector_rail diamond_block diorite dispenser door dropper dyed_wool emerald_block enchantment_table ender_chest end_rod eye_of_ender fence_gate fence fermented_spider_eye fire_charge fire firework_rocket firework_star fishing_rod flint flower_pot furnace_minecart furnace glass_bottle glass_pane glistering_melon glowstone gold_block golden_apple golden_carrot gold_ingot granite gray_dye hay_bale helmet hoe hopper_minecart hopper iron_bars iron_block iron_trapdoor item_frame jack-o-lantern jukebox ladder lapislazuli_block lead leather leggings lever light_blue_dye light_gray_dye lime_dye magenta_dye magma_block magma_cream map melon melon_seeds minecart moss_stone mossy_stone_bricks mushroom_stew nether_brick_fence nether_brick nether_wart_block note_block orange_dye painting paper pickaxe pink_dye piston planks polished_andesite polished_diorite polished_granite powered_rail pressure_plate prismarine_bricks prismarine pumpking_pie pumpkin_seeds purple_dye purpur_block purpur_pillar quartz_block quartz_pillar rabbit_stew rail red_dye red_nether_brick red_sandstone redstone_block redstone_lamp redstone_torch repeater sandstone sea_lantern shears shovel sign slab slime_block smooth_red_sandstone smooth_sandstone snow_block stained_clay stained_glass stairs stick sticky_piston stone_brick sugar sword tnt_minecart tnt torch trapdoor trapped_chest tripwire_hook weighted_pressure_plate white_wool wooden_slab wooden_stairs yellow_dye\n"
    bot.sendMessage(update.message.chat_id, text=message)

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

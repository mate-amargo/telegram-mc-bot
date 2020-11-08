#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MC64BOT - A telegram Bot to interact with a Minecraft Server

from telegram.ext import Updater, CommandHandler
import logging
import os.path
import subprocess
from subprocess import call
from mcstatus import MinecraftServer


server = MinecraftServer.lookup("127.0.0.1:25565")
token = "TOKEN"


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


server_dir = "/home/minecraft/server"


allowed_gifs = (
    "planks",
    "fence",
    "boat",
    "wooden_slab",
    "slab",
    "door",
    "pickaxe",
    "shovel",
    "axe",
    "hoe",
    "pressure_plate",
    "button",
    "fence_gate",
    "weighted_pressure_plate",
    "wooden_stairs",
    "stairs",
    "cobblestone_wall",
    "stained_clay",
    "stained_glass",
    "helmet",
    "chestplate",
    "leggings",
    "boots",
    "sword",
    "rabbit_stew",
    "firework_star",
    "firework_rocket",
    "carpet",
    "red_dye",
    "yellow_dye",
    "pink_dye",
    "magenta_dye",
    "light_blue_dye",
    "orange_dye",
    "light_gray_dye",
    "dyed_wool",
    "color_shulker_box",
)
allowed_pngs = (
    "stick",
    "torch",
    "crafting_table",
    "chest",
    "furnace",
    "ladder",
    "sign",
    "painting",
    "bed",
    "fishing_rod",
    "flint",
    "shears",
    "bucket",
    "clock",
    "compass",
    "map",
    "lever",
    "trapdoor",
    "piston",
    "sticky_piston",
    "repeater",
    "dispenser",
    "jukebox",
    "minecart",
    "furnace_minecart",
    "chest_minecart",
    "rail",
    "powered_rail",
    "detector_rail",
    "redstone_torch",
    "redstone_lamp",
    "tripwire_hook",
    "activator_rail",
    "daylight_sensor",
    "dropper",
    "hopper",
    "hopper_minecart",
    "tnt_minecart",
    "comparator",
    "trapped_chest",
    "iron_trapdoor",
    "glowstone",
    "snow_block",
    "stone_brick",
    "bricks",
    "sandstone",
    "smooth_sandstone",
    "chiseled_sandstone",
    "gold_block",
    "diamond_block",
    "iron_block",
    "lapislazuli_block",
    "emerald_block",
    "coal_block",
    "white_wool",
    "bookshelf",
    "note_block",
    "clay",
    "jack-,o-lantern"
    "tnt",
    "redstone_block",
    "nether_brick",
    "red_nether_brick",
    "nether_brick_fence",
    "nether_wart_block",
    "bone_block",
    "magma_block",
    "purpur_block",
    "end_rod",
    "end_crystal",
    "purpur_pillar",
    "quartz_block",
    "chiseled_quartz",
    "quartz_pillar",
    "hay_bale",
    "granite",
    "andesite",
    "diorite",
    "polished_granite",
    "polished_andesite",
    "polished_diorite",
    "prismarine",
    "dark_prismarine",
    "prismarine_bricks",
    "sea_lantern",
    "coarse_dirt",
    "slime_block",
    "moss_stone",
    "mossy_stone_bricks",
    "chiseled_stone_brick",
    "red_sandstone",
    "smooth_red_sandstone",
    "chiseled_red_sandstone",
    "bow",
    "arrow",
    "cake",
    "bread",
    "cookie",
    "bowl",
    "mushroom_stew",
    "beetroot_soup",
    "golden_apple",
    "pumpkin_seeds",
    "melon_seeds",
    "melon",
    "sugar",
    "golden_carrot",
    "pumpking_pie",
    "glass_bottle",
    "cauldron",
    "brewing_stand",
    "glistering_melon",
    "blaze_powder",
    "fermented_spider_eye",
    "magma_cream",
    "paper",
    "book",
    "book_and_quill",
    "iron_bars",
    "gold_ingot",
    "eye_of_ender",
    "enchantment_table",
    "fire_charge",
    "ender_chest",
    "beacon",
    "anvil",
    "flower_pot",
    "item_frame",
    "carrot_on_a_stick",
    "lead",
    "glass_pane",
    "leather",
    "banner",
    "armor_stand",
    "cyan_dye",
    "purple_dye",
    "lime_dye",
    "gray_dye",
    "bone_meal",
    "spectral_arrow",
    "tipped_arrow",
    "shield",
    "observer",
    "shulker_box",
)


def safe_sender(failure_message="El servidor está DOWN"):
    def inner(callable):
        def wrapper(bot, update):
            chat_id = update.message.chat_id
            message = callable(bot, update) if (os.path.isfile(
                server_dir + "/logs/up")) else failure_message
            bot.sendMessage(chat_id, text=message)
        return wrapper
    return inner


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="Comandos disponibles:\nstatus - Devuelve el estado del servidor.\nip - Muestra la IP del servidor.\nuptime - Tiempo desde que el servidor se inició.\nlist - Lista los jugadores conectados.\nsay - Envia un mensaje a los jugadores que están en el servidor.\ncraft - Muestra la receta para craftear un determinado bloque/item.\nversion - Muestra la versión del servidor.\nhelp - Ayuda.")


@safe_sender()
def status(_bot, _update):
    message = "El servidor está UP"
    return message


@safe_sender()
def ip(_bot, _update):
    with open("/var/tmp/public_ip", "r") as file:
        ip = file.read()
        message = ip
    return message


@safe_sender()
def uptime(_bot, _update):
    with open(server_dir+"/logs/up", "r") as file:
        server_time = file.read()
    p = subprocess.Popen(
        ["date", "+%s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _err = p.communicate()
    seconds = int(out) - int(server_time)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    message = "%2d día%s" % (d, "s " if d > 1 else " ") if (d > 0) else ""
    message += "%02d:%02d:%02d" % (h, m, s)
    return message


@safe_sender()
def list_players(_bot, _update):
    status = server.status()
    message = "No hay nadie conectado vieja! 😞" if (
        status.players.online <= 0) else "Jugadores conectados (" + \
        str(status.players.online) + "):\n"
    for player in status.players.sample:
        message += player.name + "\n"
    return message


@safe_sender("Imposible saber. El servidor está DOWN")
def version(_bot, _update):
    status = server.status()
    message = "Versión " + status.version.name.encode("utf-8")
    return message


@safe_sender("El servidor está DOWN! ¿Con quién querés que hable? ¿Con las paredes?")
def say(_bot, update):
    status = server.status()
    if (status.players.online <= 0):
        message = "No hay nadie conectado! ¿Con quién querés que hable? ¿Con las paredes?"
    else:
        user_name = update.message.from_user.first_name
        user_message = update.message.text[5:]
        call(["tmux", "-u", "send-keys", "-t", "mc_srv:0",
              "tellraw @a [\"\", {\"text\":\"", user_name, "\",\"color\":\"blue\"},{\"text\":\" dice: ", user_message, "\",\"color\":\"reset\"}]", "C-m"])
        message = "Su mensaje ha sido enviado"
    return message


def craft(bot, update):
    item = update.message.text[7:]
    chat_id = update.message.chat_id
    if item in allowed_gifs:
        bot.sendDocument(chat_id, document=open(
            "crafting/%s.gif" % (item,), "rb"))
    elif item in allowed_pngs:
        bot.sendPhoto(chat_id, photo=open("crafting/%s.png" % (item,), "rb"))
    else:
        message = "Lista de bloques crafteables:\n%s\n" % (
            " ".join(sorted(allowed_gifs + allowed_pngs)),)
        bot.sendMessage(update.message.chat_id, text=message)


def error(bot, update, error):
    logger.warn("Update '%s' caused error '%s'" % (update, error))


def main():
    # Create the EventHandler and pass it our bot"s token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    commands = {
        "help": help,
        "status": status,
        "ip": ip,
        "uptime": uptime,
        "list": list_players,
        "version": version,
        "say": say,
        "craft": craft,
    }
    for name, function in commands.items():
        dp.add_handler(CommandHandler(name, function))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()

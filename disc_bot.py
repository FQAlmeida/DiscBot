# Imports
import discord
from discord.ext import commands
from discord import Status

import configparser
from log import logger

from apps.morse_app import morse_cog
from apps.gw2_app import gw2_cog
from apps.music_app import music_cog
from apps.funny_app import fun_cog
from apps.events_app.events import WelcomeMember
from util import util
from os import environ


# Setup Logger
logger = logger.setup_logger()


# Configs object, see README for format
configs = configparser.ConfigParser()
configs.read("data/configs.ini")
# Bot object
bot = commands.Bot(command_prefix='?', description='A simple bot for discord')



@bot.event
async def on_ready():
    """ Remember """
    msg = util.welcome_console_msg(bot.user)
    print(msg)
    await bot.change_presence(activity=discord.Game(name="Waiting..."), status=Status.idle)
    logger.log(logger.INFO, util.get_log_msg(msg))


@bot.event
async def on_member_join(member: discord.Member):
    """ Remember """
    welcome = WelcomeMember(bot, member)
    await welcome.send_welcome_msg()


@bot.command(pass_context=True)
async def notfuntest(ctx):
    await on_member_join(ctx.message.author)


bot.add_cog(music_cog.MusicCog(bot))
bot.add_cog(morse_cog.MorseCog(bot))
bot.add_cog(gw2_cog.Gw2Cog(bot))
bot.add_cog(fun_cog.FunCog(bot))

try:
    token = configs["TOKEN"].get("token")
except:
    token = environ.get("DISCORD_TOKEN")

bot.run(token)

# Imports
import discord
from discord.ext import commands
import random
from apps.morse_app.morse import Morse
from apps.gw2_app import gw2
import configparser
from log import logger
from util import util


# Setup Logger
logger = logger.setup_logger()

# Morse Object
msg_morse = Morse()

# GW2 Object
guild_wars_2 = gw2.GW2()

# Configs object, see README for format
configs = configparser.ConfigParser()
configs.read("data/configs.ini")

# Bot object
bot = commands.Bot(command_prefix='?', description='A simple bot for discord')


# Define a greeting on bots is stated
@bot.event
async def on_ready():
    msg = util.welcome_console_msg(bot.user)
    print(msg)
    logger.log(logger.INFO, util.get_log_msg(msg))


# Test method
@bot.command()
async def test():
    msg = "Hello World!, Am I alive?"
    await bot.say(msg)
    logger.log(logger.INFO, util.get_log_say_msg(msg))


# Method that returns 😝 or 👑, like if you are flipping a coin
@bot.command()
async def coin():
    if random.randint(1, 2) == 1:
        msg = "😝"
    else:
        msg = "👑"
    await bot.say(msg)
    logger.log(logger.INFO, util.get_log_say_msg(msg))


# Method that returns if the member are a admin or not, admin verification needs to be more effective
@bot.command(pass_context=True)
async def admin(ctx: discord.ext.commands.Context):
    # List of admins ids
    admin_ids = {'358652273217372161'}
    if ctx.message.author.id in admin_ids:
        msg = "You're the B.O.S.S"
    else:
        msg = "You aren't the B.O.S.S"
    await bot.say(msg)
    logger.log(logger.INFO, util.get_log_say_msg(msg))


# Method that says when the member joined
@bot.command(pass_context=True)
async def joined(ctx):
    member = ctx.message.author
    msg = f"{member.name} joined at {member.joined_at}"
    await bot.say(msg)
    logger.log(logger.INFO, util.get_log_say_msg(msg))


# Method that returns the author's converted message to morse_app
@bot.command(pass_context=True)
async def morse(ctx: discord.ext.commands.Context):
    msg = str(ctx.message.content).replace("?morse ", "")
    msg_parsed = msg_morse.conv(msg)
    await bot.say(msg_parsed)
    logger.log(logger.INFO, util.get_log_say_msg(msg_parsed))


@bot.group(pass_context=True)
async def gw2(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Invalid gw2 command passed...')


@gw2.group(pass_context=True)
async def token(ctx: discord.ext.commands.Context):
    if ctx.invoked_subcommand is None:
        await bot.say('Invalid token command passed...')
    else:
        await bot.delete_message(ctx.message)


@token.command(pass_context=True)
async def add(ctx: discord.ext.commands.Context, msg: str):
    check = guild_wars_2.token.add_token(msg, ctx.message.author.id)
    msg = "Token Adicionado com sucesso" if check else "Token Inválido"
    await bot.say(msg)


@token.command(pass_context=True)
async def remove(ctx: discord.ext.commands.Context):
    check = guild_wars_2.token.remove_token(ctx.message.author.id)
    msg = "Token removido com sucesso" if check else "Token Inválido"
    await bot.say(msg)


@token.command(pass_context=True)
async def update(ctx: discord.ext.commands.Context, msg: str):
    check = guild_wars_2.token.update_token(owner=ctx.message.author.id, token=msg)
    msg = "Token atualizado com sucesso" if check else "Token Inválido"
    await bot.say(msg)

bot.run(configs["TOKEN"].get("token"))

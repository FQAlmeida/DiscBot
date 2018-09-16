# Imports
import discord
from discord.ext import commands
import random
from morse.morse import Morse
import configparser

# Morse Object
msg_morse = Morse()

# Configs object, see README for format
configs = configparser.ConfigParser()
configs.read("data/configs.ini")

# Bot object
bot = commands.Bot(command_prefix='?', description='A simple bot for discord')


# Define a greeting on bots is stated
@bot.event
async def on_ready():
    print('BOT ONLINE - Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------------------')


# Test method
@bot.command()
async def test():
    await bot.say("Hello World!, Am I alive?")


# Method that returns 😝 or 👑, like if you are flipping a coin
@bot.command()
async def coin():
    if random.randint(1, 2) == 1:
        await bot.say('😝')
    else:
        await bot.say('👑')


# Method that returns if the member are a admin or not, admin verification needs to be more effective
@bot.command(pass_context=True)
async def admin(ctx: discord.ext.commands.Context):
    # List of admins ids
    admin_ids = {'358652273217372161'}
    if ctx.message.author.id in admin_ids:
        await bot.say("You're the B.O.S.S")
    else:
        await bot.say("You aren't the B.O.S.S")


# Method that says when the member joined
@bot.command(pass_context=True)
async def joined(ctx):
    member = ctx.message.author
    await bot.say(f'{member.name} joined at {member.joined_at}')


# Method that returns the author's converted message to morse
@bot.command()
async def morse(msg: str):
    await bot.say(msg_morse.conv(msg.lower()))

bot.run(configs["TOKEN"].get("token"))

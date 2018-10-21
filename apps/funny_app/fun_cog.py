import discord
from discord.ext import commands
import random


class FunCog:
    def __init__(self, bot):
        self.bot = bot

    # Test method
    @commands.command()
    async def test(self):
        """ Remember """
        msg = "Hello World!, Am I alive?"
        await self.bot.say(msg)

    # Method that returns 😝 or 👑, like if you are flipping a coin
    @commands.command()
    async def coin(self):
        """ Remember """
        if random.randint(1, 2) == 1:
            msg = "😝"
        else:
            msg = "👑"
        await self.bot.say(msg)

    # Method that returns if the member are a admin or not, admin verification needs to be more effective
    @commands.command(pass_context=True)
    async def admin(self, ctx: discord.ext.commands.Context):
        """ Remember """
        # List of admins ids
        admin_ids = {'358652273217372161'}
        if ctx.message.author.id in admin_ids:
            msg = "You're the B.O.S.S"
        else:
            msg = "You aren't the B.O.S.S"
        await self.bot.say(msg)

    # Method that says when the member joined
    @commands.command(pass_context=True)
    async def joined(self, ctx):
        """ Remember """
        member = ctx.message.author
        msg = f"{member.name} joined at {member.joined_at}"
        await self.bot.say(msg)

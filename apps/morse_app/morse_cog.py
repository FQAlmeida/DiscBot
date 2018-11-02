import discord
from discord.ext import commands
from apps.morse_app import morse


class MorseCog:
    def __init__(self, bot):
        self.morse_obj = morse.Morse()
        self.bot = bot

    @commands.command(pass_context=True)
    async def morse(self, ctx: discord.ext.commands.Context):
        """ Method that returns the author's message converted to morse """
        msg = str(ctx.message.content).replace("?morse ", "")
        msg_parsed = self.morse_obj.conv(msg)
        await self.bot.say(msg_parsed)

import discord
from discord.ext.commands import (command, Cog, Context)
from apps.morse_app import morse


class MorseCog(Cog):
    def __init__(self, bot):
        self.morse_obj = morse.Morse()

    async def morse(self, ctx: Context):
        """ Method that returns the author's message converted to morse """
        if ctx.message:
            msg = str(ctx.message.content).replace("?morse ", "")
            msg_parsed = self.morse_obj.conv(msg)
            await ctx.send(msg_parsed)

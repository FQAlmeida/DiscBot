from apps.gw2_app.achievements import daily
from apps.gw2_app.apitoken import api_token

import discord
from discord.ext import commands

from util import util


class Gw2Cog:
    def __init__(self, bot):
        self.token_obj = api_token.Token()
        self.daily_obj = daily.Daily()
        self.bot = bot

    @commands.group(pass_context=True)
    async def gw2(self, ctx):
        """ Remember """
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid gw2 command passed...')

    @gw2.group(pass_context=True)
    async def token(self, ctx: discord.ext.commands.Context):
        """ Remember """
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid token command passed...')
        else:
            await self.bot.delete_message(ctx.message)

    @token.command(pass_context=True)
    async def add(self, ctx: discord.ext.commands.Context, msg: str):
        """ Remember """
        check = self.token_obj.add_token(msg, ctx.message.author.id)
        msg = "Token Adicionado com sucesso" if check else "Token Inválido"
        await self.bot.say(msg)

    @token.command(pass_context=True)
    async def remove(self, ctx: discord.ext.commands.Context):
        """ Remember """
        check = self.token_obj.remove_token(ctx.message.author.id)
        msg = "Token removido com sucesso" if check else "Token Inválido"
        await self.bot.say(msg)

    @token.command(pass_context=True)
    async def update(self, ctx: discord.ext.commands.Context, msg: str):
        """ Remember """
        check = self.token_obj.update_token(owner=ctx.message.author.id, token=msg)
        msg = "Token atualizado com sucesso" if check else "Token Inválido"
        await self.bot.say(msg)

    @gw2.command()
    async def dailies(self, tomorrow: str = "today"):
        """ Remember """
        await self.bot.change_presence(game=discord.Game(name="Processing..."))
        tomorrow = True if tomorrow is not None and tomorrow.lower() == "tomorrow" else False
        all_dailies = self.daily_obj.get_dailies(tomorrow=tomorrow)
        for key, value in all_dailies.items():
            if value:
                msg = util.dailies_desc(value, key, tomorrow)
                await self.bot.say(embed=msg)
        await self.bot.change_presence(game=discord.Game(name="Waiting..."))

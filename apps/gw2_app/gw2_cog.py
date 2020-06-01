from apps.gw2_app.achievements import daily
from apps.gw2_app.apitoken import api_token
from apps.gw2_app.builds import builds

import discord
from discord.ext.commands import (Cog, group, Bot, Context)
from discord import Status

from util import util


class Gw2Cog(Cog):
    def __init__(self, bot: Bot):
        self.token_obj = api_token.Token()
        self.daily_obj = daily.Daily()
        self.builds_obj = builds.Gw2Build()
        self.bot = bot

    @group()
    async def gw2(self, ctx: Context):
        """ Remember """
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid gw2 command passed...')

    @gw2.group()
    async def token(self, ctx: Context):
        """ Remember """
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid token command passed...')
        else:
            await ctx.message.delete()

    @token.command()
    async def add(self, ctx: Context, msg: str):
        """ Remember """
        check = self.token_obj.add_token(msg, ctx.message.author.id)
        msg = "Token Adicionado com sucesso" if check else "Token Inválido"
        await ctx.send(msg)

    @token.command()
    async def remove(self, ctx: Context):
        """ Remember """
        check = self.token_obj.remove_token(ctx.message.author.id)
        msg = "Token removido com sucesso" if check else "Token Inválido"
        await ctx.send(msg)

    @token.command()
    async def update(self, ctx: Context, msg: str):
        """ Remember """
        check = self.token_obj.update_token(owner=ctx.message.author.id, token=msg)
        msg = "Token atualizado com sucesso" if check else "Token Inválido"
        await ctx.send(msg)

    @gw2.command()
    async def dailies(self, ctx: Context, tomorrow: str = "today"):
        """ Remember """
        await self.bot.change_presence(activity=discord.Game(name="Processing..."), status=Status.do_not_disturb)
        tomorrow = True if tomorrow is not None and tomorrow.lower() == "tomorrow" else False
        all_dailies = self.daily_obj.get_dailies(tomorrow=tomorrow)
        for key, value in all_dailies.items():
            if value:
                msg = util.dailies_desc(value, key, tomorrow)
                await ctx.send(embed=msg)
        await self.bot.change_presence(activity=discord.Game(name="Waiting..."), status=Status.idle)
    
    @gw2.command()
    async def build(self, ctx: Context, msg: str):
        """ Remember """
        async with ctx.channel.typing():
            await self.bot.change_presence(activity=discord.Game(name="Processing..."), status=Status.do_not_disturb)
            msgs = self.builds_obj.mount_build(ctx.message.author.id, msg)
            if msgs:
                for msg in msgs:
                    await ctx.send(embed=msg)
            await self.bot.change_presence(activity=discord.Game(name="Waiting..."), status=Status.idle)
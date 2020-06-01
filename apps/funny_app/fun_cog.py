import discord
from discord.ext.commands import (command, Cog, Context)
import random


class FunCog(Cog):
    # Test method
    @command()
    async def test(self, ctx: Context):
        """ Remember """
        msg = "Hello World!, Am I alive?"
        await ctx.send(msg)

    # Method that returns 😝 or 👑, like if you are flipping a coin
    @command()
    async def coin(self, ctx: Context):
        """ Remember """
        if random.randint(1, 2) == 1:
            msg = "😝"
        else:
            msg = "👑"
        await ctx.send(msg)

    # Method that returns if the member are a admin or not, admin verification needs to be more effective
    @command()
    async def admin(self, ctx: Context):
        """ Remember """
        # List of admins ids
        admin_roles = ('ADMIN',)
        user_admins_roles = list()
        for role in ctx.author.roles:
            if role.name.upper() in admin_roles:
                user_admins_roles.append(role)
        if len(user_admins_roles) > 0:
            msg = "You're the B.O.S.S"
        else:
            msg = "You aren't the B.O.S.S"
        await ctx.send(msg)

    # Method that says when the member joined
    @command()
    async def joined(self, ctx: Context):
        """ Remember """
        member = ctx.message.author
        msg = f"{member.name} joined at {member.joined_at}"
        await ctx.send(msg)

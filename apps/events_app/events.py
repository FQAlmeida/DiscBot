import discord
import requests
from discord.ext.commands import Bot
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps


class WelcomeMember:
    def __init__(self, bot: Bot, member: discord.Member):
        self.bot = bot
        self.member = member

    async def new_member_role(self):
        role = discord.utils.get(self.member.server.roles, name="New Member")
        await self.bot.add_roles(self.member, role)

    async def send_welcome_msg(self):        
        server = discord.utils.get(self.bot.servers, name="FQA")
        channel = discord.utils.get(
            self.bot.get_all_channels(), server=server, name="welcome")
        image_name = self.mount_welcome_image(
            self.member.avatar_url, self.member.name)
        emoji = discord.utils.get(self.member.server.emojis, name="crownturtle")
        msg = f"Hey {self.member.mention}! {emoji}"
        await self.bot.send_file(channel, image_name, content=msg)

    def mount_welcome_image(self, avatar_url, member_name):
        """
            Build the welcome image
        """

        # conts declaration
        avatar_size = (117, 118)
        avatar_pos = (342, 100)
        crown_size = (80, 70)
        crown_pos = (360, 42)
        text_size = 70
        text_color = (231, 205, 84)

        # avatar build
        req = requests.get(avatar_url)
        avatar = Image.open(BytesIO(req.content))
        avatar = avatar.resize(avatar_size)
        bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        # crown build
        crown = Image.open('apps/events_app/images/crown.png')
        crown = crown.resize(crown_size)

        # open background for text build
        background = Image.open('apps/events_app/images/background.png')

        # text build
        font = ImageFont.truetype(
            'apps/events_app/fonts/AGothiqueTime.ttf', text_size)
        text_draw = ImageDraw.Draw(background)
        text = f"Bem-Vindo ao meu servidor {member_name}"
        text_s = text_draw.textsize(text, font=font)
        text_pos = ((400 - (text_s[0] / 2)), 245)
        text_draw.text(xy=text_pos, text=text,
                      fill=text_color, font=font)

        # background build
        background.paste(avatar, avatar_pos, avatar)
        background.paste(crown, crown_pos, crown)
        background.save('apps/events_app/images/welcome.png')

        return 'apps/events_app/images/welcome.png'


if __name__ == "__main__":
    avatar = Image.open(
        'apps/events_app/images/avatar.png')
    avatar = avatar.resize((117, 118))
    bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(avatar.size, Image.ANTIALIAS)
    avatar.putalpha(mask)

    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save(
        'apps/events_app/images/avatar.png')

    #avatar = Image.open('avatar.png')
    fundo = Image.open('apps/events_app/images/background.png')
    crown = Image.open('apps/events_app/images/crown.png')
    crown = crown.resize((80, 70))
    fonte = ImageFont.truetype('apps/events_app/fonts/AGothiqueTime.ttf', 70)
    escrever = ImageDraw.Draw(fundo)
    text = "Novo TuTorial :D"
    x, y = escrever.textsize(text, font=fonte)
    escrever.text(xy=((400-x/2), 245), text=text,
                  fill=(255, 255, 255), font=fonte)
    fundo.paste(avatar, (342, 100), avatar)
    fundo.paste(crown,  (360, 42), crown)
    fundo.save('events_app/images/1.png')
    fundo.show('events_app/images/1.png')

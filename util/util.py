import datetime

import discord
import switch as switch


def welcome_console_msg(user):
    """
    
    **********BOT ONLINE***********
         Logged in as: FULANO
    Under ID: 456531235446518479879
    *******************************

    """
    # Define data layout
    logged = f"Logged in as: {user.name}"
    id_data = f"Under ID: {user.id}"
    bigger = (len(logged) if len(logged) > len(id_data) else len(id_data)) + 2

    # Define the header 
    header = f"{' BOT ONLINE ':*^{bigger}}"

    # Define the logged_layout based in logged data
    logged_layout = f"{logged:^{bigger}}"

    # Define the id_layout based in id data
    id_layout = f"{id_data:^{bigger}}"

    # Define the Footer
    footer = "*" * bigger

    # Build the message
    msg = f"{header}\n{logged_layout}\n{id_layout}\n{footer}\n"
    return msg


def get_log_say_msg(msg: str):
    msg = " ".join(msg.strip().replace("*", "").splitlines())
    return f"Bot says: {msg}"


def get_log_msg(msg: str):
    return " ".join(msg.strip().replace("*", "").splitlines())


def get_images_path(image_name):
    return f"data/images/{image_name}"


def prettify_key(key: str):
    with switch.Switch(key.lower()) as case:
        if case("pve"):
            return "PvE"
        if case("pvp"):
            return "PvP"
        if case("wvw"):
            return "WvW"
        if case("fractals"):
            return "Fractals"
        if case("special"):
            return "Festival"
        if case.default:
            return False


def dailies_desc(
        dailies: dict, key: str, tomorrow: bool = False, colour: discord.Colour = discord.Colour.dark_magenta()
) -> discord.Embed:

    now = datetime.datetime.now()
    date = now + (datetime.timedelta(days=1) if tomorrow else datetime.timedelta(days=0))
    title = prettify_key(key)
    image = get_images_path("Daily_Achievement.png")
    description = f"{title} Daily Achievements - {date.date()}\n"

    msg = discord.Embed(title=title, timestamp=date, description=description, colour=colour)
    msg.set_thumbnail(url="https://i.imgur.com/oqNgdeP.png")

    for daily in dailies:
        name = f"{daily.name}"
        value = f" - {daily.requirements}\n"
        msg.add_field(name=name, value=value, inline=False)

    return msg

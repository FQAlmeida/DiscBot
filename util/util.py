import datetime

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


def dailies_desc(dailies: dict, tomorrow: False) -> str:
    today = datetime.datetime.now().date()
    if tomorrow:
        today += datetime.timedelta(days=1)
    msg = "```md"

    msg += f"\n# Guild Wars 2 -- Dailies -- {today}\n"
    for key in dailies.keys():
        if not dailies[key]:
            continue
        msg += f"\n## {prettify_key(key)}\n"
        for a in range(len(dailies[key])):
            if key == "pve":
                msg += f"{a}. {dailies[key][a].requirements}\n"
            elif key == "fractals":
                if dailies[key][a].requirements != "" and dailies[key][a].requirements is not None:
                    msg += f"{a}. {dailies[key][a].requirements}\n"
                else:
                    msg += f"{a}. {dailies[key][a].name}\n"
            else:
                msg += f"{a}. {dailies[key][a].name}\n"
    msg += "```"
    print(msg)
    return msg

def welcome_console_msg(user):
    l4 = " BOT ONLINE "
    l1 = f"Logged in as: {user.name}"
    l2 = f"Under ID: {user.id}"
    bigger = len(l1) if len(l1) > len(l2) else len(l2)
    l0 = f"{l4:*^{bigger}}"
    l3 = "*" * bigger
    msg = f"{l0}\n{l1}\n{l2}\n{l3}"
    return msg


def get_log_say_msg(msg: str):
    msg = " ".join(msg.strip().replace("*", "").splitlines())
    return f"Bot says: {msg}"


def get_log_msg(msg: str):
    return " ".join(msg.strip().replace("*", "").splitlines())

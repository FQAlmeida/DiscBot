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


# DiscBot

A development bot for discord

## Features

- Conversion from text to morse (needs a better database)
- Guild Wars 2 api integration (WIP)

## Commands

All the commands have the "?" as prefix

1. test 
   - Just returns a Hello World message for tests porpoises
2. coin
    - A "Flips a Coin" game
3. admin
    - Says if the message's author is a server admin
3. joined
    - Says when the message's author joined the discord/server
5. morse
    - Convert the message content to morse
6. gw2
    - token
        - add
            - Add a Guild Wars 2 access token
        - remove
            - Remove a Guild Wars 2 access token
        - update
            - Update a Guild Wars 2 access token

## Instructions

In the data folder, you should to create a file named **configs.ini**, the file must to have the following pattern:
> [TOKEN]
> - token = your_token_here
>  
> [GW2]
> - my_token = your_gw2_api_access_token_here

## Todo List

1. [x] Create a simple bot
2. [x] Create a morse app
3. [ ] Create a Guild Wars 2 app
    1. [x] Create a token manager
        1. [x] Create a database for keep information about token (token, permissions, discord_owner) 
        2. [x] Create a token validation
        1. [x] Create a add_token command
        2. [x] Create a remove_token command
        3. [x] Create a update_token command
        4. [x] Build some tests
    5. [ ] Create a daily achievements view
        1. [x] Get dailies 
        2. [x] Struct a Achievements class
            > - id
            > - name: achievement's name
            > - description: description of achievement, if it isn't blank
            > -  requirement: tip to complete the achievement 
            > - locked_text: another tip, more specific

        2. [ ] Convert the list of dailies to list of achievements
            - Structs a dictionary like:
                > Dict{key, list(Achievements)}

            - key: ("PvE", "PvP", "WvW", "Fractals, Special")
                - Special is dailies from festival events
            - list(Achievements): A list of parsed dailies achievements to Achievements objects
            
        4. [ ] Create a layout message with data
            ```
            Dailies Achievements - dd/MM/yyyy
            
            -------------- PvE --------------
            1. PvE Achievement 1 name
                - description, if exists
                - requirements 
                - locked_text, if exists
            ...
            n. PvE Achievement n name
                - description, if exists
                - requirements
                - locked_text, if exists
            ---------------------------------
            ...
            ------------ Special ------------ if Exists
            1. Special Achievement 1 name
                - description, if exists
                - requirements 
                - locked_text, if exists
            ...
            n. Special Achievement n name
                - description, if exists
                - requirements
                - locked_text, if exists
            ---------------------------------
            ```
            1. [ ] Setup the layout
            2. [ ] Pass to bay says as a embed message

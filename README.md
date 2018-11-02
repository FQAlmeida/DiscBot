
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
4. joined
    - Say     s when the message's author joined the discord/server
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
    - dailies *Tomorrow
        - Shows all the daily achievements

## Instructions

In the data folder, you should to create a file named **configs.ini**, the file must to have the following pattern:
> [TOKEN]
> - token = your_token_here
>  
> [GW2]
> - my_token = your_gw2_api_access_token_here

## Todo List

1. [ ] Keep all commands documented and logged
2. [ ] Create a status to bot for when he was processing a command
3. [x] Create a simple bot
4. [x] Create a morse app
5. [ ] Create a Guild Wars 2 app
    1. [x] Create a token manager
        1. [x] Create a database for keep information about token (token, permissions, discord_owner)
        2. [x] Create a token validation
        3. [x] Create a add_token command
        4. [x] Create a remove_token command
        5. [x] Create a update_token command
        6. [x] Build some tests
    2. [x] Create a daily achievements view
        1. [x] Get dailies
        2. [x] Build a Achievements class
            > - id
            > - name: achievement's name
            > - description: description of achievement, if it isn't blank
            > - requirement: tip to complete the achievement
            > - locked_text: another tip, more specific

        3. [x] Convert the list of dailies to list of achievements
            - Structs a dictionary like:
                > Dict{key, list(Achievements)}

            - key: ("PvE", "PvP", "WvW", "Fractals", "Special")
                - Special is dailies from festival events
            - list(Achievements): A list of parsed dailies achievements to Achievements objects

        4. [x] Make a tomorrows daily view

        5. [x] Create a layout message with data
            1. [x] Setup the layout
                - Layout will be formed with 5 embed messages, 1 for each element in dict
            2. [x] Pass to bot says as a embed message
                - Bot will say a message for each embed message

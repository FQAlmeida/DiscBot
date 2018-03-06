import discord
import asyncio
import random
admin_ids = {'358652273217372161'}
client = discord.Client()

@client.event
async def on_ready():
    print('BOT ONLINE - Hello World!')
    print(client.user.name)
    print(client.user.id)
    print('-------------------------')

@client.event
async def on_message(message):
    print(message.author.id)
    if message.content.lower().startswith('?test'):
        await client.send_message(message.channel, "Hello Mundo!, Am I alive?")
    elif message.content.lower().startswith('?coin'):
        if random.randint(1, 2) == 1:
            await client.add_reaction(message, '😝')
        else:
            await client.add_reaction(message, '👑')
    elif message.content.lower().startswith('?admin'):
        if admin_ids.__contains__(message.author.id):
            await client.send_message(message.channel, 'You\'re the B.O.S.S')
        else:
            await client.send_message(message.channel, 'You aren\'t the B.O.S.S')

client.run('TOKEN_HERE')
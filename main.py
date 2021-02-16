import discord
import os
import pyjokes
from commands import cmds

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user or not message.content.startswith('$'):
        return

    if message.content.startswith('$help'):
        await message.channel.send('Here\'s a list of the commands:')
        commandHelp = ''
        for cmd in cmds:
            commandHelp += cmd
            commandHelp += '\n'
        await message.channel.send(commandHelp)
    
    if message.content.startswith('$hello'):
        await message.channel.send('Oh hey there :).')
    elif message.content.startswith('$goodbye'):
        await message.channel.send('Cya later ;)')
    elif message.content.startswith('$pyjoke'):
        await message.channel.send(pyjokes.get_joke())
    else:
        await message.channel.send('That doesn\'t seem to be a valid command.\n' +
            'Type $help to see the possible commands for Portra')

client.run("ODEwMTA4NjMxMDU1ODU5NzMy.YCe2dA.Co5uUyPd2AXXBT_i-TOnlZAqSuE")
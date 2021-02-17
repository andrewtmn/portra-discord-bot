import discord
from discord.ext import commands
import logging
import os
import pyjokes
from cmdDescriptions import cmds
from random import randint

# discord.py logging to discord.log file
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# prefix for commands set to '$
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user or not message.content.startswith('$'):
        return

    if message.content.startswith('$help'):
        await helpCommand(message)
        return
   
    if message.content.startswith('$hello'):
        await message.channel.send('Oh hey there :).')
    elif message.content.startswith('$goodbye'):
        await message.channel.send('Cya later ;)')
    elif message.content.startswith('$pyjoke'):
        await message.channel.send(pyjokes.get_joke())
    else:
        await message.channel.send('That doesn\'t seem to be a valid command.\n' +
           'Type $help to see the possible commands for Portra')

    await bot.process_commands(message)

async def helpCommand(message):
    await message.channel.send('Here\'s a list of the commands:\n')
    commandHelp = ''
    for cmd in cmds:
        commandHelp += cmd
        commandHelp += '\n'
    await message.channel.send(commandHelp)

@bot.command()
async def dice(ctx, sides):
    numSides = int(sides)
    die = randint(1, numSides)
    await ctx.send("You rolled {0}".format(die))


bot.run("ODEwMTA4NjMxMDU1ODU5NzMy.YCe2dA.Co5uUyPd2AXXBT_i-TOnlZAqSuE")
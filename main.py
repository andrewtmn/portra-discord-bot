import discord
import os
import logging
import pyjokes
import youtube_dl

from cmdDescriptions import cmds
from random import randint
from discord.ext import commands

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

    await bot.process_commands(message)

async def helpCommand(message):
    await message.channel.send('Here\'s a list of the commands:\n')
    commandHelp = ''
    for cmd in cmds:
        commandHelp += cmd
        commandHelp += '\n'
    await message.channel.send(commandHelp)

@bot.command()
async def hello(ctx):
    await ctx.send("Oh hi there")

@bot.command()
async def goodbye(ctx):
    await ctx.send("See ya later")

@bot.command()
async def pyjoke(ctx):
    await ctx.send(pyjokes.get_joke())

@bot.command()
async def dice(ctx, sides):
    try:
        numSides = int(sides)
        die = randint(1, numSides)
        await ctx.send("You rolled {0}".format(die))
    except:
        await ctx.send("Invalid number of sides. Make sure it's a positive integer")

@bot.command()
async def play(ctx, url : str):
    await removeSongMP3(ctx)

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    
async def removeSongMP3(ctx):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for current audio to end or use $stop command")
        return

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        await voice.disconnect()
    else:
        await ctx.send("Portra isn't connected to a voice channel")

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio is playing at the momement.")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Portra isn't connected to a voice channel.")

bot.run("ODEwMTA4NjMxMDU1ODU5NzMy.YCe2dA.Co5uUyPd2AXXBT_i-TOnlZAqSuE")
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Oh hey there :).')
    elif message.content.startswith('$goodbye'):
        await message.channel.send('Cya later ;)')


client.run('ODEwMTA4NjMxMDU1ODU5NzMy.YCe2dA.ge-fwsnj41RURm3Dsh1jqpXFnEk')
import os
import discord

key = os.environ['BOT_KEY']

client = discord.Client()

@client.event
async def on_ready(): #called when the bot is ready
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('&hello'):
    await message.channel.send('Hello!')

client.run(key)

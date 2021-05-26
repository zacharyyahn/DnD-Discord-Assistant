import os
import discord
import random
import time
from replit import db

key = os.environ['BOT_KEY']

client = discord.Client()

def parse_roll_message(message):
  roll_list = []

  message = message[6:]
  d_location = message.find("d")
  if d_location == -1:
    return ["invalid"]
  
  num_rolls = message[0:d_location]
  dice_value = message[d_location+1:]
  print("Num rolls: " + num_rolls + " Dice value: " + dice_value)

  for i in range(0, int(num_rolls)):
    roll_list.append(random.randint(1, int(dice_value)))

  return roll_list


@client.event
async def on_ready(): #called when the bot is ready
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('!roll'):
    await message.channel.send("Rolling...")

    #Parse the roll
    roll_list = parse_roll_message(message.content)

    #If there is only a string, then there was invalid syntax
    if (type(roll_list[0]) == type(1)):
      time.sleep(2)
      the_sum = sum(roll_list)

      print_string = ""
  
      #Prepare the roll to be printed
      for item in roll_list:
        print_string += str(item) + "  "
      
      #If just one roll, don't print the total
      if (type(roll_list[0] == type(1)) and len(roll_list) == 1):
        await message.channel.send("Your roll: " + print_string)
      
      else: 
        await message.channel.send("Your rolls: " + print_string)
        await message.channel.send("Total: " + str(the_sum))

    else:
      await message.channel.send("Invalid format. (Try 1d20)")
  
  if message.content.startswith("!character"):
    db[message.author] = message.content[11:]
  
  if message.content.startswith("!list_characters"):
    for a_key in db.keys():
      await message.channel.send(a_key[0:-5] + ": " + db[a_key])

  # if message.content.startswith("!nick"):
  #   username = message.author
  #   member = discord.utils.get(message.guild.users, name=username)
  #   for mem in message.guild.users:
  #     await message.channel.send(mem)
  #   await member.edit(nick, db[username[0:-5]])



client.run(key)

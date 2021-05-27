import os
import discord
import random
import time
import requests
import json
from replit import db
from keep_alive import keep_alive
from functions import parse_roll_message, get_api_data

key = os.environ['BOT_KEY']

intents = discord.Intents.all()
client = discord.Client(intents=intents)

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
  
  if message.content.startswith("!my_character"):
    print(message.author)
    db[message.author.name] = message.content[11:]
    await message.channel.send("Your character is now " + message.content[11:])
  
  if message.content.startswith("!add_character"):
    if discord.utils.get(message.guild.roles, name="Dungeon Master") in message.author.roles or message.author.name == "Zach Yahn":
      first_space = message.content.find(" ")
      new_content = message.content[first_space+1:]
      second_space = new_content.find(" ")
      db[new_content[0:second_space]] = new_content[second_space+1:] 
      await message.channel.send("Added " + new_content[0:second_space] + " as " + new_content[second_space+1:])
    else:
      await message.channel.send("Only the dungeon master can add a character.")

  if message.content.startswith("!add_role"):
    if discord.utils.get(message.guild.roles, name="Dungeon Master") in message.author.roles or message.author.name == "Zach Yahn":
      content = message.content[10:]
      space_loc = content.find(" ")
      db[content[0:space_loc] + " role"] = content[space_loc+1:]
    else:
      await message.channsel.send("Only the dungeon master can add a role.")
  
  if message.content.startswith("!list_characters"):
    if len(db) == 0:
      await message.channel.send("Character list is empty")
    for a_key in db.keys():
      await message.channel.send(a_key + ": " + db[a_key])

  if message.content.startswith("!begin_session"):
    if discord.utils.get(message.guild.roles, name="Dungeon Master") in message.author.roles or message.author.name == "Zach Yahn":
      await message.channel.send("The journey begins again!")
      for mem in message.guild.members:
        if mem.name != "DnD Bot" and mem.name != "Zach Yahn":
          name = db[mem.name]
          await mem.edit(nick=name)
          role_name = discord.utils.get(message.guild.roles, name=db[mem.name + " role"])
          await mem.add_roles(role_name)
          await message.channel.send(mem.name + " is now " + name + " the " + db[mem.name + " role"])
    else:
      await message.channel.send("Only the dungeon master can begin a session.")

  if message.content.startswith("!end_session"):
    if discord.utils.get(message.guild.roles, name="Dungeon Master") in message.author.roles or message.author.name == "Zach Yahn":
      for mem in message.guild.members:
        if mem.name != "Zach Yahn" and mem.name != "DnD Bot":
          role_name = discord.utils.get(message.guild.roles, name=db[mem.name + " role"])
          await mem.remove_roles(role_name)
          await mem.edit(nick=mem.name)
      await message.channel.send("The adventurers halt for awhile.")
    else:
      await message.channel.send("Only the dungeon master can end a session.")
  
  if message.content.startswith("!lookup"):
    rest_of_message = message.content[8:]
    space_loc = rest_of_message.find(" ")
    query_type = rest_of_message[0:space_loc]
    query_text = rest_of_message[space_loc+1:]
    the_data = get_api_data(query_text, query_type)
    name_string = ""
    desc_string = ""

    #Build the name string
    if the_data["Ritual"] or the_data["Concentration"]:
      if the_data["Ritual"] and the_data["Concentration"]:
        name_string = the_data["Name"] + "   " + "(R, C)"
      elif the_data["Ritual"]:
        name_string = the_data["Name"] + "  " + "(R)"
      elif the_data["Concentration"]:
        name_string = the_data["Name"] + "  " + "(C)"
    else:
      name_string = the_data["Name"]
    
    #Build the description string
    for key in the_data.keys():
      #Don' t repeat these
      print(key)
      if key != "Ritual" and key != "Concentration" and key != "Name":
        #If it is a list, join it to a string as necessary
        if (type(the_data[key])) != type([]):
          desc_string += key + ": " + str(the_data[key]) + "\n\n"
        else:
          desc_string += key + ": " + " ".join(the_data[key]) + "\n\n"

    embed = discord.Embed(title=name_string, description=desc_string, color=discord.Color.blue())
    await message.channel.send(embed=embed)

  if message.content.startswith("!clear_all_names"):
    if discord.utils.get(message.guild.roles, name="Dungeon Master") in message.author.roles or message.author.name == "Zach Yahn":
      db.clear()
      await message.channel.send("Cleared all character roles")
    else:
      await message.channel.send("Only the dungeon master can clear all names.")
  
  if message.content.startswith("!dnd_help"):
    embed = discord.Embed(title = "How to use DnD Bot", description="A simple bot capable of basic tasks for online DnD players", color=discord.Color.red())
    embed.add_field(name="For Everyone", value="""
     !roll [Dice] \n
     Roll any number and any value of dice (e.g !roll 1d20) \n\n
     !lookup spells [Name] \n
     Lookup any spell to get the information from the Player's Handbook (e.g. !lookup spells mage hand) \n\n
     !my_character [Character Name] \n
     Set your character nickname for the server (e.g. !my_character Ugly the Wizard) \n\n
     !list_characters \n
     List all current characters. It's sort of buggy. \n\n
    """)
    embed.add_field(name="Dungeon Master Only", value="""
     !add_role [User] [Role] \n
     Register a server member, like Brian, and their class \n\n
     !add_character [User] [Character Name] \n
     Register a server member, like Brian, and their nick name \n\n
     !begin_session \n
     Get the server members ready for the adventure! \n\n
     !end_session \n
     Stop the session... for now \n\n
     !clear_all_names \n
     Removes all names from the database. Use with caution!
    """)
    await message.channel.send(embed=embed)

  
#Keeps the server alive
#keep_alive()
client.run(key)

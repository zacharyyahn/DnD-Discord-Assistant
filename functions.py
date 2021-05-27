import random
import requests
import json
from replit import db

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

def get_api_data(thing, query_type):
  return_data = {}
  complete_string = thing.lower().split(" ")
  complete_string = "-".join(complete_string)
  response = requests.get("http://www.dnd5eapi.co/api/"+ query_type + "/" + complete_string)
  json_data = json.loads(response.text)
  print(json_data)
  
  if query_type == "spells":
    return_data["Ritual"] = json_data["ritual"]
    return_data["Concentration"] = json_data["concentration"]
    return_data["Name"] = json_data["name"]
    return_data["Description"] = json_data["desc"]
    try:
      return_data["Higher Level"] = json_data["higher_level"]
    except:
      pass
    return_data["Range"] = json_data["range"]
    return_data["Duration"] = json_data["duration"]
    return_data["Casting Time"] = json_data["casting_time"]
    return_data["Level"] = json_data["level"]
  
  return return_data


    

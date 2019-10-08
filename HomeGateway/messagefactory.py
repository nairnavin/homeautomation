import json

class MessageFactory:

  def create_empty_message():
    message = None
    with open('messageformat.json') as jsonFile:
      message = json.load(jsonFile)
    return message  

  def create_message(name, device_type, state, value):
    message = None
    with open('messageformat.json') as jsonFile:
      message = json.load(jsonFile)
      message["deviceInfo"]["name"] = name
      message["deviceInfo"]["type"] = device_type
      message["deviceState"]["status"] = state
      message["deviceState"]["value"] = value
    return message  

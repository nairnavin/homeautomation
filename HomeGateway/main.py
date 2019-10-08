from battery import Battery
from smartmeter import SmartMeter
from smartlight import SmartLight
import time
import paho.mqtt.client as mqtt
import json

BROKER_ADDRESS = '85.119.83.194' #test.mosquitto.org
home_assets = []

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Connected to broker")
    for asset in home_assets:
      if asset.is_controllable():
        client.subscribe(asset.get_subscribe_topic())      
  else:
    print("Connection failed")

def on_message(client, userdata, message):
  print("message received  ",str(message.payload.decode("utf-8")),\
        "topic",message.topic,"retained ",message.retain)
  
def init_assets():
  battery1 = Battery(soc=30, simulationSeconds=60, state=Battery.State.IDLE)
  battery1.setName('Battery 1')
  battery1.set_state(Battery.State.DISCHARGING)
  sm1 = SmartMeter('Electricity')
  light1 = SmartLight('Living Room Main Light')
  home_assets.append(battery1)
  home_assets.append(sm1)
  home_assets.append(light1)

  for asset in home_assets:
    asset.start()


# Run following code when the program starts
if __name__ == '__main__':
  init_assets()
  client = mqtt.Client("gateway1") #create new instance
  client.connect(BROKER_ADDRESS) #connect to broker
  client.on_message = on_message
  client.on_connect = on_connect
  client.loop_start()
  
  while(True):

    for asset in home_assets:
      print(asset.to_string())
      client.publish(asset.get_publish_topic(), str(json.dumps(asset.get_message_json()))) #publish
    time.sleep(5)

  sm1.join()
  battery1.join()
  light1.join()
  print('Main Terminating...')

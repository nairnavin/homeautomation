import paho.mqtt.client as mqtt
import json
from influxdal import InfluxDAL

BROKER_ADDRESS = '85.119.83.194'

# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    if rc == 0:
      print("Connected to broker")   
      client.subscribe('premise/#')   
    else:
      print("Connection failed")

def convert_to_influx_battery_format(inputjson):
  payloadjson = json.loads(inputjson)
  influxjson = None
  with open('influxformat.json') as jsonFile:
    influxjson = json.load(jsonFile)
    influxjson[0]['measurement'] = 'Battery'
    influxjson[0]['tags']['customerid'] = '1'
    influxjson[0]['fields']['soc'] = payloadjson['deviceState']['value']
    influxjson[0]['fields']['status'] = payloadjson['deviceState']['status']
  return influxjson


def convert_to_influx_smartmeter_format(inputjson):
  payloadjson = json.loads(inputjson)
  influxjson = None
  with open('influxformat.json') as jsonFile:
    influxjson = json.load(jsonFile)
    influxjson[0]['measurement'] = 'SmartMeter'
    influxjson[0]['tags']['customerid'] = '1'
    influxjson[0]['fields']['value'] = payloadjson['deviceState']['value']
  return influxjson

def convert_to_influx_smartlight_format(inputjson):
  payloadjson = json.loads(inputjson)
  influxjson = None
  with open('influxformat.json') as jsonFile:
    influxjson = json.load(jsonFile)
    influxjson[0]['measurement'] = 'SmartLight'
    influxjson[0]['tags']['customerid'] = '1'
    influxjson[0]['fields']['state'] = payloadjson['deviceState']['status']
  return influxjson

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  if msg.topic == 'premise/battery/h2c':
    InfluxDAL().save_data(convert_to_influx_battery_format(msg.payload))
  elif msg.topic == 'premise/smartmeter/h2c':
    InfluxDAL().save_data(convert_to_influx_smartmeter_format(msg.payload))
  elif msg.topic == 'premise/smartlight/h2c':
    InfluxDAL().save_data(convert_to_influx_smartlight_format(msg.payload))

client = mqtt.Client('Server')
print("Trying connection ... ")
client.connect(BROKER_ADDRESS)
client.on_connect = on_connect
client.on_message = on_message
print("Done")
client.loop_forever()
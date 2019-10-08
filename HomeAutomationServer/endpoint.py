from battery import Battery
from smartmeter import SmartMeter
from smartlight import SmartLight
from flask import Flask
import time
import paho.mqtt.client as mqtt
import json

# Flask end points
app = Flask(__name__)

broker_address = '85.119.83.194' #test.mosquitto.org

def getMessageStructure(name, deviceType, state, value):
  message = {}
  with open('messageformat.json') as jsonFile:
    message = json.load(jsonFile)
    message["deviceInfo"]["name"] = name
    message["deviceInfo"]["type"] = deviceType
    message["deviceState"]["status"] = state
    message["deviceState"]["value"] = value
  return message

@app.route("/battery/")
def batteryValue():
    return str(battery1.currentSOC())

@app.route("/battery/charge")
def chargeBattery():
    # Start running the threads!
    battery1.setState(Battery.Status.CHARGING)
    battery1.start()
    return str(battery1.currentSOC())

@app.route("/battery/discharge")
def dischargeBattery():
    # Start running the threads!
    battery1.setState(Battery.Status.DISCHARGING)
    battery1.start()
    return str(battery1.currentSOC())

@app.route("/battery/stop")
def stopBattery():
    # Start running the threads!
    battery1.setState(Battery.Status.IDLE)
    battery1.start()
    return str(battery1.currentSOC())    

# Run following code when the program starts
if __name__ == '__main__':
  battery1 = Battery(soc=30, simulationSeconds=60, state=Battery.State.IDLE)
  battery1.setName('Battery 1')
  #battery2 = Battery(soc=50, simulationSeconds=120, state=Battery.State.IDLE)
  #battery2.setName('Battery 2')
  sm1 = SmartMeter('Electricity')
  battery1.setState(Battery.State.DISCHARGING)
  #battery2.setState(Battery.State.CHARGING)
  light1 = SmartLight('Living Room Main Light')
  sm1.start()
  battery1.start()
  #battery2.start()
  client = mqtt.Client("gateway1") #create new instance
  client.connect(broker_address) #connect to broker


  while(True):
    
    print('SmartMeter: ' + str(sm1.currentConsumption()) + ' ' + str(sm1.totalConsumption()))
    print('Battery 1: ' + str(battery1.currentSOC()))
    #print('Battery 2: ' + str(battery2.currentSOC()))
    print('Smart Light: ' + light1.name + ' ' + str(light1.state))
    

    battery1Msg = getMessageStructure('Battery 1', 'Battery Inverter', str(battery1.getState()), battery1.currentSOC())
    #battery2Msg = getMessageStructure('Battery 2', 'Battery Inverter', str(battery2.getState()), battery2.currentSOC())
    light1.setState(SmartLight.State.ON if light1.getState() == SmartLight.State.OFF else SmartLight.State.OFF)
    lightMsg = getMessageStructure('Living Room Smart Light', 'Smart Light', "ON" if light1.getState() == SmartLight.State.ON else "OFF", '')
    smartmeterMsg = getMessageStructure('Electricity', 'Smart Meter', '', '{ "current" : ' + str(sm1.currentConsumption()) + ', "total" : ' + str(sm1.totalConsumption()) + '}')
    client.publish("premise/smart-light/living-room", str(json.dumps(lightMsg))) #publish
    client.publish("premise/battery", str(json.dumps(battery1Msg))) #publish
    #client.publish("premise/battery/2", str(json.dumps(battery2Msg))) #publish
    client.publish("premise/smart-meter", str(json.dumps(smartmeterMsg)))
    time.sleep(5)
  #app.run(host='0.0.0.0')
  sm1.join()
  battery1.join()
  #battery2.join()
  print('Main Terminating...')

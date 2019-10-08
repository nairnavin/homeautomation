from asset import Asset
import random
import datetime as dt
import time
from messagefactory import MessageFactory

'''
SmartMeter class to simulate a utility smart meter. It is a simple simulator that generates a set of 
random values to simulate consumption for power, water, gas etc
The class has some simple logic to generate values based on time of day.
'''
class SmartMeter(Asset):

  PUBLISH_TOPIC = 'premise/smartmeter/h2c'
  SUBSCRIBE_TOPIC = 'premise/smartmeter/c2h'

  ''' Constructor. '''
  def __init__(self, utility, peak = [25/10000, 30/10000], offpeak = [10/10000, 15/10000], sleep = 5):

    super().__init__()
    self._utility = utility
    self._sleep = sleep
    self._total_consumption = 0
    self._consumption = 0
    self._peak = peak
    self._offpeak = offpeak
    super().set_publish_topic(self.PUBLISH_TOPIC)
    super().set_subscribe_topic(self.SUBSCRIBE_TOPIC)
    super().set_controllable(False)

  # Run the thread
  def run(self):
    while(True):
      hour = dt.datetime.today().hour;
      #print(hour)
      if hour >= 6 & hour < 8:
        self._consumption = random.uniform(self._peak[0], self._peak[1])
      elif hour >= 8 & hour < 18:
        self._consumption = random.uniform(self._offpeak[0], self._offpeak[1])  
      elif hour >= 18 & hour < 21:
        self._consumption = random.uniform(self._peak[0], self._peak[1])
      elif hour >= 21 & hour < 24:
        self._consumption = random.uniform(self._offpeak[0], self._offpeak[1]) 
      elif hour >= 0 & hour < 6:
        self._consumption = random.uniform(self._offpeak[0], self._offpeak[1])
      self._total_consumption += self._consumption
      time.sleep(self._sleep) 

  def currentConsumption(self):
    return self._consumption

  def totalConsumption(self):
    return self._total_consumption

  def get_message_json(self):
    return MessageFactory.create_message('Electricity', 'Smart Meter', \
      '', '{ "current" : ' + str(self.currentConsumption()) + ', "total" : ' + str(self._total_consumption()) + '}')

  def to_string(self):
    return 'SmartMeter: ' + str(self.currentConsumption()) + ' ' + str(self._total_consumption())
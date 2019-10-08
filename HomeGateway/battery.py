import time
from enum import Enum
from asset import Asset
from messagefactory import MessageFactory

'''
Battery class to simulate a battery charging/discharing cycle. It is not designed to be an accurate model, in 
fact it is a simple linear charge/discharge model, so to be used only to demo battery functionality but not a 
replacement for an actual battery by any means
'''
class Battery(Asset):

  PUBLISH_TOPIC = 'premise/battery/h2c'
  SUBSCRIBE_TOPIC = 'premise/battery/c2h'
  '''
  Enum to hold constants related to battery status
  '''
  class State(Enum):
    IDLE = 1
    CHARGING = 2
    DISCHARGING = 3

  ''' Constructor. '''
  def __init__(self, soc, simulationSeconds, state, sleep=5):

    super().__init__()
    super().set_publish_topic(self.PUBLISH_TOPIC)
    super().set_subscribe_topic(self.SUBSCRIBE_TOPIC)
    super().set_controllable(True)
    self._simulation_secs = simulationSeconds
    self.set_state(state)
    self._soc = soc
    self._sleep = sleep

  # Run the thread
  def run(self):
    sim_secs = 0
    while self._soc != 0 and self._soc != 100 and self._state != self.State.IDLE and sim_secs < self._simulation_secs:
        self._soc = self._soc + self._rate 
        if self._soc < 0:
            self._soc = 0
        elif self._soc > 100:
            self._soc = 100
        sim_secs += 5
        time.sleep(self._sleep)
  
  # Set battery to idle
  def set_state(self, state):
    super().set_state(state)
    if self._state == self.State.IDLE:
        self._rate = 0
    elif self._state == self.State.DISCHARGING:
        self._rate = -self._soc * 5 / self._simulation_secs
    elif self._state == self.State.CHARGING:
        self._rate = (100 - self._soc) * 5 / self._simulation_secs

  # Return current battery SOC value
  def soc(self):
    return self._soc

  def get_message_json(self):
    return MessageFactory.create_message('Battery 1', 'Battery Inverter', \
      str(self.get_state()), self.soc())

  def to_string(self):
    return 'Battery 1: ' + str(self.soc())

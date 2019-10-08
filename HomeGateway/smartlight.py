from enum import Enum
from asset import Asset
from messagefactory import MessageFactory

class SmartLight(Asset):

  PUBLISH_TOPIC = 'premise/smartlight/h2c'
  SUBSCRIBE_TOPIC = 'premise/smartlight/c2h'

  class State(Enum):
    OFF = 0
    ON = 1

  def __init__(self, name, state = State.OFF):
    super().__init__()
    super().set_state(state)
    self._name = name
    super().set_publish_topic(self.PUBLISH_TOPIC)
    super().set_subscribe_topic(self.SUBSCRIBE_TOPIC)
    super().set_controllable(True)

  def get_message_json(self):
    return MessageFactory.create_message('Living Room Smart Light', 'Smart Light', \
          "ON" if self.get_state() == SmartLight.State.ON else "OFF", '')

  def to_string(self):
    return 'Smart Light: ' + self._name + ' ' + str(self.get_state())
from threading import Thread

class Asset(Thread):

  def __init__(self):
    super().__init__()

  def is_controllable(self):
    return self._controllable

  def set_controllable(self, is_controllable):
    self._controllable = is_controllable

  def set_state(self, status):
    self._state = status

  def get_state(self):
    return self._state

  def set_value(self, value):
    self._value = value

  def get_value(self):
    return self._value

  def get_publish_topic(self):
    return self._publish_topic

  def set_publish_topic(self, topic):
    self._publish_topic = topic

  def get_subscribe_topic(self):
    return self._subscribe_topic

  def set_subscribe_topic(self, topic):
    self._subscribe_topic = topic

  def get_message_json(self):
    return "{}"

  def to_string(self):
    return ""

  def run(self):
    pass
from influxdb import InfluxDBClient

class InfluxDAL:
  INFLUXDB_ADDRESS = '0.tcp.ngrok.io'
  INFLUXDB_USER = 'root'
  INFLUXDB_PASSWORD = 'root'
  INFLUXDB_DATABASE = 'DeviceDataDB'
  INFLUXDB_PORT = 13994
  influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

  def __init__(self):
    databases = self.influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == self.INFLUXDB_DATABASE, databases))) == 0:
        self.influxdb_client.create_database(self.INFLUXDB_DATABASE)
    self.influxdb_client.switch_database(self.INFLUXDB_DATABASE)

  def save_data(self, json_body):
    self.influxdb_client.write_points(json_body)
import Adafruit_DHT
import State

def Probe_Humidity_Temperature():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    State.HUMIDITY = humidity # Update the program state
    State.TEMPERATURE = temperature # Update the program state
    return

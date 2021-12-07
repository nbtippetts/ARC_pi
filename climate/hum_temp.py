import Adafruit_DHT
#add math function for VPD calculation
import math
def get_humidity_temperature():
	sensor = Adafruit_DHT.DHT22
	pin =4
	new_humidity = 0.0
	new_temperature = 0.0
	break_loop = True;
	while break_loop:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			vpd=((6.1078*math.exp(17.08085*temperature/(234.175+temperature)))-(6.1078*math.exp(17.08085*temperature/(234.175+temperature))*(humidity/100)))/10.
			humidity = int(humidity)
			new_humidity = humidity
			fahrenheit = (temperature * 9/5) + 32
			new_temperature = int(fahrenheit)
			break_loop=False
		else:
			print('Failed to retrieve data from humidity sensor.')
			continue
	print(new_humidity,new_temperature,vpd)
	return new_humidity, new_temperature, vpd
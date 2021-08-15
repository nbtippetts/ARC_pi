import Adafruit_DHT
def get_humidity_temperature():
	sensor = Adafruit_DHT.DHT22
	pin =4
	new_humidity = 0.0
	new_temperature = 0.0
	for i in range(2):
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			humidity = int(humidity)
			new_humidity = humidity
			fahrenheit = (temperature * 9/5) + 32
			new_temperature = int(fahrenheit)
			break
		else:
			print('Failed to retrieve data from humidity sensor.')
			continue
	print(new_humidity,new_temperature)
	return new_humidity, new_temperature
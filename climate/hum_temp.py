import time
import board
import adafruit_scd4x
#add math function for VPD calculation
import math

from gpiozero import exc
from .models import ClimateData
def read_sensor_data():
	humidity = 0.0
	co2 = 0.0
	vpd = 0.0
	temperature = 0.0
	save_data = 0

	i2c = board.I2C()
	scd4x = adafruit_scd4x.SCD4X(i2c)
	print("Serial number:", [hex(i) for i in scd4x.serial_number])

	scd4x.start_low_periodic_measurement()
	print("Waiting for first measurement....")

	while True:
		try:
			if scd4x.data_ready:
				co2 = scd4x.CO2
				humidity = scd4x.relative_humidity
				vpd=((6.1078*math.exp(17.08085*temperature/(234.175+temperature)))-(6.1078*math.exp(17.08085*temperature/(234.175+temperature))*(humidity/100)))/10.
				temperature = scd4x.temperature
				fahrenheit = (temperature * 9/5) + 32
				print(int(humidity), int(fahrenheit), round(vpd,2), co2)
				# if save_data >= 0:
				try:
					climate_data=ClimateData.objects.first()
					climate_data.humidity=humidity
					climate_data.temp=fahrenheit
					climate_data.vpd=vpd
					climate_data.co2=co2
					climate_data.save()
					print('data has been inserted successfully.')
				except Exception as e:
					climate_data=ClimateData()
					climate_data.humidity=humidity
					climate_data.temp=fahrenheit
					climate_data.vpd=vpd
					climate_data.co2=co2
					climate_data.save()
					print('data has been inserted successfully.')
					# save_data=0
				# save_data+=1
			time.sleep(5)
			# print('loop')
		except Exception as e:
			pass
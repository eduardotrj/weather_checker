import requests, json
from pprint import pprint
from datetime import datetime

k = 273.15		# Kº to celcius.

def main():
	answer = True
	print('Enter the name of the city where you want to check the weather.')

	while answer:
		city= input("\nEnter a city: ")
		check_weather(city)
		answer = False
		message = input("Do you want to check another city?: ")

		# valid options:
		if message == 'yes' or \
		message == 'si' or \
		message == 's' or \
		message == 'y' or \
		message == 'true' or \
		message == 'please' or \
		message == 'another': 
			answer = True

def recommendation_momment(t,weather,wind):
	wind=wind*3.6  	# To use as km/h.
	iswindy = False
	raining = False
	drizzling = False
	snowing = False
	sunny = False
	cloudy = False
	dusty = False
	isdanger = False
	temperature = int
	resp = str
	if_drive = '. Warning in case of driving '

	#___________________ TRANSLATE DATA ________________
	if wind>20: iswindy = True 		# 20km/h

	if t <273: temperature=1 		# Temperature under 0º
	elif t<285: temperature=2       # Temperature 0-12º
	elif t<293: temperature=3       # Temperature 12-20º
	elif t<298: temperature=4       # Temperature 20-25º
	elif t<309: temperature=5       # Temperature 25-34º
	else: temperature=6       # Temperature over 34º

	# List of all conditions from API
	# https://openweathermap.org/weather-conditions
	if weather == 781 or weather == 221 or wind>60: isdanger = True # like tornado
	elif weather > 500 and weather < 600: raining = True
	elif weather > 300 and weather < 400: drizzling = True
	elif weather > 600 and weather < 700: snowing = True
	elif weather == 751 or weather == 761 or weather == 731: dusty = True 
	elif weather == 800 or weather == 801: sunny = True 
	else: cloudy = True
	#___________________ RESOLVING ________________

	if isdanger:
		resp = 'not to go out'
	elif temperature == 1 or temperature == 2 and iswindy:
		resp = 'to dress too warmly'
	elif temperature == 2 or temperature == 3 and iswindy:
		resp = 'to dress warmly'
	elif temperature == 3 or temperature == 4 and iswindy:
		resp = 'to wear a light coat'
	elif temperature >= 5 and sunny:
		resp = 'to wear a light and shelter from the sun'
	else:
		resp = 'to wear summer clothing'

	if raining and iswindy and temperature<3:
		resp = resp + ' with watherproof'
	elif raining and iswindy:
		resp = resp + ' with hooded mackintosh'
	elif raining:
		resp = resp + ' with umbrella'
	elif drizzling or snowing:
		resp = resp + ' with hat'

	if dusty:
		resp = resp + ' and glasses for dust'
	elif sunny:
		resp = resp + ' and sunglasses if is daytime'
	#___________________ DRIVING WARNING ________________
	# In case

	if weather >= 503 and weather < 600:
		resp = resp + if_drive + 'due strong raining'
	elif weather >= 600 and weather < 700:
		resp = resp + if_drive + 'due snow on the road'
	elif weather >= 700 and weather < 770:
		resp = resp + if_drive + 'due bad visibility on the road'

	return ('\nIt is recommended ' + resp + '.' )


def check_weather(city):
	# API description:
	# https://openweathermap.org/current
	API_Key = '1a61a5688998a517c45fda29a4ed7200'
	base_url = "http://api.openweathermap.org/data/2.5/weather?appid="+API_Key+"&q="+city
	weather_data = requests.get(base_url).json()

	weather_now = weather_data['weather'][0]['description']
	weather_code = weather_data['weather'][0]['id']
	temperature = weather_data['main']['temp']
	temperature_max = weather_data['main']['temp_max']
	temperature_min = weather_data['main']['temp_min']
	humidity = weather_data['main']['humidity']
	sunrise = datetime.utcfromtimestamp(weather_data['sys']['sunrise'])
	sunset = datetime.utcfromtimestamp(weather_data['sys']['sunset'])
	windspeed = weather_data['wind']['speed']

	print(f'\nThe weather in {city.capitalize()} is {weather_now} \n'
		f'The current temperature is: {temperature-k:.2f}Cº \n'
		f'With a min and max of: {temperature_min-k:.2f} - {temperature_max-k:.2f}Cº \n'
		f'Sunrise time: {sunrise.strftime("%X")}\n'
		f'Sunset time: {sunset.strftime("%X")}\n'
		f'Humity: {humidity}%\n'
		f'Wind speed: {windspeed*3.6:.2f}km/h'
		)

	print(recommendation_momment(temperature,weather_code,windspeed))
	print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n")

main()
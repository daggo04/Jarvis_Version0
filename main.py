import boto3
import datetime
import random
from pyowm.owm import OWM
from pyowm.utils import timestamps
from data import *
#setting up Open Weather Map dependencies
owm = OWM(OWM_Key)
mgr = owm.weather_manager()
weather = mgr.weather_at_place('Bergen,NO').weather
#Finding temperatures for Bergen
temp_dict_celsius = weather.temperature('celsius') 
#Requesting weather report in 3h intervals for the next 5 days
h3_forecaster = mgr.forecast_at_coords(60.39, 5.32, "3h")
#Getting timestamps for the next 3 hours
next3h = timestamps.next_three_hours()
#Checking if it will rain in the next 3 hours
rain = h3_forecaster.will_be_rainy_at(next3h)
#Composing message
intro_msg = "God Morgen! Din " + random.choice(kos_msg) + "."
max_temp_msg = "Max temp i dag er: " + str(temp_dict_celsius["temp_max"])
min_temp_msg = "Min temp i dag er: " + str(temp_dict_celsius["temp_min"])
if rain == True:
	rain_msg = "Ta med paraply!"
else:
	rain_msg = "La paraplyen stå :)" 
message = intro_msg + "\n" + max_temp_msg + "\n" + min_temp_msg + "\n" + rain_msg
#Sending message to recipients
client = boto3.client("sns")
for recipient in tlf_nr:
	client.publish(PhoneNumber=recipient, Message=message)


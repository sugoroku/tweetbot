#! /home/pi/.pyenv/shims/python
#! _*_ coding: utf-8 _*_

import pywapi
import pprint
import twython
import datetime
import time
import os

CONSUMER_KEY    = os.environ['TW_SUNRIZE_C_KEY']
CONSUMER_SECRET = os.environ['TW_SUNRIZE_C_SECRET']
ACCESS_KEY      = os.environ['TW_SUNRIZE_A_KEY']
ACCESS_SECRET   = os.environ['TW_SUNRIZE_A_SECRET']
api = twython.Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

result = pywapi.get_weather_from_weather_com('JAXX0085')
pp = pprint.PrettyPrinter(indent=4)

#print("sunrise: "+ result['forecasts'][0]['sunrise'])
#print("weather: "+ result['forecasts'][0]['day']['brief_text'])
#print("high temp: "+ result['forecasts'][0]['high'])

sunrise = result['forecasts'][1]['sunrise']
brief_text = result['forecasts'][1]['day']['brief_text']
high_temp = result['forecasts'][1]['high']
chance_precip = result['forecasts'][1]['day']['chance_precip']

if brief_text == 'Sunny' or brief_text == 'Clear' or brief_text == 'M Sunny' or brief_text == 'M Clear' or brief_text == 'Sunny/Wind' or brief_text == 'M Sunny/Wind' or brief_text == 'M Sun/Wind':
  weather = "晴れ"
elif brief_text == 'P Cloudy' or brief_text == 'P Cldy/Wind':
  weather = "晴れ時々曇り"
elif brief_text == 'Clear Late':
  weather = "曇りのち晴れ"
elif brief_text == 'M Cloudy' or brief_text == 'Cloudy' or brief_text == 'Cloudy/Wind' or brief_text == 'M Cldy/Wind' or brief_text == 'AM Clouds':
  weather = "曇り"
elif brief_text == 'Rain' or brief_text == 'Rain Early' or brief_text == 'Showers' or brief_text == 'Rain/Wind' or brief_text == 'Showers/Wind' or brief_text == 'Few Showers':
  weather = "雨"
elif brief_text == 'PM Showers' or brief_text == 'PM Rain':
  weather = "午後に雨"
elif brief_text == 'AM Showers' or brief_text == 'AM Rain/Wind' or brief_text == 'AM Lgt Rain' or brief_text == 'AM Rain':
  weather = "午前に雨"
elif brief_text == 'PM T-Storms':
  weather = "午後に強風を伴う雨"
elif brief_text == 'Rain/Thunder' or brief_text == 'Sct T-Storms' or brief_text == 'T-Storms':
  weather = "雷雨"
else:
  weather = brief_text

tweet = "おはようございます\nまもなく陽が昇ります\n本日の天気は" + weather +"\n最高気温は" + high_temp + "℃\n降水確率は" + chance_precip + "%\n今日も良い日でありますように\nhttps://weather.com/ja-JP/weather/today/l/JAXX0085:1:JA"

now = datetime.datetime.now()

print("SunriseApp start")
print(now)

d_hour = int(sunrise[0:1],10) - now.hour
if d_hour < 0:
  d_hour += 24

d_minute = int(sunrise[2:4],10) - now.minute

d_sec = d_hour*3600 + d_minute*60

print(d_sec)
time.sleep(d_sec)

pp.pprint(result)

api.update_status(status=tweet)
print("SunriseApp end")


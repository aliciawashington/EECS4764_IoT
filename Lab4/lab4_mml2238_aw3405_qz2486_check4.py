import network
import urequests
import ujson
from machine import I2C, SPI
import ssd1306
import math

i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5), freq=100000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('Columbia University', '')
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig()[0])
#print('network config:', wlan.ifconfig()[0])

# IP address to test
ip_address = wlan.ifconfig()[0]

# URL to send the request to
request_url = 'http://ip-api.com/json/' + ip_address + '?fields=lat,lon'
# Send request and decode the result
response = urequests.get(request_url)
result = response.content.decode()
# Clean the returned string so it just contains the dictionary data for the IP address
#result = result.split("(")[1].strip(")")
# Convert this data into a dictio
result  = ujson.loads(result)
lat = result.get('lat')
lon = result.get('lon')
print('Lat: ' + str(lat) + ' Lon: ' + str(lon) )

weather_url = 'https://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid=136c185d9a95a599ec92c9f94bd7ab5b'
weather_call = urequests.get(weather_url)
weather = weather_call.content.decode()
weather = ujson.loads(weather)
#print(weather.split("main"[1]))
#main = weather.get("weather")
description = weather.get('weather')[0].get('description')
temp = weather.get('main').get('temp')
tempstr = 'Temp: ' + str(round(temp,1)-273) + ' C'
print(tempstr)
print(description)
#print(weather)

# display.text(description, 0, 0, 1)    
# display.text(tempstr, 0, 10, 1)
display.text('Lat: ' +str(lat), 0, 00, 1)    
display.text('Lon: ' +str(lon), 0, 10, 1)  

display.show()
display.fill(0)


tweet = 'Latitude:' + str(lat) + '.Longitude:' + str(lon)  + 'The weather is' + description +' and ' + str(temp) +'C.'
#api_key = G4goB9wJ8uaQwu9JT5Ex0JVP7
#tweet_url = 'https://api.thingspeak.com/update.json?api_key=I2WVL8NZO28SRZ6X&tweet=lon:43'
tweet = tweet.replace(" ", "+")
print(tweet)
tweet_url =	'https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key=I2WVL8NZO28SRZ6X&status='+tweet
tweet_call = urequests.post(tweet_url)
print(tweet_call.json)



 #print(typeof(result))

import network
import urequests as requests
import esp
import gc
import ubinascii
from time import sleep
from random import random
from config import SSID, PASSWORD
from send_data import data_post

esp.osdebug(None)
gc.collect()
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

while not station.isconnected():
    pass

print("Connection successful")
print(station.ifconfig())

def getmac():
    mac_addr = station.config('mac')
    mac_addr_str = ubinascii.hexlify(mac_addr,':').decode()
    return mac_addr_str

while True:
    # Generate a random number for data value
    dummy_data = round(random()*100, 3)
    data = dummy_data
    #This field option represents the type of data reading
    field = '1'
    # Post Data point to Database
    try:
        data_post(field, data)
        print(f"Data Sent\nField (Data Type):{field}\tData:{data}\n")
    except:
        pass
    time.sleep(15)

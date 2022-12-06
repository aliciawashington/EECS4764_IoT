import network
import esp
import gc
import ubinascii

esp.osdebug(None)
gc.collect()


ssid ='Verizon_JSVC7Z' #'Columbia University'
password = 'noisy6-hist-pod'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

print("Connection successful")
print(station.ifconfig())

mac_addr = station.config('mac')
mac_addr_str = ubinascii.hexlify(mac_addr).decode()
print(mac_addr_str)
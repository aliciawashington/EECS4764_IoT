from machine import RTC, Pin, PWM, I2C, ADC, SPI
import time
import ssd1306
import network
import esp
import gc
import socket
import urequests
import ujson

esp.osdebug(None)
gc.collect()


ssid = 'Verizon_JSVC7Z' #'Columbia University' 
password = 'noisy6-hist-pod'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

print("Connection successful")
print(station.ifconfig())



hspi = SPI(1, baudrate=1500000, polarity=1, phase=1)
cs = Pin(15, Pin.OUT)
rtc = machine.RTC()
i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5), freq=100000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Setup the Accelerometer
cs.value(1)
time.sleep_ms(50)
cs.value(0)
hspi.write(b'\x31\x07')
cs.value(1)
time.sleep_ms(50)
cs.value(0)
hspi.write(b'\x2d\x08')
cs.value(1)
time.sleep_ms(50)
cs.value(0)
hspi.write(b'\x2c\x0a')
cs.value(1)
time.sleep_ms(50)
cs.value(0)
hspi.write(b'\x2e\x00')
cs.value(1)
time.sleep_ms(50)
cs.value(0)
hspi.write(b'\x38\x00')
cs.value(1)

x_pos = 0
y_pos = 0   

def postAcc(date, x_pos, y_pos):
    post_data = ujson.dumps({"date": date, "X": x_pos, "Y": y_pos})
    url = "http://3.90.5.246:5000"
    res = urequests.post(url, data=post_data)
    
    print(res.text)
    print(f'Response: {res}')

while True:
    cs.value(0)
    buf = bytearray(5)
    hspi.readinto(buf, 0xF2)
    cs.value(1)
    x = int.from_bytes(buf[0:1], "big")
    y = int.from_bytes(buf[2:3], "big")
    
    x_clean = 0
    y_clean = 0
    if x>200:
        x_clean = x - 256
    else:
        x_clean = x
        
    if y > 200:
        y_clean = 256 - y
    else:
        y_clean = y * -1
    
    x_pos = x_pos + x_clean
    y_pos = y_pos + y_clean
    if x_pos < 0 :
        x_pos = 32
    elif x_pos > 32 :
        x_pos = 0
    if y_pos < 0 :
        y_pos = 128
    elif y_pos > 128 :
        y_pos = 0
        
        
    
    print("x: " + str(x_pos) + " y: " + str(y_pos))     
    year, month, day = rtc.datetime()[0:3]
    date = str(month) + "/" + str(day) +"/" + str(year)
    display.text(date, y_pos, x_pos, 1)    
    display.show()
    display.fill(0)
    #postAcc(date, x_pos, y_pos)
    x_old = x
    y_old = y

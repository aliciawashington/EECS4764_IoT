from machine import RTC, Pin, PWM, I2C, ADC, SPI
#import machine
import time
import utime
import ssd1306

hspi = SPI(1, baudrate=1500000, polarity=1, phase=1)
cs = Pin(15, Pin.OUT)

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
hspi.write(b'x2e\x00')
cs.value(1)
time.sleep_ms(50)
cs.value(0)
hspi.write(b'\x38\x00')
cs.value(1)

rtc = machine.RTC()
rtc.datetime() # get date and time
dt = [2022, 10 ,5, 3, 15, 33, 0, 0]
rtc.datetime(dt)
i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5), freq=100000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)
#x_old = 0
#y_old = 0
x_pos = 0
y_pos = 0   

while True:
    cs.value(0)
    #hspi.write(b'\xb3')
    buf = bytearray(5)
    hspi.readinto(buf, 0xF2)
    cs.value(1)
    #time.sleep_ms(50)
    #cs.value(0)
    #hspi.write(b'\xb4')
    #x2 = hspi.read(1)
    x = int.from_bytes(buf[0:1], "big")
    y = int.from_bytes(buf[2:3], "big")
    #z = int.from_bytes(buf[4:5], "big")
    
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
        
    #x_clean = (x_clean+8) % 16 
    #y_clean = (y_clean+8) % 16
    #x_pos = x_clean<<1
    #y_pos = y_clean<<2
    
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
    
    x_old = x
    y_old = y
    

    

    

    
    



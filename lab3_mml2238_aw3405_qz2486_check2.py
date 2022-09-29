from machine import RTC, Pin, PWM, I2C, ADC
import utime
import ssd1306

adc = ADC(0)
lr = adc.read()

rtc = RTC()
dt = [2022, 9 ,28, 3, 15, 33, 0, 0]
rtc.datetime(dt)

i2c = I2C(sda=Pin(4), scl=Pin(5), freq=100000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

Hbutt = Pin(0, Pin.IN, Pin.PULL_UP)
Mbutt = Pin(2, Pin.IN, Pin.PULL_UP)
Sbutt = Pin(13, Pin.IN, Pin.PULL_UP)

def Hbutt_handler(p):
    time = list(rtc.datetime())
    time[4] += 1
    rtc.datetime(time)

def Mbutt_handler(p):
    time = list(rtc.datetime())
    time[5] += 1
    rtc.datetime(time)
    
def Sbutt_handler(p):
    time = list(rtc.datetime())
    time[6] += 5
    rtc.datetime(time)
    print("handled")
    
#debouncer
def wait_pin_change(pin):
    cur_value = pin.value()
    active = 0
    while active <20:
        if pin.value() != cur_value:
            active += 1
        else:
            active = 0

#wait_pin_change(Hbutt)
#wait_pin_change(Mbutt)

while True:
    #wait_pin_change(butt1)
    Hbutt.irq(trigger = Pin.IRQ_FALLING, handler= Hbutt_handler)
    Mbutt.irq(trigger = Pin.IRQ_FALLING, handler= Mbutt_handler)
    Sbutt.irq(trigger = Pin.IRQ_FALLING, handler= Sbutt_handler)
    hour = str(rtc.datetime()[4])
    minute = str(rtc.datetime()[5])
    sec = str(rtc.datetime()[6])
    time = hour + ":" + minute + ":" + sec
    lr = adc.read()
    display.text(str(rtc.datetime()[0:3]), 0, 0, 1)    
    display.text(time, 0, 10, 1)
    display.text(str(lr), 0, 20 , 1)
    display.contrast((lr>>2)-1)
    display.show()
    display.fill(0)
    



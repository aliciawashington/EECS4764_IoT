from machine import Pin, SPI, RTC, I2C
import time
import ssd1306 

hspi = SPI(1, baudrate=1500000, polarity=1, phase=1)
cs = Pin(15, Pin.OUT)
rtc = RTC()
i2c = I2C(sda=machine.Pin(4), scl=machine.Pin(5), freq=100000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)


def read_data():
    #          X D0       X D1      Y D0    Y D1     Z D0      Z D1
    data_reg = [b'\xb2', b'\xb3', b'\xb4', b'\xb5', b'\xb6', b'\xb7']
    #Read data in the x position
    cs.value(0)
    hspi.write(data_reg[0])
    buf = bytearray(1)
    hspi.readinto(buf)
    cs.value(1)
    print(buf)
    temp = int.from_bytes(buf, "big")
    print(temp)


def setupAcc():
    init_str = [b'\x31\x07', b'\x2d\x08', b'\x2c\x0a', b'\x2e\x00', b'\x38\x00']
    
    for idx, item in enumerate(init_str):
        cs.value(0)
        hspi.write(item)
        cs.value(1)
    print("Register Initialization Complete")
            
#Initialize Registers
setupAcc()

while True:
    read_data()
    time.sleep(0.1)
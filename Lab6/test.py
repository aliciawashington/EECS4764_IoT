import machine
import time
# physical connection (4 wire)
# SCK - SCL
# MO - SDA
# MI - SDO
# Pin(0) - CS
spi = machine.SPI(1, baudrate=1500000, polarity=1, phase=1)
cs = machine.Pin(15, machine.Pin.OUT)
def read_data():
    # Reading data in x position
    cs.value(0)
    spi.write(b'\xb3')
    x1 = spi.read(1)
    print(f"Register x33: {x1} ")
    print(f"Register x33 calculation value: {x1[0]}")
    cs.value(1)
    cs.value(0)
    spi.write(b'\xb2')
    x0 = spi.read(1)
    print(f"Register x32: {x0}")
    print(f"Register x32 calculation value: {x0[0]}")
    cs.value(1)
    interm_a = x1[0] * 4 + x0[0]
    x = (interm_a// 64) / 256
    print(f'Calulated X: {x}')
    print(f'Intermediate Cal x1[0]* 4 + x0[0] {interm_a}')
    if x >= 0 and x <= 2:
        x = x
    else:
        x = x - 4
    # Reading data in yposition
    cs.value(0)
    spi.write(b'\xb5')
    y1 = spi.read(1)
    cs.value(1)
    cs.value(0)
    spi.write(b'\xb4')
    y0 = spi.read(1)
    cs.value(1)
    y = (y1[0] * 4 + y0[0] // 64) / 256
    if y >= 0 and y <= 2:
        y = y
    else:
        y = y - 4
    return [x, y]
power = b'\x2d\x08'
# full-res/left/2g
data_format = b'\x31\x0c'
# 00001100
cs.value(0)
spi.write(power)
cs.value(1)
cs.value(0)
spi.write(data_format)
cs.value(1)
while True:
    dx, dy = read_data()
    print(dx, dy)
    time.sleep(0.1)
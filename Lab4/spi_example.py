from machine import SPI, Pin

#Physical connections
# SCK -> SCL
# MO -> SDA
# MI -> SDO
#initialize the hardware spi on the esp8266
hspi = SPI(1, baudrate=1500000, polarity=1, phase=1)
cs = Pin(15, mode=Pin.OUT, value=1) # Replace 15 with correct pin

try:
    cs(0) #Enable CS pin
    hspi.write(#some stuff) #Write Data
finally:
    cs(1) #Disable CS pin

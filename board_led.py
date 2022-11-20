from machine import Pin

# must use 'LED' on PICOW instead of PIN-X
LED = Pin('LED', Pin.OUT)
LED.on()

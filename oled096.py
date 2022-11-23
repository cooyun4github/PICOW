import time
from machine import Pin, I2C

# i2c
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400_000)
slv_addr = i2c.scan()[0] # 0x3c
print("i2c device address:", hex(slv_addr))

def i2c_write(sig, data):
    i2c.writeto(slv_addr, bytearray([sig, data]))


# 0.96 oled params
PAGE = 8
ROW = 128
WRITE_DATA_SIG = 0x40
WRITE_CMD_SIG = 0x00
PAGE_START = 0xb0
LOW_COLUMN_ADDR = 0
HIGH_COLUMN_ADDR = 0x10


def fill_black():
    for p in range(8):
        i2c_write(WRITE_CMD_SIG, 0xb0 + p)
        i2c_write(WRITE_CMD_SIG, 0)
        i2c_write(WRITE_CMD_SIG, 16)
        for r in range(128):
            i2c_write(WRITE_DATA_SIG, 0)

def fill_picture(data):
    for p in range(PAGE):
        i2c_write(WRITE_CMD_SIG, PAGE_START + p)
        i2c_write(WRITE_CMD_SIG, LOW_COLUMN_ADDR)
        i2c_write(WRITE_CMD_SIG, HIGH_COLUMN_ADDR)
        for r in range(ROW):
            i2c_write(WRITE_DATA_SIG, data)

def init_oled():
    i2c_write(WRITE_CMD_SIG, 0xAE) # display off
    i2c_write(WRITE_CMD_SIG, 0x20)
    i2c_write(WRITE_CMD_SIG, 0x10)
    i2c_write(WRITE_CMD_SIG, 0xb0)
    i2c_write(WRITE_CMD_SIG, 0xc8)
    i2c_write(WRITE_CMD_SIG, 0x00)
    i2c_write(WRITE_CMD_SIG, 0x10)
    i2c_write(WRITE_CMD_SIG, 0x40)

    i2c_write(WRITE_CMD_SIG, 0x81) # contract control
    i2c_write(WRITE_CMD_SIG, 0x7F) # 1~255, RESET = 7Fh

    i2c_write(WRITE_CMD_SIG, 0xa1) # segment remap
    i2c_write(WRITE_CMD_SIG, 0xa6) # normal/reverse
    i2c_write(WRITE_CMD_SIG, 0xa8) # multiplex ratio
    i2c_write(WRITE_CMD_SIG, 0x3F)

    i2c_write(WRITE_CMD_SIG, 0xa4) # resume to RAM content/always entir display on

    i2c_write(WRITE_CMD_SIG, 0xd3) # display offset
    i2c_write(WRITE_CMD_SIG, 0x00)
    i2c_write(WRITE_CMD_SIG, 0xd5) # osc division
    i2c_write(WRITE_CMD_SIG, 0xf0)
    i2c_write(WRITE_CMD_SIG, 0xd9) # pre-charge period
    i2c_write(WRITE_CMD_SIG, 0x22)
    i2c_write(WRITE_CMD_SIG, 0xda) # COM pins
    i2c_write(WRITE_CMD_SIG, 0x12)
    i2c_write(WRITE_CMD_SIG, 0xdb) # vcomh
    i2c_write(WRITE_CMD_SIG, 0x20)
    i2c_write(WRITE_CMD_SIG, 0x8d) # charge pump enable
    i2c_write(WRITE_CMD_SIG, 0x14) 
    i2c_write(WRITE_CMD_SIG, 0xaf) # display on

def main():
    init_oled()
    fill_black()
    while(1):
        fill_picture(0x0)
        time.sleep(1)
        fill_picture(0x0f)
        time.sleep(1)

main()

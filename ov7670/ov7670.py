from machine import Pin, PWM, I2C
import time
import ov7670_init_param
import ov7670_my_param

machine.freq(260_000_000)

# ov7670
vs = Pin(20, Pin.IN)
hs = Pin(19, Pin.IN)
pc = Pin(21, Pin.IN)
pin28 = Pin(28, Pin.OUT)
vs_count = 0
hs_count = 0
pc_count = 0

# https://docs.micropython.org/en/latest/library/machine.Pin.html?highlight=irq#machine.Pin.irq
# The irq handler must take exactly one argument which is the Pin instance
def vs_rising_irq(pin):
    global vs_count
    global hs_count
    vs_count += 1
    hs_count = 0
    print("vs_count:", vs_count)

def hs_rising_irq(pin):
    global hs_count
    hs_count += 1

def hs_test_irq(pin):
    global pin28
    pin28.value(hs.value())

def pc_irq(pin):
    global pin28
    pin28.value(pc.value())


rgb565_qvga = ov7670_init_param.rgb565_qvga_25fps
yuv_640x480 = ov7670_init_param.yuv_12fps
yuv_320x240 = ov7670_my_param.yuv_qvga_12fps
yuv_160x120 = ov7670_my_param.yuv_qqvga_12fps
yuv_80x60   = ov7670_my_param.yuv_80x60


# XCLK
XCLK = PWM(Pin(22))
MAX_DUTY_MAP = 65535
XCLK.freq(8_000_000)
XCLK.duty_u16(32768)


# i2c
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)
slv_addrs = i2c.scan()
print("number of slave:", len(slv_addrs))
if len(slv_addrs) == 0:
    print("No i2c device")
else:
    for slv_addr in slv_addrs:
        print("slave address:", hex(slv_addr))
slv_addr = 0x21

def sccb_write(reg, data):
    i2c.writeto(slv_addr, bytearray([reg, data]))

def sccb_read(reg):
    i2c.writeto(slv_addr, bytearray([reg]))
    return i2c.readfrom(slv_addr, 1)[0]


def ov7670_init():
    for param in yuv_80x60:
        print(hex(param[0]), "-", hex(param[1]))
        sccb_write(param[0], param[1])


sccb_write(0x12, 0x80)
time.sleep(1)
ov7670_init()
time.sleep(1)


def main1():
    pc_last = 0
    hs_last = 0
    vs_last = 0
    vs_count = 0
    hs_count = 0
    pc_count = 0

    while(1):
        while (vs.value()):
            # 先count++一次
            if (0 == vs_last):
                vs_last = 1
                vs_count += 1

            while (hs.value()):
                # 先count++一次
                if (0 == hs_last):
                    hs_last = 1
                    hs_count +=1

                # pc count计算
                pc_value = pc.value()
                if (1 == pc_value and 0 == pc_last):
                    pc_count += 1
                pc_last = pc_value

            # 出循环，hs.value()变化，hs_last也变化
            hs_last = 0
        # 出循环，vs.value()变化，vs_last也变化
        # 变化前先打印一次信息
        if (1 == vs_last):
            print("frame id:", vs_count, " height:", hs_count, " frame pixel:", pc_count)
            vs_last = 0
            hs_count = 0
            pc_count = 0


# 实际证明，使用中断更耗时间
def main0():
    vs.irq(trigger = Pin.IRQ_RISING, handler = vs_rising_irq)
    hs.irq(trigger = Pin.IRQ_RISING, handler = hs_rising_irq)
    #pc.irq(trigger = Pin.IRQ_RISING, handler = test_irq)

    global pin28
    while(1):
        pin28.value(pc.value())

    global pc_count
    pc_last = 0
    count = 0
    while(1):
        if (1 == vs.value() and 1 == hs.value() and pc.value() != pc_last):
            pc_count += pc.value()
            pc_last = pc.value()
        if (pc_count == 80 * 60):
            pc_count = 0
            count += 1
            print(count)


main1()

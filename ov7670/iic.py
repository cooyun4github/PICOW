from machine import Pin, I2C

# class i2c represents a pair of master-slav
# 1-N need multiplu instances
class IIC:
    def __init__(self, i2c_id, scl_pin, sda_pin, frequency = 400_000, slv_addr = 0):
        self.i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=frequency)
        if (0 == slv_addr):
            slv_addrs = self.i2c.scan()
            if len(slv_addrs) == 0:
                print("No i2c device")
            else:
                print("i2c device found, address:", hex(slv_addrs[0]))
                self.slv_addr = slv_addrs[0]

    def write(self, reg, data):
        self.i2c.writeto(self.slv_addr, bytearray([reg, data]))
        # print("write ", "{:#04x}".format(data), "to reg", "{:#04x}".format(reg), "success")

    def readfrom_mem(self, reg, num):
        return self.i2c.readfrom(self.slv_addr, reg, num)

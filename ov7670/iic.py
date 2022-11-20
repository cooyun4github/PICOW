from machine import Pin, I2C

# class i2c represents a pair of master-slav
# 1-N need multiplu instances
# how to use:
# import ii2
# i2c = iic.IIC(0, 17, 16)
class IIC:
    def __init__(self, i2c_id, scl_pin, sda_pin, frequency = 400_000, slv_addr = 0):
        self.scl_pin = Pin(scl_pin)
        self.sda_pin = Pin(sda_pin)
        self.i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=frequency)

        if (0 == slv_addr):
            slv_addrs = self.i2c.scan()
            if len(slv_addrs) == 0:
                print("No i2c device")
            else:
                print("i2c device found, address:", hex(slv_addrs[0]))
                self.slv_addr = slv_addrs[0]


    def start(self):
        self.scl_pin.on()
        self.sda_pin.on()
        # time.sleep_us(1)
        self.sda_pin.off()
        # time.sleep_us(1)


    def stop(self):
        self.scl_pin.on()
        self.sda_pin.off()
        #time.sleep_us(1)
        self.sda_pin.on()


    def write(self, write_sig, data):
        self.start()
        self.i2c.writeto(self.slv_addr, bytearray([write_sig, data]))
        self.stop()

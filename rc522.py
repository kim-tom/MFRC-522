import RPi.GPIO as GPIO
from pirc522 import RFID
import time

class RC522(RFID):
    def wait_for_tag(self, timeout=0):
        # enable IRQ on detect
        self.init()
        self.irq.clear()
        self.dev_write(0x04, 0x00)
        self.dev_write(0x02, 0xA0)
        # wait for it
        waiting = True
        start_time = time.time()
        while waiting:
            self.init()
            #self.irq.clear()
            self.dev_write(0x04, 0x00)
            self.dev_write(0x02, 0xA0)

            self.dev_write(0x09, 0x26)
            self.dev_write(0x01, 0x0C)
            self.dev_write(0x0D, 0x87)
            waiting = not self.irq.wait(0.1)
            if timeout > 0 and (time.time() - start_time) > timeout:
                print("timeout!")
                break
        self.irq.clear()
        self.init()
    def power_on(self):
        GPIO.output(self.pin_rst, 1)
    def power_off(self):
        GPIO.output(self.pin_rst, 0)
    def get_RFID(self, timeout=0):
        self.wait_for_tag(timeout)
        (error, tag_type) = self.request()
        if not error :
            (error, uid) = self.anticoll()
        else:
            uid =  [0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        return uid

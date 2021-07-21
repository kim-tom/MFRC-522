from wsgiref.simple_server import make_server
import RPi.GPIO as GPIO
from pirc522 import RFID
import time
import json

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class MY_RFID(RFID):
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
        self.reset()

rc522 = MY_RFID()
def get_RFID():
    rc522.wait_for_tag(0.1)
    (error, tag_type) = rc522.request()
    if not error :
        (error, uid) = rc522.anticoll()
        return uid
    else:
        return [0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
def app(environ, start_response):
  status = '200 OK'
  headers = [
    ('Content-type', 'application/json; charset=utf-8'),
    ('Access-Control-Allow-Origin', '*'),
  ]
  start_response(status, headers)
  return [json.dumps({'id': get_RFID()}).encode("utf-8")]

with make_server('', 3000, app) as httpd:
  print("Serving on port 3000...")
  httpd.serve_forever()

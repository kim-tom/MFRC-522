from wsgiref.simple_server import make_server
import RPi.GPIO as GPIO
from pirc522 import RFID
import time
import json

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
rc522 = RFID()
def get_RFID():
    rc522.wait_for_tag()
    (error, tag_type) = rc522.request()
    if not error :
        (error, uid) = rc522.anticoll()
    if not error :
        return uid
    else:
        return 0
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

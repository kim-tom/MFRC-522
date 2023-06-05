from rc522 import RC522
import time
from fastapi import FastAPI
import RPi.GPIO as GPIO

rc522 = RC522()
app = FastAPI()

@app.get("/")
def get_id():
   id_ = rc522.get_RFID(0.1)
   if int(time.time()) % 600 == 0:
      rc522.power_off()
      print("Reset Started.")
      time.sleep(0.001)
      rc522.power_on()
      print("Reset Finished.")
   return {
       "id": id_
   }
@app.get("/reset")
def reset():
   rc522.power_off()
   print("Reset Started.")
   time.sleep(1)
   rc522.power_on()
   print("Reset Finished.")
   return {
       "reset": 1
   }

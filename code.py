from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
import ntptime
import urequests
import json
import time
import unit

setScreenColor(0xa7daff)
env3_0 = unit.get(unit.ENV3, unit.PORTA)

image0 = M5Img(225, 170, "res/default.jpg", True)
label0 = M5TextBox(10, 20, "12:00", lcd.FONT_DejaVu56, 0x000000, rotate=0)
label1 = M5TextBox(10, 81, "12/12/2024", lcd.FONT_DejaVu24, 0x000000, rotate=0)
label2 = M5TextBox(10, 117, "Room:", lcd.FONT_UNICODE, 0x000000, rotate=0)
label3 = M5TextBox(90, 115, "-10F", lcd.FONT_DejaVu24, 0x000000, rotate=0)
label5 = M5TextBox(120, 155, "100F", lcd.FONT_DejaVu24, 0x000000, rotate=0)
label4 = M5TextBox(10, 155, "Current:", lcd.FONT_DejaVu24, 0x000000, rotate=0)
circle0 = M5Circle(300, 20, 6, 0xFFFFFF, 0x7a7a7a)
label6 = M5TextBox(10, 196, "Partly Cloudy", lcd.FONT_DejaVu24, 0x000000, rotate=0)

# Describe this function... 
def Current_Temperature():
  label3.setText(str((str(("%.2f"%(((9 / 5) * (env3_0.temperature) + 32)))) + str('°F'))))

# Describe this function...
def Display_Time_And_Date():
  if (ntp.minute()) >= 10:
    label0.setText(str((str(((str((ntp.hour())) + str(':')))) + str((ntp.minute())))))
  else:
    label0.setText(str((str(((str((ntp.hour())) + str(':')))) + str(((str('0') + str((ntp.minute()))))))))
  label1.setText(str((str(((str(((str((ntp.month())) + str('/')))) + str(((str((ntp.day())) + str('/'))))))) + str((ntp.year())))))

wifiCfg.autoConnect(lcdShow=False)
if wifiCfg.wlan_sta.isconnected():
  circle0.setBgColor(0x33cc00)
ntp = ntptime.client(host='us.pool.ntp.org', timezone=8)
try:
  req = urequests.request(method='GET', url='http://api.weatherapi.com/v1/current.json?key=e88b3268525441fc97c234023240406&q=19026&aqi=no', headers={})
  label5.setText(str(req.json()['current']['temp_f'])+"F")
  label6.setText(str(req.json()['current']['condition']['text']))
  image0.changeImg("res/"+req.json()['current']['condition']['icon'].split('/')[-1])
  image0.hide()
  image0.show()
  gc.collect()
  req.close()
except:
  pass
while True:
  Display_Time_And_Date()
  Current_Temperature()
  wait(5)
  wait_ms(2)

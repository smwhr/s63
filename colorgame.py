from gpiozero.pins.mock import MockFactory
from gpiozero import Device
Device.pin_factory = MockFactory()

from device import S63
#from simulator import S63

phone = S63()

def makeColor(i):
  print(i)
  if i == "1":
    phone.led.red = 1
  if i == "2":
    phone.led.green = 1
  if i == "3":
    phone.led.blue = 1
  if i == "4":
    phone.led.red = 0.66
  if i == "5":
    phone.led.green = 0.66
  if i == "6":
    phone.led.blue = 0.66
  if i == "7":
    phone.led.red = 0.33
  if i == "8":
    phone.led.green = 0.33
  if i == "9":
    phone.led.blue = 0.33
  if i == "0":
    phone.led.green = 0
  if i == "*":
    phone.led.red = 0
  if i == "#":
    phone.led.blue = 0

def say_hello():
    phone.led.color = (1,1,1)

def say_goodbye():
    phone.led.color = (0,0,0)

def compose(n):
    makeColor(n)


phone.comb_when_pressed = say_hello
phone.comb_when_released = say_goodbye
phone.on_compose = compose

phone.run()
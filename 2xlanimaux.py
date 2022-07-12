# from gpiozero.pins.mock import MockFactory
# from gpiozero import Device
# Device.pin_factory = MockFactory()
import pyglet

# from device import S63
from simulator import S63

phone = S63()
player = pyglet.media.Player()

sources = {}
sources['1'] = pyglet.media.load('tiger2xl/tiger2xllemondedesanimaux/Track1.ogg')
sources['2'] = pyglet.media.load('tiger2xl/tiger2xllemondedesanimaux/Track2.ogg')
sources['3'] = pyglet.media.load('tiger2xl/tiger2xllemondedesanimaux/Track3.ogg')
sources['4'] = pyglet.media.load('tiger2xl/tiger2xllemondedesanimaux/Track4.ogg')

def makeColor(i):
  print(i)
  if i == "1":
    phone.led.red = 1
    phone.led.green = 0
    phone.led.blue = 0
  elif i == "2":
    phone.led.red = 0
    phone.led.green = 1
    phone.led.blue = 0
  elif i == "3":
    phone.led.red = 0
    phone.led.green = 0
    phone.led.blue = 1
  elif i == "4":
    phone.led.red = 0
    phone.led.green = 0.5
    phone.led.blue = 0.5
  else:
    phone.led.red = 0
    phone.led.green = 0
    phone.led.blue = 0


init = False
current_track = '1'
def say_hello():
    global init
    if not init:
        player.queue(sources['1'])
        player.seek(50)
        init = True
    player.play()
    phone.led.color = (1,1,1)

def say_goodbye():
    player.pause()
    phone.led.color = (0,0,0)

def compose(n):
    global current_track, sources
    makeColor(n)
    next_track = n
    if next_track in sources and current_track != next_track:
        next_source = sources[next_track]
        current_time = player.time
        player.pause()
        player.queue(next_source)
        player.next_source()
        player.seek(current_time)
        player.play()
        current_track = next_track
        print(player.source)
    if n == "*":
        player.seek(player.time - 3)
    if n == "#":
        player.seek(player.time + 3)


phone.comb_when_pressed = say_hello
phone.comb_when_released = say_goodbye
phone.on_compose = compose

phone.run()
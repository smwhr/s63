from gpiozero import Button, RGBLED
from signal import pause
from collections import namedtuple
import rx
from rx import Observable
from rx import operators as ops


led = RGBLED(red=4, green=14, blue=15)
# loading : red
led.color = (1, 0, 0)


def say_hello():
    led.color = (1,1,1)


def say_goodbye():
    led.color = (0,0,0)


comb = Button(3)
comb.when_pressed = say_hello
comb.when_released = say_goodbye

Row = namedtuple('Row', ['n'])
Col = namedtuple('Col', ['n'])

buttons = {}


def debug_pressed(v):
    print(v)


def observeRowPins(pins):
    def handle(observer, scheduler):
        def _handle(b):
            observer.on_next(Row(n=pins.index(b.pin.number)))
        for pin in pins:
            buttons[pin] = Button(pin)
            buttons[pin].when_pressed = _handle
    return handle


def observeColPins(pins):
    def handle(observer, scheduler):
        def _handle(b):
            observer.on_next(Col(n=pins.index(b.pin.number)))
        for pin in pins:
            buttons[pin] = Button(pin)
            buttons[pin].when_pressed = _handle
    return handle


colStream = rx.create(observeColPins(COL_PINS))
rowStream = rx.create(observeRowPins(ROW_PINS))

#colStream.subscribe(on_next=lambda i: print(i))
#rowStream.subscribe(on_next=lambda i: print(i))

def findKey(xy):
  row, col = xy
  return KEYPAD[row.n][col.n]

keyStream = rowStream.pipe(
                ops.join(
                  colStream,
                  lambda l: rx.timer(.01),
                  lambda r: rx.timer(.01)
                ),
                ops.map(findKey),
            )

def makeColor(i):
  print(i)
  if i == 1:
    led.red = 1
  if i == 2:
    led.green = 1
  if i == 3:
    led.blue = 1
  if i == 4:
    led.red = 0.66
  if i == 5:
    led.green = 0.66
  if i == 6:
    led.blue = 0.66
  if i == 7:
    led.red = 0.33
  if i == 8:
    led.green = 0.33
  if i == 9:
    led.blue = 0.33
  if i == 0:
    led.green = 0
  if i == "*":
    led.red = 0
  if i == "#":
    led.blue = 0


# keyStream.subscribe(on_next=lambda i: print(i))
keyStream.subscribe(on_next=lambda i: makeColor(i))

# ready : green
led.color = (0, 1, 0)
pause()

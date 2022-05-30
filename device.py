from gpiozero import Button, RGBLED
from signal import pause
from collections import namedtuple
import rx
from rx import Observable
from rx import operators as ops

Row = namedtuple('Row', ['n'])
Col = namedtuple('Col', ['n'])

KEYPAD = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
]
ROW_PINS = [7 , 8, 25, 24]
COL_PINS = [11, 9, 10]
HANG_PIN = 23

class S63(object):
    def __init__(self):
        self.init_callbacks()
        self.init_hanger()
        self.init_buttons()
        self.init_led()

    def init_callbacks(self):
        self.comb_when_pressed = lambda: None
        self.comb_when_released = lambda: None
        self.on_compose = lambda: None

    def init_hanger(self):
        self.comb = Button(HANG_PIN)

        def when_pressed():
            self.comb_when_pressed()
        def when_released():
            self.comb_when_released()

        self.comb.when_pressed = when_pressed
        self.comb.when_released = when_released

    def init_buttons(self):
        self.buttons = {}
        colStream = rx.create(self.observeColPins(COL_PINS))
        rowStream = rx.create(self.observeRowPins(ROW_PINS))

        keyStream = rowStream.pipe(
                      ops.join(
                        colStream,
                        lambda l: rx.timer(.01),
                        lambda r: rx.timer(.01)
                      ),
                      ops.map(self.findKey),
                  )

        keyStream.subscribe(on_next=lambda i: self.on_compose(i))

    def observeRowPins(self,pins):
        def handle(observer, scheduler):
            def _handle(b):
                observer.on_next(Row(n=pins.index(b.pin.number)))
            for pin in pins:
                self.buttons[pin] = Button(pin)
                self.buttons[pin].when_pressed = _handle
        return handle


    def observeColPins(self,pins):
        def handle(observer, scheduler):
            def _handle(b):
                observer.on_next(Col(n=pins.index(b.pin.number)))
            for pin in pins:
                self.buttons[pin] = Button(pin)
                self.buttons[pin].when_pressed = _handle
        return handle

    def findKey(self, xy):
      row, col = xy
      return KEYPAD[row.n][col.n]

    def init_led(self):
      self.led = RGBLED(red=4, green=14, blue=15)
      pass

    def run(self):
      pause()
    

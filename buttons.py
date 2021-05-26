from gpiozero import Button
from signal import pause


def pressed(b):
    print(b)

def say_hello():
    print("Hello!")

def say_goodbye():
    print("Goodbye!")

comb = Button(23)

comb.when_pressed = say_hello
comb.when_released = say_goodbye

c1 = Button(11)
c1.when_pressed = lambda b: pressed("c1")

c2 = Button(9)
c2.when_pressed = lambda b: pressed("c2")

c3 = Button(10)
c3.when_pressed = lambda b: pressed("c3")

l1 = Button(7)
l1.when_pressed = lambda b: pressed("l1")

l2 = Button(8)
l2.when_pressed = lambda b: pressed("l2")

l3 = Button(25)
l3.when_pressed = lambda b: pressed("l3")

l4 = Button(24)
l4.when_pressed = lambda b: pressed("l4")

print("Phone is ready")

pause()

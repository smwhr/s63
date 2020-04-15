from gpiozero import Button
from signal import pause


def pressed(b):
    print(b)

def say_hello():
    print("Hello!")

def say_goodbye():
    print("Goodbye!")

comb = Button(3)

comb.when_pressed = say_hello
comb.when_released = say_goodbye

c1 = Button(11)
c1.when_pressed = lambda b: pressed("c1")

c2 = Button(25)
c2.when_pressed = lambda b: pressed("c2")

c3 = Button(9)
c3.when_pressed = lambda b: pressed("c3")

l1 = Button(19)
l1.when_pressed = lambda b: pressed("l1")

l2 = Button(16)
l2.when_pressed = lambda b: pressed("l2")

l3 = Button(6)
l3.when_pressed = lambda b: pressed("l3")

l4 = Button(20)
l4.when_pressed = lambda b: pressed("l4")

print("Phone is ready")

pause()
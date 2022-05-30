import pyglet
from signal import pause

player = pyglet.media.Player()
source = pyglet.media.load('tiger2xl/tiger2xllemondedesanimaux/Track1.ogg')
player.queue(source)
player.play()

pause()
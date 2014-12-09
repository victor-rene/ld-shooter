from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.uix.image import Image


class Saucer(Image):

  def __init__(self, **kw):
    super(Saucer, self).__init__(**kw)
    self.source = 'img/saucer.png'
    self.dx = 0
    self.dy = 0
    self.size = 50, 50
    self.counter = 0
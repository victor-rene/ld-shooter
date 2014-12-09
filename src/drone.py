from kivy.graphics import Rectangle
from kivy.uix.image import Image


class Drone(Image):
  def __init__(self, **kw):
    super(Drone, self).__init__(**kw)
    self.source = 'img/drone.png'
    self.dx = 0
    self.dy = 0
    self.size = 80, 80
    self.counter = 0
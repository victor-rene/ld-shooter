from random import randint

from kivy.uix.image import Image
from kivy.uix.widget import Widget


class Explosion(Widget):

  def __init__(self, x, y, **kw):
    super(Explosion, self).__init__(**kw)
    self.images = [None, None, None]
    for i in range(0, 3):
      self.images[i] = Image(source='img/explosion.zip')
      img = self.images[i]
      img.anim_delay = .1
      img.pos = x + randint(-20, 20), y + randint(-20, 20)
      img.size = 40, 40
      self.add_widget(img)
    self.pos = x, y
    self.size = 70, 70
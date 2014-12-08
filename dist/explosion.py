from kivy.uix.image import Image


class Explosion(Image):

  def __init__(self, x, y, **kw):
    super(Explosion, self).__init__(**kw)
    self.source='img/explosion.zip'
    self.pos = x, y
    self.size = 70, 70
    self.anim_delay = .1
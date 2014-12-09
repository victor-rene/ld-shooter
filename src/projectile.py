from kivy.uix.image import Image


class Projectile(Image):

  def __init__(self, type, dx, dy, player, **kw):
    super(Projectile, self).__init__(**kw)
    self.source = 'img/' + type + '.png'
    self.dx = dx
    self.dy = dy
    self.player = player
    self.score_bonus = 1
from kivy.graphics import Rectangle
from kivy.uix.image import Image


class Ship(Image):

  def __init__(self, **kw):
    super(Ship, self).__init__(**kw)
    self.source = 'img/ship.png'
    self.dx = 0
    self.dy = 0
    self.bind(pos=self._update_rect)
    self.bind(size=self._update_rect)
    with self.canvas.after:
      self.rect_shield = Rectangle(source='img/blank.png')   
    self.afterburner = Image(source='img/afterburner.zip')
    self.add_widget(self.afterburner)
    self.shield = 100
    self.anim_delay = .1
      
  def _update_rect(self, *args):
    self.rect_shield.pos = self.pos
    self.rect_shield.size = self.size
    self.afterburner.pos = self.pos
    self.afterburner.size = self.size
    
  def steer_x(self, value):
    self.dx = value
    
  def steer_y(self, value):
    self.dy = value
    
  def shield(self, color):
    if color:
      self.rect_shield.source = 'img/' + color + '-shield.png'
    else:
      self.rect_shield.source = None
      
  def on_pos(self, *args):
    if self.x < 0:
      self.x = 0
    if self.x > self.parent.width - self.width:
      self.x = self.parent.width - self.width
    if self.y < 0:
      self.y = 0
    if self.y > self.parent.height - self.height:
      self.y = self.parent.height - self.height
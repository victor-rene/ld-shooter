from random import randint

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_pygame import SoundPygame
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from __main__ import root_widget
from drone import Drone
from projectile import Projectile
from saucer import Saucer
from ship import Ship
from util import check_classname


class Game(Widget):

  def __init__(self, **kw):
    super(Game, self).__init__(**kw)
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
    self._keyboard.bind(on_key_up=self._on_keyboard_up)
    self.build_ship()
    with self.canvas.before:
      self.rect_bg1 = Image(source='img/background-blue.png')
      self.rect_bg2 = Image(source='img/background-blue.png') # allow_stretch=True, keep_ratio=False
    self.bind(size=self._update_rect)
    self.bind(pos=self._update_rect)
    self.counter = 0
    self.drones = []
    self.saucers = []
    Clock.schedule_interval(self.anim_objects, 1./60)
    self.sfx_laser = SoundPygame(source='sfx/laser.wav')
    self.sfx_explo = SoundPygame(source='sfx/explosion.wav')
    
  def _update_rect(self, *args):
    self.rect_bg1.pos = self.width/2 - self.height/2, 0
    self.rect_bg1.size = self.height, self.height * 1
    self.rect_bg2.pos = self.width/2 - self.height/2, self.height
    self.rect_bg2.size = self.height, self.height * 1
    
  def build_ship(self):
    self.ship = Ship(size=(100, 100))
    self.add_widget(self.ship)
    self.center_widget(self.ship, 'h')
    
  def center_widget(self, widget, orientation):
    if orientation == 'h':
      widget.x = self.width/2 - widget.width/2
    elif orientation == 'v':
      widget.y = self.height/2 - widget.height/2

  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    self._keyboard = None

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
      self.ship.steer_x(-20)
    elif keycode[1] == 'right':
      self.ship.steer_x(20)
    elif keycode[1] == 'up':
      self.ship.steer_y(20)
    elif keycode[1] == 'down':
      self.ship.steer_y(-20)
    elif keycode[1] == 'd':
      missile = Projectile('missile', 0, 10, 'player')
      missile.size = 75, 75
      missile.x = self.ship.get_center_x() - missile.width / 2
      missile.y = self.ship.y + self.ship.height
      self.add_widget(missile)
    elif keycode[1] == 's':
      if self.sfx_laser.state == 'play':
        self.sfx_laser.stop()
      self.sfx_laser.play()
      laser1 = Projectile('laser', 0, 20, 'player')
      laser1.x = self.ship.x + self.ship.width * .35
      laser1.y = self.ship.y + self.ship.height / 10
      self.add_widget(laser1)
      laser2 = Projectile('laser', 0, 20, 'player')
      laser2.x = self.ship.x - self.ship.width * .35
      laser2.y = self.ship.y + self.ship.height / 10
      self.add_widget(laser2)
    elif keycode[1] == 'd':
      self.ship.shield('blue')
    elif keycode[1] == 's':
      self.ship.shield('green')
    return True
    
  def _on_keyboard_up(self, keyboard, keycode):
    if keycode[1] == 'left':
      self.ship.steer_x(0)
    elif keycode[1] == 'right':
      self.ship.steer_x(0)
    elif keycode[1] == 'up':
      self.ship.steer_y(0)
    elif keycode[1] == 'down':
      self.ship.steer_y(0)
    return True
    
  def spawn_drone(self):
    if self.counter % 80 == 0:
      drone = Drone()
      max_x = self.width/2 + self.height/2
      min_x = self.width/2 - self.height/2
      drone.x = randint(min_x, max_x)
      drone.y = self.height
      drone.dy = randint(-5, -3)
      drone.dx = randint(-3, 3)
      self.add_widget(drone)
      self.drones.append(drone)
      
  def fire_drone(self):
    if self.counter % 40 == 0:
      for drone in self.drones:
        bullet1 = Projectile('bullet', 0, -10, 'computer')
        bullet1.x = drone.center_x - bullet1.width/2 + drone.width * .4
        bullet1.y = drone.y
        self.add_widget(bullet1)
        bullet2 = Projectile('bullet', 0, -10, 'computer')
        bullet2.x = drone.center_x - bullet2.width/2 - drone.width * .4
        bullet2.y = drone.y
        self.add_widget(bullet2)
        
  def spawn_saucer(self):
    if self.counter % 60 == 0:
      saucer = Saucer()
      max_x = self.width/2 + self.height/2
      min_x = self.width/2 - self.height/2
      saucer.x = randint(min_x, max_x)
      saucer.y = self.height
      saucer.dy = randint(-5, -3)
      saucer.dx = randint(-3, 3)
      self.add_widget(saucer)
      self.saucers.append(saucer)
      
  def fire_saucer(self):
    if self.counter % 30 == 0:
      for saucer in self.saucers:
        bullet1 = Projectile('bullet', 0, -10, 'computer')
        bullet1.x = saucer.center_x - bullet1.width/2
        bullet1.y = saucer.y
        self.add_widget(bullet1)
        bullet2 = Projectile('bullet', -7, -7, 'computer')
        bullet2.x = saucer.center_x - bullet2.width/2 - saucer.width * .4
        bullet2.y = saucer.y
        self.add_widget(bullet2)
        bullet3 = Projectile('bullet', 7, -7, 'computer')
        bullet3.x = saucer.center_x - bullet3.width/2 + saucer.width * .4
        bullet3.y = saucer.y
        self.add_widget(bullet3)
      
  def anim_objects(self, dt):
    self.counter += 1
    self.spawn_drone()
    self.spawn_saucer()
    self.fire_drone()
    self.fire_saucer()
    for child in self.children:
      if child.dx or child.dy:
        # movement
        child.x += child.dx
        child.y += child.dy
        # collision check
        if check_classname(child, 'Projectile'):
          if child.player == 'player':
            for drone in self.drones:
              if child.collide_widget(drone):
                self.remove_widget(child)
                self.remove_widget(drone)
                self.drones.remove(drone)
            for saucer in self.saucers:
              if child.collide_widget(saucer):
                self.remove_widget(child)
                self.remove_widget(saucer)
                self.saucers.remove(saucer)
              if self.sfx_explo.state == 'play':
                self.sfx_explo.stop()
              self.sfx_explo.play()
      # outside of screen        
      if child.y < - 200:
        self.remove_widget(child)
        if check_classname(child, 'Drone'):
          self.drones.remove(child)
        elif check_classname(child, 'Saucer'):
          self.saucers.remove(child)
      if child.y > self.height + 200:
        self.remove_widget(child)
        if check_classname(child, 'Drone'): 
          self.drones.remove(child)
        elif check_classname(child, 'Saucer'):
          self.saucers.remove(child)
    # background scrolling      
    self.rect_bg1.y -= 3
    self.rect_bg2.y -= 3
    if self.rect_bg1.y < - self.height:
      self.rect_bg1.y = self.rect_bg2.y + self.rect_bg2.height
    if self.rect_bg2.y < - self.height:
      self.rect_bg2.y = self.rect_bg1.y + self.rect_bg1.height
    # fps update  
    lbl_fps.text = '%.2f' % Clock.get_fps()

game = Game()
lbl_fps = Label(pos_hint={'center_x': .95, 'center_y': .95})
root_widget.add_widget(game)
root_widget.add_widget(lbl_fps)
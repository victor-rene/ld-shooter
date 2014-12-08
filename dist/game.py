from random import randint

from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
# from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_pygame import SoundPygame
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from __main__ import root_widget
from drone import Drone
from explosion import Explosion
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
    self.ship = Ship()
    with self.canvas.before:
      self.rect_bg1 = Image(source='img/background-blue.png', allow_stretch=True, keep_ratio=False)
      self.rect_bg2 = Image(source='img/background-blue.png', allow_stretch=True, keep_ratio=False) # , allow_stretch=True, keep_ratio=False
    self.bind(size=self._update_rect)
    self.bind(pos=self._update_rect)
    self.counter = 0
    self.drones = []
    self.saucers = []
    Clock.schedule_interval(self.anim_objects, 1./60)
    self.sfx_laser = SoundPygame(source='sfx/laser.wav')
    self.sfx_explo = SoundPygame(source='sfx/explosion.wav')
    # self.sfx_laser = SoundLoader.load('sfx/laser.wav')
    # self.sfx_explo = SoundLoader.load('sfx/explosion.wav')
    self.img_explo = []
    with self.canvas.after:
      Color(.8, .2, .2, 1)
      self.lifebar = Rectangle() 
    self.score = 0
    self.accel = 0
    self._initialized = False
    
  def _update_rect(self, *args):
    # self.rect_bg1.pos = self.width/2 - self.height/2, 0
    # self.rect_bg1.size = self.height, self.height * 1
    # self.rect_bg2.pos = self.width/2 - self.height/2, self.height
    # self.rect_bg2.size = self.height, self.height * 1
    self.rect_bg1.pos = self.pos
    self.rect_bg1.size = self.size
    self.rect_bg2.pos = 0, self.height
    self.rect_bg2.size = self.size
    if not self._initialized:
      self.initialize()
    
  def initialize(self):
    self.add_widget(self.ship)
    self.ship.pos= self.center_x - self.ship.width/2, self.y
    self.update_health()
    self._initialized = True

  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    self._keyboard = None

  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'escape':
      self.app_close()
    if keycode[1] == 'left':
      self.ship.steer_x(-20)
    elif keycode[1] == 'right':
      self.ship.steer_x(20)
    elif keycode[1] == 'up':
      self.ship.steer_y(20)
    elif keycode[1] == 'down':
      self.ship.steer_y(-20)
    elif keycode[1] == 'd':
      missile = Projectile('missile', 0, 10, 'human')
      missile.size = 75, 75
      missile.x = self.ship.get_center_x() - missile.width / 2
      missile.y = self.ship.y + self.ship.height
      self.add_widget(missile)
    elif keycode[1] == 's':
      # if self.sfx_laser.state == 'play':
        # self.sfx_laser.stop()
      self.sfx_laser.play()
      laser1 = Projectile('laser', 0, 20, 'human')
      laser1.x = self.ship.x + self.ship.width * .35
      laser1.y = self.ship.y + self.ship.height / 10
      self.add_widget(laser1)
      laser2 = Projectile('laser', 0, 20, 'human')
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
    if self.counter % (160 - self.accel) == 0:
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
    if self.counter % (80 - self.accel) == 0:
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
    if self.counter % (120 - self.accel) == 0:
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
    if self.counter % (60 - self.accel) == 0:
      for saucer in self.saucers:
        bullet1 = Projectile('bullet', 0, -10, 'computer')
        bullet1.x = saucer.center_x - bullet1.width/2
        bullet1.y = saucer.y - saucer.height/2
        self.add_widget(bullet1)
        bullet2 = Projectile('bullet', -7, -7, 'computer')
        bullet2.x = saucer.center_x - bullet2.width/2 - saucer.width * .4
        bullet2.y = saucer.y - saucer.height/2
        self.add_widget(bullet2)
        bullet3 = Projectile('bullet', 7, -7, 'computer')
        bullet3.x = saucer.center_x - bullet3.width/2 + saucer.width * .4
        bullet3.y = saucer.y - saucer.height/2
        self.add_widget(bullet3)
      
  def anim_objects(self, dt):
    self.counter += 1
    self.accel = max(30, self.counter / 200)
    self.spawn_drone()
    self.spawn_saucer()
    self.fire_drone()
    self.fire_saucer()
    for child in self.children:
      if not check_classname(child, 'Explosion'):
        # movement
        if child.dx or child.dy:
          child.x += child.dx
          child.y += child.dy
        # collision check
        if check_classname(child, 'Projectile'):
          projectile = child
          if projectile.player == 'human':
            for drone in self.drones:
              if projectile.collide_widget(drone):
                self.inc_score(1)
                self.explosion(drone.x, drone.y)
                self.remove_widget(projectile)
                self.remove_widget(drone)
                self.drones.remove(drone)
                # if self.sfx_explo.state == 'play':
                  # self.sfx_explo.stop()
                
            for saucer in self.saucers:
              if projectile.collide_widget(saucer):
                self.inc_score(1)
                self.explosion(saucer.x, saucer.y)
                self.remove_widget(projectile)
                self.remove_widget(saucer)
                self.saucers.remove(saucer)
                # if self.sfx_explo.state == 'play':
                  # self.sfx_explo.stop()
          elif projectile.player == 'computer':
            if projectile.collide_widget(self.ship):
              self.remove_widget(projectile)
              self.ship.shield -= 1
              self.update_health() 
              self.blink()  
                
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
    lbl_fps.text = 'FPS: %.2f' % Clock.get_fps()
    # game over
    if self.ship.shield <= 0:
      popup = Popup(title='GAME OVER',
        content=Label(text='Score: %s' % self.score),
        size_hint=(None, None), size=(400, 400))
      popup.open()
      popup.bind(on_dismiss=self.app_close)
      return False
    
  def explosion(self, x, y):
    self.sfx_explo.play()
    self.img_explo.append(Explosion(x, y))
    self.add_widget(self.img_explo[-1])
    Clock.schedule_once(self.clear_explosion, 1)

  def clear_explosion(self, dt):
    if len(self.img_explo) > 0:
      self.remove_widget(self.img_explo[0])
      del self.img_explo[0]
      
  def blink(self):
    self.ship.source = 'img/ship_blink.zip'
    Clock.schedule_once(self.clear_blink, 1)

  def clear_blink(self, dt):
    self.ship.source = 'img/ship.png'
      
  def update_health(self):
    self.lifebar.pos = 0, self.height * .95
    self.lifebar.size = self.width/2 * self.ship.shield / 100., self.height * .05 
    # lbl_hp.text = str(self.ship.shield) + '/' + '100'
    
  def inc_score(self, value):
    self.score += value
    lbl_score.text = 'SCORE: %s' % self.score
    
  def app_close(self, *args):
    App.get_running_app().stop()
      
    
game = Game()
lbl_fps = Label(pos_hint={'center_x': .95, 'center_y': .95})
# lbl_hp = Label(pos_hint={'center_x': .1, 'center_y': .95})
lbl_score = Label(pos_hint={'center_x': .95, 'center_y': .90})
root_widget.add_widget(game)
root_widget.add_widget(lbl_fps)
# root_widget.add_widget(lbl_hp)
root_widget.add_widget(lbl_score)
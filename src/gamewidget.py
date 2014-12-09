from random import randint

from kivy.app import App
from kivy.animation import Animation
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_pygame import SoundPygame
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from dialog.gameover import GameOver
from dialog.newgame import NewGame
from drone import Drone
from explosion import Explosion
from musicplayer import MusicPlayer
from projectile import Projectile
from saucer import Saucer
from ship import Ship
from util import check_classname


# music = SoundLoader.load('music/1 - Bishopric Of Cambrai - Day Of The Dispair.mp3')
# music = SoundLoader.load('sfx/laser.wav')
# music.loop = True
# music.play()
# Config.set('graphics', 'fullscreen', 'auto')
# Config.set('graphics', 'borderless', 1)
Window.fullscreen = 'auto'


class GameWidget(Widget):

  def __init__(self, root_widget, **kw):
    super(GameWidget, self).__init__(**kw)
    self.root_widget = root_widget
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
    self.level = 0
    self.drones = []
    self.saucers = []
    Clock.schedule_interval(self.update_game, 1./60)
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
      self.root_widget.close_app()
    if keycode[1] == 'left':
      self.ship.steer_x(-20)
    elif keycode[1] == 'right':
      self.ship.steer_x(20)
    elif keycode[1] == 'up':
      self.ship.steer_y(20)
    elif keycode[1] == 'down':
      self.ship.steer_y(-20)
    elif keycode[1] == 'f' and not self.ship.is_shielded and self.ship.cooldown == 0:
      self.ship.cooldown = 25
      missile = Projectile('missile', 0, 10, 'human')
      missile.score_bonus = 5
      missile.size = 75, 75
      missile.x = self.ship.get_center_x() - missile.width / 2
      missile.y = self.ship.y + self.ship.height
      self.add_widget(missile)
    elif keycode[1] == 's' and not self.ship.is_shielded and self.ship.cooldown == 0:
      # if self.sfx_laser.state == 'play':
        # self.sfx_laser.stop()
      self.ship.cooldown = 5   
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
      self.ship.toggle_shield()
    # elif keycode[1] == 'q':
      # self.ship.shield('green')
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
    if self.counter % (60 - self.level*2) == 0:
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
    for drone in self.drones:
      if drone.counter > (30 * self.level_mod):
        drone.counter = 0
        bullet1 = Projectile('bullet', 0, -10, 'computer')
        bullet1.x = drone.center_x - bullet1.width/2 + drone.width * .4
        bullet1.y = drone.y
        self.add_widget(bullet1)
        bullet2 = Projectile('bullet', 0, -10, 'computer')
        bullet2.x = drone.center_x - bullet2.width/2 - drone.width * .4
        bullet2.y = drone.y
        self.add_widget(bullet2)
      else: drone.counter += 1
        
  def spawn_saucer(self):
    if self.counter % (90 - self.level*2) == 0:
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
    for saucer in self.saucers:
      if saucer.counter > (30 * self.level_mod):
        saucer.counter = 0
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
      else: saucer.counter += 1
      
  def update_game(self, dt):
    self.counter += 1
    if self.ship.cooldown:
      self.ship.cooldown -= 1
    level = self.counter / 600
    if level == 20:
      self.ship.hp = 0
    if level > self.level:
      self.level = level
      self.root_widget.ids['level'].text = 'LEVEL: %s' % (self.level + 1)
      self.ship.hp = self.ship.hp_max
      self.update_health()
    self.level_mod = (1 - self.level/40.)
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
                self.inc_score(projectile.score_bonus)
                self.explosion(drone.x, drone.y)
                self.remove_widget(projectile)
                self.remove_widget(drone)
                self.drones.remove(drone)
                # if self.sfx_explo.state == 'play':
                  # self.sfx_explo.stop()
                
            for saucer in self.saucers:
              if projectile.collide_widget(saucer):
                self.inc_score(projectile.score_bonus)
                self.explosion(saucer.x, saucer.y)
                self.remove_widget(projectile)
                self.remove_widget(saucer)
                self.saucers.remove(saucer)
                # if self.sfx_explo.state == 'play':
                  # self.sfx_explo.stop()
          elif projectile.player == 'computer':
            if projectile.collide_widget(self.ship):
              self.remove_widget(projectile)
              if not self.ship.is_shielded:
                self.ship.hp -= 1
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
    self.root_widget.ids['fps'].text = 'FPS: %.2f' % Clock.get_fps()
    # game over
    if self.ship.hp <= 0:
      go_popup = GameOver(self.root_widget)
      go_popup.set_score(self.score)
      go_popup.open()
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
    self.lifebar.size = self.width/2 * self.ship.hp / self.ship.hp_max, self.height * .05 
    # lbl_hp.text = str(self.ship.shield) + '/' + '100'
    
  def inc_score(self, value):
    self.score += value
    self.root_widget.ids['score'].text = 'SCORE: %s' % self.score
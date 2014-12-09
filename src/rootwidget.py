from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

from gamewidget import GameWidget
from musicplayer import MusicPlayer


class RootWidget(RelativeLayout):

  def __init__(self, **kw):
    super(RootWidget, self).__init__(**kw)
    
  def new_game(self):
    self.clear_widgets()
    
    game_widget = GameWidget(self) #level = x
    self.add_widget(game_widget)
    self.ids['game'] = game_widget
    
    lbl_fps = Label(pos_hint={'center_x': .95, 'center_y': .95})
    self.add_widget(lbl_fps)
    self.ids['fps'] = lbl_fps
    
    lbl_score = Label(pos_hint={'center_x': .95, 'center_y': .90})
    self.add_widget(lbl_score)
    self.ids['score'] = lbl_score

    musicplayer = MusicPlayer()
    musicplayer.start()

  def close_app(self, *args):
    App.get_running_app().stop()
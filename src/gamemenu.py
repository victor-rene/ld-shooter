from kivy.uix.label import Label

from __main__ import root_widget
from gamewidget import GameWidget
from musicplayer import MusicPlayer


class GameMenu(object):

  @staticmethod
  def new_game():
    root_widget.clear_widgets()
    
    game_widget = GameWidget() #level = x
    root_widget.add_widget(game_widget)
    root_widget.ids['game'] = game_widget
    
    lbl_fps = Label(pos_hint={'center_x': .95, 'center_y': .95})
    root_widget.add_widget(lbl_fps)
    root_widget.ids['fps'] = lbl_fps
    
    lbl_score = Label(pos_hint={'center_x': .95, 'center_y': .90})
    root_widget.add_widget(lbl_score)
    root_widget.ids['score'] = lbl_score

    musicplayer = MusicPlayer()
    musicplayer.start()
    
  @staticmethod
  def close_app(*args):
    App.get_running_app().stop()
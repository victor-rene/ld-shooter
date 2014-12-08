from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout

from __main__ import root_widget
from userdata import load_data, write_data


class GameOver(Popup):
  
  def __init__(self, **kw):
    super(GameOver, self).__init__(**kw)
    self.title = 'GAME OVER'
    self.layout = RelativeLayout()
    self.btn_new_game = Button(text='New Game', size_hint=(.5,.1), pos_hint={'center_x':.25, 'center_y': .05})
    self.btn_new_game.bind(on_press=self.new_game)
    self.btn_exit = Button(text='Exit', size_hint=(.5,.1), pos_hint={'center_x':.75, 'center_y': .05})
    self.btn_exit.bind(on_press=self.app_close)
    self.lbl_score = Label(size_hint=(.5,.1), pos_hint={'center_x':.5, 'center_y': .4})
    self.lbl_high_score = Label(size_hint=(.5,.1), pos_hint={'center_x':.5, 'center_y': .7})
    self.layout.add_widget(self.lbl_score)
    self.layout.add_widget(self.lbl_high_score)
    self.layout.add_widget(self.btn_new_game)
    self.layout.add_widget(self.btn_exit)
    self.content = self.layout
    self.size_hint = (None, None)
    self.size = (400, 400)
        
  def set_score(self, score):
    high_score = load_data('data/score.txt')
    if score > high_score:
      high_score = score
      write_data('data/score.txt', score)
    self.lbl_score.text = 'Score: %s' % score
    self.lbl_high_score.text = 'High Score: %s' % high_score
    
  def app_close(self, *args):
    App.get_running_app().stop()
  
  def new_game(self, *args):
    root_widget.clear_widgets()
    import game
    reload(game)
    self.dismiss()
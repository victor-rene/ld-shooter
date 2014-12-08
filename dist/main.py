import sys
from threading import Thread
from Queue import Queue, Empty

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout


def enqueue_input(input, queue):
  for line in iter(input.readline, b''):
    queue.put(line)
  input.close()


q = Queue()
t = Thread(target=enqueue_input, args=(sys.stdin, q))
t.daemon = True # thread dies with the program
t.start()


def read_line(dt):
  # read line without blocking
  try:  line = q.get_nowait() # or q.get(timeout=.1)
  except Empty:
    pass
  else: # got line
    line = line.strip()
    if line:
      exec(line)


class RootWidget(RelativeLayout):

  def __init__(self, **kw):
    super(RootWidget, self).__init__(**kw)


root_widget = RootWidget()
user_data = dict()


class GameApp(App):

  def build(self):
    return root_widget


if __name__ == '__main__':
  print sys.argv, sys.argv[-1] == 'prod'
  if sys.argv[1] == 'prod':
    import game
  else: Clock.schedule_interval(read_line, 0.1)
  GameApp().run()
import sys
from threading import Thread
from Queue import Queue, Empty

from kivy.app import App
from kivy.clock import Clock

from rootwidget import RootWidget


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


root_widget = RootWidget()


class GameApp(App):

  def build(self):
    return root_widget

   
if __name__ == '__main__':
  if len(sys.argv) > 1 and sys.argv[1] == 'dev':
    Clock.schedule_interval(read_line, 0.1)
  else: root_widget.new_game()
  GameApp().run()
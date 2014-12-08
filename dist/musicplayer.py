import os
import pygame.mixer_music

from random import randint


pygame.mixer.init()
dirname = os.path.dirname(os.path.realpath(__file__))


class MusicPlayer(object):

  def __init__(self):
    self.folder = 'music'
    # self.current = 0
    self.count = 0
    self.tracks = []
    filename = os.path.join(dirname, self.folder, 'list.txt')
    with open(filename) as f:
      for line in f.readlines():
        self.tracks.append(line.strip())
        self.count += 1
        
  def start(self):
    # self.play(randint(1, self.count))
    first = randint(0, self.count - 1)
    pygame.mixer.music.load(os.path.join(dirname, self.folder, self.tracks[first]))
    for i in range(1, self.count):
      next = (i + first) % (self.count - 1)
      pygame.mixer.music.queue(os.path.join(dirname, self.folder, self.tracks[next]))
    pygame.mixer.music.play()
  
  # def play(self, index):
    # for track in self.tracks:
      # if track.startswith(str(index) + ' '):
        # pygame.mixer.music.load(os.path.join(dirname, 'music',  track))
        # # TODO: learn to scan pygame events to setup callback when track ends
        # pygame.mixer.music.play()
        # return
    
  # def next(self, *args):
    # if self.current < self.count:
      # self.current += 1
    # else: self.current = 1
    # self.play(self.current)
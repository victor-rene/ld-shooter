import sys

if len(sys.argv) > 1:
  filename = sys.argv[1]
  with open(filename, 'r') as f:
    for line in f:
      print line
      sys.stdout.flush()
  
while True:
  try:
    input = raw_input()
    if input != 'exit()':
      print input
      sys.stdout.flush()
    else: break
  except (EOFError):
    break #end of file reached (file stream redirection)
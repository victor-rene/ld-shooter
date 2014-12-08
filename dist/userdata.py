def load_data(filename):
  data = None
  with open(filename, 'r') as f:
    data = f.read()
  return eval(data.strip())
  
def write_data(filename, data):
  with open(filename, 'w') as f:
    f.write(repr(data))
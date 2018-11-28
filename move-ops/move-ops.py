#! usr/bin/python

"""A script for generating moving operation commands.

DESCRIPTIONS:
  Given two inpurt records A and B in the follwing format:
  A:       B:
  1,1,1    1,2,10
  1,1,2    1,2,11
  1,1,3    1,2,12
  ...      ...
  2,1,1    2,3,3
  2,2,2    2,1,1
  2,3,3    2,2,2
  Transform the data into a chunked data format as:
  A or B:
  [1.1, [1, 2, 3...]]
  Generate moving operation command (MoveUp [number of steps] at [cell id]) sequences as:
  MoveUp 1 at 3
  MoveUp 2 at 6
  ...
"""

import csv

def read_data(path):
  """ Read data from a file and transform data into chunk format
  """
  with open(path) as file:
    # Read data from file
    raw = csv.reader(file)
    print('==== RAW DATA IN FILE ====')
    for row in raw:
      print(row)

    # Transform data into chunk format
    file.seek(0)
    data = []
    key = [-1, -1]
    value = []
    for row in raw:
      rec = [int(x) for x in row]
      if(key[0] < 0 and key[1] < 0):
        key[0] = rec[0]
        key[1] = rec[1]
        value.append(rec[2])
        continue
      else:
        if(key[0] == rec[0] and key[1] == rec[1]):
          value.append(rec[2])
        else:
          data.append([key.copy(), value.copy()])
          key[0] = rec[0]
          key[1] = rec[1]
          value[:] = []
          value.append(rec[2])
    data.append([key.copy(), value.copy()])
    print('==== CHUNK DATA IN FILE ===')
    for rec in data:
      print(rec)

def main():
  """ Main entry
  """
  # Import data from A
  read_data('data/A.csv')
  # read_data('data/B.csv')

# Scrip entry
if __name__ == '__main__':
    main()

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
  Generate moving operation command (MoveUp/MoveDown [number of steps] at [cell id]) sequences as:
  MoveUp 1 at 3
  MoveUp 2 at 6
  MoveDown 1 at 4
  ...
"""

import csv

def read_data(path):
  """ Read data from a file and transform data into chunk format
  """
  with open(path) as file:
    # Read data from file
    raw = csv.reader(file)

    # Transform data into chunk format
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

  # Return data in chunk format
  return data

def get_real_idx(data, idx):
  """Evaluate the real index of data based on the index obtained of chunk data
  """
  real_idx = 0
  for i in range (0, idx):
    real_idx += len(data[i][1])
  return real_idx

def generate_moveop_commands(data_A, data_B):
  """Generate moveop command sequence according to data A and data B,
  so that data A can be rearranged into data B
  """
  for idx_B, rec_B in enumerate(data_B):
    key = rec_B[0]
    for idx_A, rec_A in enumerate(data_A):
      if key == rec_A[0]:
        delta = idx_A - idx_B
        if(delta != 0):
          real_idx_A = get_real_idx(data_A, idx_A)
          if(delta > 0):
            print('Move up the cell ' + str(real_idx_A) + ' of A ' + str(delta) + ' steps')
          elif(delta < 0):
            print('Move down the cell ' + str(real_idx_A) + ' of A ' + str(-delta) + ' steps')
          data_A.insert(idx_B, data_A.pop(idx_A))
        break

  # Check A after movment if it's the same as B
  assert(data_A == data_B)

def main():
  """ Main entry
  """
  # Import data from A and B
  data_A = read_data('data/A.csv')
  data_B = read_data('data/B.csv')

  # Generate operation movement command sequence
  generate_moveop_commands(data_A, data_B)

# Scrip entry
if __name__ == '__main__':
    main()

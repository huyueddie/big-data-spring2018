for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  df['hour'].replace(range(j, j + 5, 1), range(-5, 0, 1), inplace=True)
  df['hour'].replace(range(i, i + 19, 1), range(0, 19, 1), inplace=True)

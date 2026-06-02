def minimum(list):
  min = list[0]
  for i in list:
    if min > i:
      min = i
  return min

print(minimum([1,4,0]))


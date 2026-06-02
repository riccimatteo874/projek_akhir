def minimum(list):
  min = list[0]
  for i in list:
    if min > i:
      min = i
  return min

print(minimum([1,4,0]))

def man_isdigit(teks):
  if len(teks) < 1:
    return False
  angka = '0123456789'
  for i in teks:
    if i not in angka:
      return False
  return True
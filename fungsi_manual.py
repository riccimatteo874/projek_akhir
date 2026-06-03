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

def man_split(teks, pemisah):
  hasil = []
  temp_kata = ""
  for char in teks:
    if char == pemisah:
      hasil.append(temp_kata)
      temp_kata = ""
    else:
      temp_kata += char
  hasil.append(temp_kata)
  return hasil
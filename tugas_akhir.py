# CLASS PLAYER, ENEMY, ITEM, SKILL
class Entitas:
  def __init__(self, nama, hp=100, attack=10):
    self.nama = nama
    self.hp = hp
    self.max_hp = hp
    self.attack = attack

class NodeSkill:
  def __init__(self, nama_skill):
    self.nama = nama_skill
    self.left = None
    self.right = None

class Player(Entitas):
  def __init__(self, nama, role='fighter'):
    super().__init__(nama)
    self.exp = 0
    self.score = 0
    self.level = 1
    self.role = role
    self.gold = 0
    self.inventory = Inventory()
    self.skill_tree = NodeSkill('Lvl 1: Tebasan Pedang')
    self.buruan = set()

    if role == 'tank':
      self.hp = 150
      self.max_hp = 150
      self.attack = 5
      self.skill_tree = NodeSkill('Lvl 1: Hantaman Perisai')
    elif role == 'marksman':
      self.hp = 80
      self.max_hp = 80
      self.attack = 15
      self.skill_tree = NodeSkill('Lvl 1: Panah Kilat')

class Enemy(Entitas):
  def __init__(self, nama, hp, attack, reward_gold):
    super().__init__(nama, hp, attack)
    self.reward_gold = reward_gold

class Item:
  def __init__(self, nama, jenis, power, harga):
    self.nama = nama
    self.jenis = jenis
    self.power = power
    self.harga = harga

class Inventory:
  def __init__(self):
    self.items = []

  def tambah_item(self, item):
    self.items.append(item)

  def tampilkan_item(self):
    if not self.items:
      return False
    for i, item in enumerate(self.items):
      print(f'{i+1}. {item.nama}: {item.jenis} + {item.power}')
    return True

  def hapus_item(self, index):
    if 0 < index <= len(self.items):
      return self.items.pop(index-1)
    return None

toko = [
  Item('heal potion', 'heal', 30, 30),
  Item('attack potion', 'buff', 10, 30)
]

#================================================

# CLASS UNTUK LEADERBOARD ENEMY
class NodeEnemy: # BINARY SEARCH TREE
  def __init__(self, enemy):
    self.enemy = enemy
    self.left = None
    self.right = None

class BountyBoard: # BINARY SEARCH TREE
  def __init__(self):
    self.root = None

  def insert(self, enemy):
    if self.root is None:
      self.root = NodeEnemy(enemy)
    else:
      self.rekursif_insert(self.root, enemy)

  def rekursif_insert(self, node, enemy):
    if enemy.reward_gold < node.enemy.reward_gold:
      if node.left is None:
        node.left = NodeEnemy(enemy)
      else:
        self.rekursif_insert(node.left, enemy)
    elif enemy.reward_gold > node.enemy.reward_gold:
      if node.right is None:
        node.right = NodeEnemy(enemy)
      else:
        self.rekursif_insert(node.right, enemy)

  def tampilkan_board(self, node, nomor = None):
    if nomor is None:
      nomor = [1]
    if node:
      self.tampilkan_board(node.right, nomor)
      print(f"{nomor[0]}. {node.enemy.nama} | HP: {node.enemy.hp} | Atk: {node.enemy.attack} | Hadiah: {node.enemy.reward_gold} Gold") 
      nomor[0] += 1
      self.tampilkan_board(node.left, nomor)
  
  def search_target(self, node, target_gold):
    if node is None or node.enemy.reward_gold == target_gold:
      return node
    if target_gold < node.enemy.reward_gold:
      return self.search_target(node.left, target_gold)
    return self.search_target(node.right, target_gold)
#===================================================================================================================================

# CLASS UNTUK DATA PEMAIN
class NodePlayer(): #single linked list
  def __init__(self, player):
    self.player = player
    self.next = None

class PlayerList(): # SINGLE LINKED LIST
  def __init__(self):
    self.head = None

  def tambah_pemain(self, player):
    new = NodePlayer(player)
    new.next = self.head
    self.head = new
  
  def get_pemain(self, user):
    temp = self.head
    while temp:
      if temp.player.nama == user:
        return temp.player
      temp = temp.next
    return None
#================================================================================================

# CLASS UNTUK HISTORY PERMAINAN
class NodeHistory: # DOUBLE LINKED LIST
  def __init__(self, log):
    self.log = log
    self.prev = None
    self.next = None

class GameHistory:
  def __init__(self):
    self.head = self.tail = None
  
  def add_log(self, log):
    new_node = NodeHistory(log)
    if not self.head:
      self.head = self.tail = new_node
    else:
      new_node.prev = self.tail
      self.tail.next = new_node
      self.tail = new_node
  
  def tampilkan(self):
    curr = self.head
    if not curr:
      print('Belum ada riwayat permainan')
      return
    print('Riwayat Permainan')
    while curr:
      print(f'>> {curr.log}')
      curr = curr.next
#===========================================================================================

# CLASS UNTUK SYSTEM BATTLE
class NodeBattle:
  def __init__(self, entitas):
    self.entitas = entitas
    self.next = None

class Battle: # CIRCULAR LINKED LIST
  def __init__(self):
    self.head = None
    self.current = None

  def tambah_unit(self, unit):
    new_node = NodeBattle(unit)
    if not self.head:
      self.head = new_node
      new_node.next = self.head
    else:
      temp = self.head
      while temp.next != self.head:
        temp = temp.next
      temp.next = new_node
      new_node.next = self.head
    self.current = self.head
#=====================================================================================

# CLASS UNTUK MODE SURVIVAL
class Survival: # QUEUE
  def __init__(self):
    self.antrian = []

  def enqueue(self, enemy):
    self.antrian.append(enemy)

  def dequeue(self):
    if self.antrian:
      return self.antrian.pop(0)
    else:
      return None

  def is_empty(self):
    return len(self.antrian) == 0
#===============================================================================

# CLASS UNTUK LOGIN PEMAIN
class Login(): # hash table 
  def __init__(self, size=10):
    self.size = size
    self.table = [[] for _ in range(size)]

  def hash(self, key):
    jumlah = sum(ord(i) for i in key)
    return jumlah % self.size

  def register(self, username, pw):
    index = self.hash(username)
    for item in self.table[index]:
      if item[0] == username:
        return False 
    self.table[index].append((username, pw))
    return True

  def cek(self, username, pw):
    index = self.hash(username)
    for item in self.table[index]:
      if item[0] == username and item[1] == pw:
        return True
    return False
#====================================================================================================

# CLASS UNTUK MAP ARENA
class GameMap: # GRAPH
  def __init__(self):
    self.adj_list = {
      "Desa Petualang": [["Hutan Terlarang"], Enemy("Slime", 30, 5, 20)],
      "Hutan Terlarang": [["Desa Petualang", "Gua Naga"], Enemy("Goblin", 60, 12, 50)],
      "Gua Naga": [["Hutan Terlarang"], Enemy("Naga Hitam", 150, 25, 200)] 
    }
#=====================================================================================================

#****************************
#FUNGSI FUNGSI UNTUK DI MAIN 
#****************************

# QUICK SORT UNTUK LEADERBOARD PEMAIN
def manual_quick_sort(arr): 
  if len(arr) <= 1: return arr
  pivot = arr[len(arr)//2].score
  left = [x for x in arr if x.score > pivot]
  mid = [x for x in arr if x.score == pivot]
  right = [x for x in arr if x.score < pivot]
  return manual_quick_sort(left) + mid + manual_quick_sort(right)
#=========================================================================================

#FUNGSI UNTUK BERPINDAH MAP
def navigasi_map(sekarang, game_map): #REKURSIF
  print(f'\nLokasi saat ini: {sekarang}')
  option = game_map.adj_list[sekarang][0]
  print('Lokasi yang terhubung:')
  for i, lokasi in enumerate(option):
    print(f'{i+1}. Pergi ke {lokasi}')
  print('0. Berhenti')
  try:
    pilih = int(input('Pilih: '))
    if pilih == 0:
      return sekarang
    elif 0 < pilih <= len(option):
      next_map = option[pilih-1] 
      print(f'Menuju {next_map}')
      return navigasi_map(next_map, game_map)
    else:
      print('Tidak valid')
      return navigasi_map(sekarang, game_map)
  except ValueError:
    print('Input Angka')
    return navigasi_map(sekarang, game_map)

# FUNGSI UNTUK MEMILIH SKILL BARU SAAT NAIK LEVEL 3 DAN 5
def menu_pilih_skill_baru(player): # BINARY TREE
  if player.level == 3:
    print(f"\n=== ✨ SELAMAT NAIK LEVEL 3! SILAKAN PILIH 1 DARI 2 SKILL BARU ✨ ===")
    
    if player.role == "fighter": 
      print("1. Lvl 3: Pukulan Berat (Attack Type)\n2. Lvl 3: Semangat Juang (Heal Type)")
      pilih = input("Pilihanmu (1/2): ")
      if pilih == '1' :
        player.skill_tree.left = NodeSkill("Lvl 3: Pukulan Berat (Attack)")
        print(f"-> Berhasil Mempelajari: {player.skill_tree.left.nama}!") 
      else:
        player.skill_tree.right = NodeSkill("Lvl 3: Semangat Juang (Heal)")
        print(f"-> Berhasil Mempelajari: {player.skill_tree.right.nama}!")

    elif player.role == "tank":
      print("1. Lvl 3: Guncang Dunia (Attack Type)\n2. Lvl 3: Keberanian (Heal Type)")
      pilih = input("Pilihanmu (1/2): ")
      if pilih == '1':
        player.skill_tree.left = NodeSkill("Lvl 3: Guncang Dunia (Attack)")
        print(f"-> Berhasil Mempelajari: {player.skill_tree.left.nama}!")
      else:
        player.skill_tree.right = NodeSkill("Lvl 3: Keberanian (Heal)")
        print(f"-> Berhasil Mempelajari: {player.skill_tree.right.nama}!")

    elif player.role == "marksman":
      print("1. Lvl 3: Hujan Panah (Attack Type)\n2. Lvl 3: Kegigihan Pemanah (Heal Type)")
      pilih = input("Pilihanmu (1/2): ")
      if pilih == '1':
        player.skill_tree.left = NodeSkill("Lvl 3: Hujan Panah (Attack)")
        print(f"-> Berhasil Mempelajari: {player.skill_tree.left.nama}!")
      else:
        player.skill_tree.right = NodeSkill("Lvl 3: Kegigihan Pemanah (Heal)")
        print(f"-> Berhasil Mempelajari: {player.skill_tree.right.nama}!")

  elif player.level == 5:
    print(f"\n=== ✨ SELAMAT NAIK LEVEL 5! SILAKAN PILIH 1 DARI 2 SKILL ULTIMATE ✨ ===")
    parent_node = player.skill_tree.left if player.skill_tree.left else player.skill_tree.right

    if player.role == "fighter":
      print("1. Lvl 5: Tebasan Pemutus Langit (Attack Type)\n2. Lvl 5: Meditasi Ksatria (Heal Type)")
      pilih = input("Pilihanmu (1/2): ")
      if pilih == '1':
        parent_node.left = NodeSkill("Lvl 5: Tebasan Pemutus Langit (Attack)")
        print(f"-> Berhasil Mempelajari Ultimate: {parent_node.left.nama}!")
      else:
        parent_node.right = NodeSkill("Lvl 5: Meditasi Ksatria (Heal)")
        print(f"-> Berhasil Mempelajari Ultimate: {parent_node.right.nama}!")

    elif player.role == "tank":
      print("1. Lvl 5: Amukan Bumi (Attack Type)\n2. Lvl 5: Benteng Abadi (Heal Type)")
      pilih = input("Pilihanmu (1/2): ")
      if pilih == '1':
        parent_node.left = NodeSkill("Lvl 5: Amukan Bumi (Attack)")
        print(f"-> Berhasil Mempelajari Ultimate: {parent_node.left.nama}!")
      else:
        parent_node.right = NodeSkill("Lvl 5: Benteng Abadi (Heal)")
        print(f"-> Berhasil Mempelajari Ultimate: {parent_node.right.nama}!")

    elif player.role == "marksman":
      print("1. Lvl 5: Tembakan Badai (Attack Type)\n2. Lvl 5: Angin Penyembuh (Heal Type)")
      pilih = input("Pilihanmu (1/2): ")
      if pilih == '1':
        parent_node.left = NodeSkill("Lvl 5: Tembakan Badai (Attack)")
        print(f"-> Berhasil Mempelajari Ultimate: {parent_node.left.nama}!")
      else:
        parent_node.right = NodeSkill("Lvl 5: Angin Penyembuh (Heal)")
        print(f"-> Berhasil Mempelajari Ultimate: {parent_node.right.nama}!")

# FUNGSI UNTUK MENU SHOP
def shop_menu(player):
  global toko
  print(f'\n=====SHOP=====')
  print(f'gold: {player.gold}')
  for i, item in enumerate(toko):
    print(f'{i+1}. {item.nama} {item.jenis} + {item.power}\nprice: {item.harga} gold')
  
  try:
    pilih = int(input('Beli (Input nomor, 0 untuk batal): '))
    if 0 < pilih <= len(toko): 
      item = toko[pilih-1]
      if player.gold >= item.harga:
        player.gold -= item.harga
        player.inventory.tambah_item(item)
        print(f'{item.nama} berhasil dibeli') 
      else:
        print('Gold tidak cukup')
  except ValueError:
    print('Masukkan nomor yang valid!')
#===========================================================================================

# FUNGSI UNTUK MENGGUNAKAN ITEM DI BATTLE
def use_item(player):
  print('\nINVENTORY')
  if not player.inventory.tampilkan_item():
    print('Tas Kosong')
    return False
  try:
    pilih = int(input('Gunakan Item (Input nomor, 0 untuk batal): '))
    if pilih > 0:
      item = player.inventory.hapus_item(pilih)
      if item:
        if item.jenis == 'heal':
          player.hp = minimum([player.max_hp, player.hp + item.power])
          print(f'{item.nama} telah digunakan. Hp saat ini: {player.hp}')
        elif item.jenis == 'buff':
          player.attack += item.power
          print(f'{item.nama} telah digunakan. Attack saat ini: {player.attack}')
        return True
  except ValueError:
    print('Masukkan nomor yang valid!')
  return False
#================================================================================================

# FUNGSI UNTUK MENAMPILKAN SKILL TREE PEMAIN
def tampilkan_skill(node, level=0):
  if node:
    print('  '* level + '└─ ' + node.nama) 
    tampilkan_skill(node.left, level + 1)
    tampilkan_skill(node.right, level + 1)
#=================================================================================================

# FUNGSI UNTUK MENGAMBIL SKILL YANG SUDAH DIPILIH
def get_skills(node, result):
  if node is not None:
    result.append(node.nama)
    get_skills(node.left, result)
    get_skills(node.right, result)
  return result
#==================================================================================================

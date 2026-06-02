from fungsi_manual import minimum, man_isdigit
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
  
  def hapus_pemain(self, user):
    temp = self.head
    prev = None
    while temp:
      if temp.player.nama == user:
        if prev:
          prev.next = temp.next
        else:
          self.head = temp.next
        return True
      prev = temp
      temp = temp.next
    return False
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
  
  def hapus_akun(self, username):
    index = self.hash(username)
    for i, item in enumerate(self.table[index]):
      if item[0] == username:
        self.table[index].pop(i) # Hapus data dari list dalam Hash Table
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

# FUNGSI UNTUK BATTLE SYSTEM
def battle_system(player, enemy, history):
  turns = Battle()
  turns.tambah_unit(player)
  turns.tambah_unit(enemy)
  stack_aksi = []

  print(f'\n⚔️ Bertarung melawan {enemy.nama} ⚔️')
  while player.hp > 0 and enemy.hp > 0:
    unit = turns.current.entitas
    if unit.nama == player.nama:
      print(f'\nStatus:\nHp: {unit.hp}/{unit.max_hp} Attack: {unit.attack}')
      print('1. Serang / 2. Skill / 3. Item / 4. Undo')
      pilih = input('Aksi: ')

      snapshot_status = (player.hp, player.attack, enemy.hp, list(player.inventory.items))

      if pilih == '1':
        enemy.hp -= unit.attack
        log = f'{unit.nama} menyerang {enemy.nama} -{unit.attack} hp'
        stack_aksi.append((snapshot_status, log)) 

      elif pilih == '2':
        skills = []
        get_skills(unit.skill_tree, skills)
        print('\n--- Skill ---')
        for i, skl in enumerate(skills):
          print(f'{i+1}. {skl}')
        print('0. Batal')
        pilihan_skill = input('Gunakan skill? ')
        if man_isdigit(pilihan_skill) and 0 < int(pilihan_skill) <= len(skills):
          nama_skill = skills[int(pilihan_skill)-1]

          if 'Lvl 1' in nama_skill:
            damage = int(unit.attack * 1.5)
            enemy.hp -= damage
            log = f'{unit.nama} menggunakan skill {nama_skill}, {enemy.nama} terkena {damage} damage.'
          
          elif 'Lvl 3' in nama_skill:
            if 'Heal' in nama_skill:
              heal = int(unit.max_hp * 0.4)
              unit.hp = minimum([unit.max_hp, unit.hp + heal])
              log = f'{unit.nama} menggunakan {nama_skill}, memulihkan {heal} hp.'
            else:
              damage = int(unit.attack * 2.0)
              enemy.hp -= damage
              log = f'{unit.nama} menggunakan {nama_skill}, {enemy.nama} terkena {damage} damage.'
          
          elif 'Lvl 5' in nama_skill:
            if 'Heal' in nama_skill:
              heal = int(unit.max_hp * 0.7)
              unit.hp = minimum([unit.max_hp, unit.hp + heal])
              log = f'{unit.nama} menggunakan {nama_skill}, memulihkan {heal} hp.'
            else:
              damage = int(unit.attack * 3.0)
              enemy.hp -= damage
              log = f'{unit.nama} menggunakan {nama_skill}, {enemy.nama} terkena {damage} damage.'
          
          stack_aksi.append((snapshot_status, log)) 
          print(f'>>>{log}')
        
        else:
          continue

      elif pilih == '3':
        if not use_item(player):
          continue

        log = f'{unit.nama} menggunakan item dari tas.'
        stack_aksi.append((snapshot_status, log))
      
      elif pilih == '4':
        if stack_aksi:

          data_lama, teks_log = stack_aksi.pop()
          player.hp, player.attack, enemy.hp, tas_lama = data_lama
          
          player.inventory.items = list(tas_lama) 
          
          print(f'\n⏪ Membatalkan aksi: {teks_log}')
          print(f'✨ Waktu diputar mundur! HP Player, HP Musuh, dan Isi Tas kembali seperti semula.')
          continue
        else:
          print('\n❌ Belum ada aksi yang bisa di-undo!')
          continue
          
      else:
        continue
    else:
      player.hp -= unit.attack
      print(f'{unit.nama} menyerang! Hp = {player.hp}')

    turns.current = turns.current.next
  
  if player.hp > 0:
    hadiah_exp = int(enemy.reward_gold * 0.8)
    print(f'\n🎉 Kamu menang! Mendapat {enemy.reward_gold} Gold dan {hadiah_exp} Exp 🎉')
    player.gold += enemy.reward_gold
    player.exp += hadiah_exp
    player.score += enemy.reward_gold
    player.buruan.add(enemy.nama)
    history.add_log(enemy.nama)

    if player.exp >= 100:
      player.level += 1
      player.exp -= 100
      player.max_hp += 20
      player.hp = player.max_hp
      player.attack += 5
      print(f'Kamu naik level. Level saat ini: {player.level}')
      menu_pilih_skill_baru(player)
    
  else:
    print(f'\n💀 Kamu kalah 💀')

  player.hp = player.max_hp
  enemy.hp = enemy.max_hp
#===============================================================================================================================

# FUNGSI UNTUK MUAT GAME
def muat_game(lala, listpemain):
  try:
      with open("database_pemain.txt", "r") as file:
        for baris in file:
          data = baris.strip().split(',')
          
          if len(data) == 7:
            nama, pw, role, level, exp, gold, score = data

            lala.register(nama, pw)

            p_baru = Player(nama, role)
            p_baru.level = int(level)
            p_baru.exp = int(exp)
            p_baru.gold = int(gold)
            p_baru.score = int(score)

            tambahan_lvl = p_baru.level - 1
            p_baru.max_hp += (tambahan_lvl * 20)
            p_baru.hp = p_baru.max_hp
            p_baru.attack += (tambahan_lvl * 5)

            listpemain.tambah_pemain(p_baru)
                
  except FileNotFoundError:
    return
#================================================================================================

# FUNGSI SIMPAN GAME
def simpan_game(lala, listpemain):
    with open("database_pemain.txt", "w") as file:
      temp = listpemain.head
      while temp:
        p = temp.player

        password_user = ""
        index = lala.hash(p.nama)
        for item in lala.table[index]:
            if item[0] == p.nama:
                password_user = item[1]
                break

        file.write(f"{p.nama},{password_user},{p.role},{p.level},{p.exp},{p.gold},{p.score}\n")
        temp = temp.next
#===========================================================n=============================================================

#FUNGSI UNTUK MENU ADMIN
def menu_admin(lala, listpemain):
  while True:
    print("\n=== PANEL ADMIN ===")
    print("1. Tambah Karakter (Register Player)")
    print("2. Edit Karakter (Ubah Status)")
    print("3. Hapus Karakter (Banned)")
    print("4. Atur Level Permainan")
    print("5. Melihat Data Pemain")
    print("0. Keluar dari Panel Admin")
    try:
      opsi = int(input("Pilih opsi Admin: "))
      
      if opsi == 1:
        print("\n-- Tambah Karakter Baru --")
        user_baru = input("Username: ")
        pas_baru = input("Password: ")
        role = input("Role (fighter/tank/marksman): ")
        if role in ['fighter', 'tank', 'marksman']:
          if lala.register(user_baru, pas_baru):
            listpemain.tambah_pemain(Player(user_baru, role))
            print(f"Karakter {user_baru} berhasil diciptakan!")
          else:
            print("Username sudah terdaftar.")
        else:
          print("Role tidak valid!")
          
      elif opsi == 2:
        print("\n-- Edit Karakter --")
        user = input("Masukkan username yang ingin diedit: ")
        p = listpemain.get_pemain(user)
        if p:
          print(f"Data saat ini: HP={p.max_hp}, Attack={p.attack}, Gold={p.gold}")
          p.max_hp = int(input("Max HP baru: "))
          p.hp = p.max_hp
          p.attack = int(input("Attack baru: "))
          p.gold = int(input("Gold baru: "))
          print(f"Data karakter {user} berhasil diubah!")
        else:
          print("Karakter tidak ditemukan.")
          
      elif opsi == 3:
        print("\n-- Hapus Karakter --")
        user = input("Masukkan username yang ingin dihapus: ")
        if listpemain.hapus_pemain(user) and lala.hapus_akun(user):
          print(f"Karakter {user} telah dihapus dari sistem.")
        else:
          print("Karakter tidak ditemukan.")
          
      elif opsi == 4:
        print("\n-- Atur Level --")
        user = input("Masukkan username: ")
        p = listpemain.get_pemain(user)
        if p:
          print(f"Level saat ini: {p.level}")
          level_lama = p.level
          level_baru = int(input("Ubah menjadi level: "))
          selisih_level = level_baru - level_lama
          p.max_hp += (selisih_level * 20)
          p.hp = p.max_hp
          p.attack += (selisih_level * 5)
          if level_lama < 3 and level_baru >= 3:
            p.level = 3
            print(f"\n⚙️ [ADMIN] Wajib pilih skill Level 3 untuk {p.nama}:")
            menu_pilih_skill_baru(p)
            
          if level_lama < 5 and level_baru >= 5:
            p.level = 5
            print(f"\n⚙️ [ADMIN] Wajib pilih skill Level 5 untuk {p.nama}:")
            menu_pilih_skill_baru(p)
          
          p.level = level_baru 
          print(f"✅ Level karakter {user} berhasil diatur menjadi {p.level} (Status HP, Attack, dan Skill Tree telah diperbarui).")
        else:
          print("❌ Karakter tidak ditemukan.")
      elif opsi == 5:
        print("\n-- Data Seluruh Pemain --")
        temp = listpemain.head
        if not temp:
          print("Belum ada pemain di dalam database.")
        else:
          while temp:
            p = temp.player
            print(f"{p.nama} | Role: {p.role} | Lvl: {p.level} | Gold: {p.gold} | Skor: {p.score}")
            temp = temp.next
            
      elif opsi == 0:
        print("Keluar dari Panel Admin...")
        break
      else:
        print("Pilihan tidak valid.")
    except ValueError:
      print("Harap masukkan angka yang benar!")
#==============================================================================================

# FUNGSI MAIN
def main():
  lala = Login()
  listpemain = PlayerList()
  history = GameHistory()
  game_map = GameMap()
  lokasi_aktif = 'Desa Petualang'
  p_aktif = None
  
  muat_game(lala, listpemain)

  bounty_board = BountyBoard()
  
  bounty_board.insert(Enemy("Laba-Laba Beracun", 85, 18, 80)) # Node Root
  bounty_board.insert(Enemy("Kelelawar Gua", 45, 8, 35))
  bounty_board.insert(Enemy("Golem Batu", 160, 28, 180))
  bounty_board.insert(Enemy("Slime Hijau", 30, 5, 20))
  bounty_board.insert(Enemy("Goblin Pengintai", 60, 12, 50))
  bounty_board.insert(Enemy("Raja Slime (BOSS)", 70, 12, 60))
  bounty_board.insert(Enemy("Raja Orc (BOSS)", 120, 22, 120))
  bounty_board.insert(Enemy("Prajurit Kadal", 110, 20, 130))
  bounty_board.insert(Enemy("Naga Hitam (BOSS)", 250, 35, 300))
 
  while True:
    if not p_aktif:
      print("\n=== BATTLE ARENA ===")
      print("1. Login\n2. Register\n3. Keluar Game")
      try:
        opsi = int(input("Pilih menu: "))
        if opsi == 1:
          user = input('username: ')
          pas = input('password: ')
          if user == 'admin123' and pas == 'admin123':
            menu_admin(lala, listpemain)
            continue
          elif lala.cek(user, pas):
            p_aktif = listpemain.get_pemain(user)
            if p_aktif:
              print(f'\nLogin sukses. Welcome {p_aktif.nama}')
          else:
            print('Login gagal. Username atau password salah.')

        elif opsi == 2:
          user_baru = input('Username: ')
          pas_baru = input('Password: ')
          
          while True:
            try:
              print('Pilih role:\n1. fighter\n2. tank\n3. marksman')
              t = int(input('Pilih: '))
              if t == 1:
                role = 'fighter'
                break
              elif t == 2:
                role = 'tank'
                break
              elif t == 3:
                role = 'marksman'
                break
              else:
                print('Pilih antara 1/2/3!!')
            except ValueError:
              print('Masukkan angka 1/2/3')
              
          if lala.register(user_baru, pas_baru):
            new_player = Player(user_baru, role)
            listpemain.tambah_pemain(new_player)
            print('Registrasi berhasil')
          else:
            print('Registrasi gagal. Username sudah terpakai.')

        elif opsi == 3:
          simpan_game(lala, listpemain)
          print("Keluar")
          break
      except ValueError:
        print("Masukkan angka yang valid!")

    else:
      print(f"\n=== MAIN MENU | {lokasi_aktif} | Player: {p_aktif.nama} ({p_aktif.role}) | Lvl: {p_aktif.level} ===")
      print("1. Pindah Lokasi ")
      print("2. Battle Survival ") 
      print("3. Toko Item")
      print("4. Bounty Board")
      print("5. Lihat Data (Skill Tree & Log)")
      print("6. Leaderboard Skor ")
      print("7. Logout")

      try:
        opsi = int(input('Pilih: '))
        if opsi == 1:
          lokasi_aktif = navigasi_map(lokasi_aktif, game_map)

        elif opsi == 2:
          print(f'\n⚔️ MODE SURVIVAL - {lokasi_aktif} ⚔️')
          q_musuh = Survival()
          
          if lokasi_aktif == "Desa Petualang":
            q_musuh.enqueue(Enemy("Slime Hijau", 30, 5, 20))
            q_musuh.enqueue(Enemy("Kelelawar Gua", 45, 8, 35))
            q_musuh.enqueue(Enemy("Raja Slime (BOSS)", 70, 12, 60))
          elif lokasi_aktif == "Hutan Terlarang":
            q_musuh.enqueue(Enemy("Goblin Pengintai", 60, 12, 50))
            q_musuh.enqueue(Enemy("Laba-Laba Beracun", 85, 18, 80))
            q_musuh.enqueue(Enemy("Raja Orc (BOSS)", 120, 22, 120))
          elif lokasi_aktif == "Gua Naga":
            q_musuh.enqueue(Enemy("Prajurit Kadal", 110, 20, 130))
            q_musuh.enqueue(Enemy("Golem Batu", 160, 28, 180))
            q_musuh.enqueue(Enemy("Naga Hitam (BOSS)", 250, 35, 300))
            
          wave = 1
          while not q_musuh.is_empty() and p_aktif.hp > 0:
            musuh_sekarang = q_musuh.dequeue()
            print(f'\nWAVE {wave}')
            battle_system(p_aktif, musuh_sekarang, history)
            wave += 1

        elif opsi == 3:
          shop_menu(p_aktif)
        
        elif opsi == 4:
          print('\n=== 📜 PAPAN BURONAN (BST) 📜 ===')
          bounty_board.tampilkan_board(bounty_board.root)
          print('=================================')
          try:
            pil_gold = int(input("Masukkan jumlah Hadiah Gold buronan yang ingin dilawan (0 batal): "))
            if pil_gold > 0:
              target = bounty_board.search_target(bounty_board.root, pil_gold)
              if target:
                print(f"\n=> Target Ditemukan: {target.enemy.nama}!")
                battle_system(p_aktif, target.enemy, history)
              else:
                print("Buronan dengan nilai Gold tersebut tidak ditemukan!")
                
          except ValueError:
            print("Input tidak valid! Harap masukkan angka.")

        elif opsi == 5:
          print('\nSKILL TREE')
          tampilkan_skill(p_aktif.skill_tree)
          print(f"\nMonster yang pernah dikalahkan:")
          counter = 1
          for i in p_aktif.buruan:
            print(f'{counter}. {i}')
            counter += 1
          history.tampilkan()
        
        elif opsi == 6:
          semua_pemain = []
          temp = listpemain.head
          while temp:
            semua_pemain.append(temp.player)
            temp = temp.next
          
          leaderboard = manual_quick_sort(semua_pemain)
          
          print("\n=== LEADERBOARD SKOR PEMAIN ===")
          for rank, p in enumerate(leaderboard):
            print(f"{rank+1}. {p.nama} | Skor: {p.score}")

        elif opsi == 7:
          p_aktif = None
          simpan_game(lala, listpemain)
          print('Berhasil Logout, Data Disimpan')
          
      except ValueError:
        print("Masukkan angka yang valid!")
        continue

if __name__ == "__main__":
  main()
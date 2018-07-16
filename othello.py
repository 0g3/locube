import os
import pickle
from copy import deepcopy
from datetime import datetime

# TODO: ダイエット
class Othello3D():
  COLOR1 = 1
  COLOR2 = -1
  NOEXIST = 0
  POINTER = 2
  
  def __init__(self, board_size, first_player_color=1, save_data=None, rec=False, debug=False):
    self.debug = debug
    self.rec = rec
    if rec:
      if not os.path.isdir('rec'):
        os.mkdir('rec')
        print('made "rec" directory')

      rec_dir_name = datetime.now().strftime('%Y-%m-%d:%H-%M-%S')
      self.rec_dir_path = os.path.join('.', 'rec', rec_dir_name)
      os.mkdir(self.rec_dir_path)
      print('made "{}" directory'.format(self.rec_dir_path))

    self.board_size = board_size

    if save_data:
      self.rec_dir_path = os.path.join('.', 'rec', save_data)

      # 一番最新のデータを見つける
      for dat in os.listdir(self.rec_dir_path):
        n_max = 0 
        try:
          n = int(dat)
          if n_max < n:
            n_max = n 
        except:
          pass

        self.rec_file_path = os.path.join(self.rec_dir_path, str(n_max))
        self.load(self.rec_file_path)

    else:
      self.now_player_color = first_player_color
      self.phase = 1
      self.make_board(self.board_size)

    self.set_pointer(0, 0, 0)
    self.count()



  # **************************************** pointer functions ****************************************
  def set_pointer(self, x, y, z):
    self.pointer = {}
    self.pointer['x'] = x
    self.pointer['y'] = y
    self.pointer['z'] = z 
    self.pointer['tmp'] = self.board[z][y][x]
    self.board[z][y][x] = Othello3D.POINTER


  def move_pointer(self, drc):
    '''指定された方角にポインターを動かす'''
    success = False
    if drc == 'l':
      if 0 < self.pointer['x'] < self.board_size:
        self.board[self.pointer['z']][self.pointer['y']][self.pointer['x']] = self.pointer['tmp']
        self.pointer['x'] -= 1
        success = True
    if drc == 'r':
      if 0 <= self.pointer['x'] < self.board_size-1:
        self.board[self.pointer['z']][self.pointer['y']][self.pointer['x']] = self.pointer['tmp']
        self.pointer['x'] += 1
        success = True
    if drc == 'u':
      if 0 < self.pointer['y'] < self.board_size:
        self.board[self.pointer['z']][self.pointer['y']][self.pointer['x']] = self.pointer['tmp']
        self.pointer['y'] -= 1
        success = True
    if drc == 'd':
      if 0 <= self.pointer['y'] < self.board_size-1:
        self.board[self.pointer['z']][self.pointer['y']][self.pointer['x']] = self.pointer['tmp']
        self.pointer['y'] += 1
        success = True
    if drc == 't':
      if 0 < self.pointer['z'] < self.board_size:
        self.board[self.pointer['z']][self.pointer['y']][self.pointer['x']] = self.pointer['tmp']
        self.pointer['z'] -= 1
        success = True
    if drc == 'b':
      if 0 <= self.pointer['z'] < self.board_size-1:
        self.board[self.pointer['z']][self.pointer['y']][self.pointer['x']] = self.pointer['tmp']
        self.pointer['z'] += 1
        success = True

    if success:
      self.pointer['tmp'] = self.board[self.pointer['z']][self.pointer['y']][self.pointer['x']]
      self.board[self.pointer['z']][self.pointer['y']][self.pointer['x']] = Othello3D.POINTER


  # **************************************** search functions ****************************************
  def count(self):
    '''プレイヤーの石の数を調べる'''
    self.n_color1 = 0
    self.n_color2 = 0
    for z in range(self.board_size):
      for y in range(self.board_size):
        for x in range(self.board_size):
          if self.board[z][y][x] == Othello3D.COLOR1:
            self.n_color1 += 1
          if self.board[z][y][x] == Othello3D.COLOR2:
            self.n_color2 += 1


  def dose_exist(self, x, y, z):
    '''選択した座標に駒が存在するか調べる'''
    return True if self.board[z][y][x] != Othello3D.NOEXIST else False


  def check_full(self):
    for z in range(self.board_size):
      for y in range(self.board_size):
        for x in range(self.board_size):
          if self.board[z][y][x] == Othello3D.NOEXIST:
            return False
    return True


  # **************************************** reverse function ****************************************
  # TODO: DRYを守る
  def reverse(self):
    reversed_flg = False
    x = self.pointer['x']
    y = self.pointer['y']
    z = self.pointer['z']
    l_color = self.board[z][y][x]

    # ******************** x軸方向 ******************** 
    # ********* x+ ********* 
    if x < self.board_size-2:
      for hi in range(x+1, self.board_size):
        h_color = self.board[z][y][hi]
        if h_color == Othello3D.NOEXIST:
          break
        if h_color == l_color:
          for reversed_i in range(x+1, hi):
            if self.board[z][y][reversed_i] == -l_color:
              self.board[z][y][reversed_i] = l_color
              reversed_flg = True
          break
    # ********* x- ********* 
    if x > 1:
      for hi in range(x-1, -1, -1):
        h_color = self.board[z][y][hi]
        if h_color == Othello3D.NOEXIST:
          break
        if h_color == l_color:
          for reversed_i in range(x-1, hi, -1):
            if self.board[z][y][reversed_i] == -l_color:
              self.board[z][y][reversed_i] = l_color
              reversed_flg = True
          break
    # ******************** y軸方向 ******************** 
    # ********* y+ ********* 
    if y < self.board_size-2:
      for hi in range(y+1, self.board_size):
        h_color = self.board[z][hi][x]
        if h_color == Othello3D.NOEXIST:
          break
        if h_color == l_color:
          for reversed_i in range(y+1, hi):
            if self.board[z][reversed_i][x] == -l_color:
              self.board[z][reversed_i][x] = l_color
              reversed_flg = True
          break
    # ********* y- ********* 
    if y > 1:
      for hi in range(y-1, -1, -1):
        h_color = self.board[z][hi][x]
        if h_color == Othello3D.NOEXIST:
          break
        if h_color == l_color:
          for reversed_i in range(y-1, hi, -1):
            if self.board[z][reversed_i][x] == -l_color:
              self.board[z][reversed_i][x] = l_color
              reversed_flg = True
          break
    # ******************** xy軸方向 ******************** 
    if x < self.board_size-2:
      # ********* x+y+ ********* 
      if y < self.board_size-2:
        for hi_y, hi_x in zip(range(y+1, self.board_size), range(x+1, self.board_size)):
          h_color = self.board[z][hi_y][hi_x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_y, reversed_i_x in zip(range(y+1, hi_y), range(x+1, hi_x)):
              if self.board[z][reversed_i_y][reversed_i_x] == -l_color:
                self.board[z][reversed_i_y][reversed_i_x] = l_color
                reversed_flg = True
            break
      # ********* x+y- ********* 
      if y > 1:
        for hi_y, hi_x in zip(range(y-1, -1, -1), range(x+1, self.board_size)):
          h_color = self.board[z][hi_y][hi_x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_y, reversed_i_x in zip(range(y-1, hi_y, -1), range(x+1, hi_x)):
              if self.board[z][reversed_i_y][reversed_i_x] == -l_color:
                self.board[z][reversed_i_y][reversed_i_x] = l_color
                reversed_flg = True
            break
    if x > 1:
      # ********* x-y+ ********* 
      if y < self.board_size-2:
        for hi_y, hi_x in zip(range(y+1, self.board_size), range(x-1, -1, -1)):
          h_color = self.board[z][hi_y][hi_x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_y, reversed_i_x in zip(range(y+1, hi_y), range(x-1, hi_x, -1)):
              if self.board[z][reversed_i_y][reversed_i_x] == -l_color:
                self.board[z][reversed_i_y][reversed_i_x] = l_color
                reversed_flg = True
            break
      # ********* x-y- ********* 
      if y > 1:
        for hi_y, hi_x in zip(range(y-1, -1, -1), range(x-1, -1, -1)):
          h_color = self.board[z][hi_y][hi_x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_y, reversed_i_x in zip(range(y-1, hi_y, -1), range(x-1, hi_x, -1)):
              if self.board[z][reversed_i_y][reversed_i_x] == -l_color:
                self.board[z][reversed_i_y][reversed_i_x] = l_color
                reversed_flg = True
            break
    # ******************** yz軸方向 ******************** 
    if y < self.board_size-2:
      # ********* y+z+ ********* 
      if z < self.board_size-2:
        for hi_z, hi_y in zip(range(z+1, self.board_size), range(y+1, self.board_size)):
          h_color = self.board[hi_z][hi_y][x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_z, reversed_i_y in zip(range(z+1, hi_z), range(y+1, hi_y)):
              if self.board[reversed_i_z][reversed_i_y][x] == -l_color:
                self.board[reversed_i_z][reversed_i_y][x] = l_color
                reversed_flg = True
            break
      # ********* y+z- ********* 
      if z > 1:
        for hi_z, hi_y in zip(range(z-1, -1, -1), range(y+1, self.board_size)):
          h_color = self.board[hi_z][hi_y][x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_z, reversed_i_y in zip(range(z-1, hi_z, -1), range(y+1, hi_y)):
              if self.board[reversed_i_z][reversed_i_y][x] == -l_color:
                self.board[reversed_i_z][reversed_i_y][x] = l_color
                reversed_flg = True
            break
    if y > 1:
      # ********* y-z+ ********* 
      if z < self.board_size-2:
        for hi_z, hi_y in zip(range(z+1, self.board_size), range(y-1, -1, -1)):
          h_color = self.board[hi_z][hi_y][x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_z, reversed_i_y in zip(range(z+1, hi_z), range(y-1, hi_y, -1)):
              if self.board[reversed_i_z][reversed_i_y][x] == -l_color:
                self.board[reversed_i_z][reversed_i_y][x] = l_color
                reversed_flg = True
            break
      # ********* y-z- ********* 
      if z > 1:
        for hi_z, hi_y in zip(range(z-1, -1, -1), range(y-1, -1, -1)):
          h_color = self.board[hi_z][hi_y][x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_z, reversed_i_y in zip(range(z-1, hi_z, -1), range(y-1, hi_y, -1)):
              if self.board[reversed_i_z][reversed_i_y][x] == -l_color:
                self.board[reversed_i_z][reversed_i_y][x] = l_color
                reversed_flg = True
            break
    # ******************** zx軸方向 ******************** 
    if x < self.board_size-2:
      # ********* x+z+ ********* 
      if z < self.board_size-2:
        for hi_z, hi_x in zip(range(z+1, self.board_size), range(z+1, self.board_size)):
          h_color = self.board[hi_z][y][hi_x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_z, reversed_i_x in zip(range(z+1, hi_z), range(x+1, hi_x)):
              if self.board[reversed_i_z][y][reversed_i_x] == -l_color:
                self.board[reversed_i_z][y][reversed_i_x] = l_color
                reversed_flg = True
            break
      # ********* x+z- ********* 
      if z > 1:
        for hi_z, hi_x in zip(range(z-1, -1, -1), range(x+1, self.board_size)):
          h_color = self.board[hi_z][y][hi_x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_z, reversed_i_x in zip(range(z-1, hi_z, -1), range(x+1, hi_x)):
              if self.board[reversed_i_z][y][reversed_i_x] == -l_color:
                self.board[reversed_i_z][y][reversed_i_x] = l_color
                reversed_flg = True
            break
    if x > 1:
      # ********* x-z+ ********* 
      if z < self.board_size-2:
        for hi_z, hi_x in zip(range(z+1, self.board_size), range(x-1, -1, -1)):
          h_color = self.board[hi_z][y][hi_x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_z, reversed_i_x in zip(range(z+1, hi_z), range(x-1, hi_x, -1)):
              if self.board[reversed_i_z][y][reversed_i_x] == -l_color:
                self.board[reversed_i_z][y][reversed_i_x] = l_color
                reversed_flg = True
            break
      # ********* x-z- ********* 
      if z > 1:
        for hi_z, hi_x in zip(range(z-1, -1, -1), range(x-1, -1, -1)):
          h_color = self.board[hi_z][y][hi_x]
          if h_color == Othello3D.NOEXIST:
            break
          if h_color == l_color:
            for reversed_i_z, reversed_i_x in zip(range(z-1, hi_z, -1), range(x-1, hi_x, -1)):
              if self.board[reversed_i_z][y][reversed_i_x] == -l_color:
                self.board[reversed_i_z][y][reversed_i_x] = l_color
                reversed_flg = True
            break
    # ******************** z軸方向 ******************** 
    # ********* z+ ********* 
    if z < self.board_size-2:
      for hi in range(z+1, self.board_size):
        h_color = self.board[hi][y][x]
        if h_color == Othello3D.NOEXIST:
          break
        if h_color == l_color:
          for reversed_i in range(z+1, hi):
            if self.board[reversed_i][y][x]  == -l_color:
              self.board[reversed_i][y][x] = l_color
              reversed_flg = True
          break
    # ********* z- ********* 
    if z > 1:
      for hi in range(z-1, -1, -1):
        h_color = self.board[hi][y][x]
        if h_color == Othello3D.NOEXIST:
          break
        if h_color == l_color:
          for reversed_i in range(z-1, hi, -1):
            if self.board[reversed_i][y][x]  == -l_color:
              self.board[reversed_i][y][x] = l_color
              reversed_flg = True
          break
    # ******************** xyz軸方向 ******************** 
    if z < self.board_size-2:
      # ********* x+y+z+ ********* 
      if x < self.board_size-2:
        if y < self.board_size-2:
          for hi_z, hi_y, hi_x in zip(range(z+1, self.board_size), range(y+1, self.board_size), range(x+1, self.board_size)):
            h_color = self.board[hi_z][hi_y][hi_x]
            if h_color == Othello3D.NOEXIST:
              break
            if h_color == l_color:
              for reversed_i_z, reversed_i_y, reversed_i_x in zip(range(z+1, hi_z), range(y+1, hi_y), range(x+1, hi_x)):
                if self.board[reversed_i_z][reversed_i_y][reversed_i_x] == -l_color:
                  self.board[reversed_i_z][reversed_i_y][reversed_i_x] = l_color
                  reversed_flg = True
              break
        # ********* x+y-z+ ********* 
        if y > 1:
          for hi_z, hi_y, hi_x in zip(range(z+1, self.board_size), range(y-1, -1, -1), range(x+1, self.board_size)):
            h_color = self.board[hi_z][hi_y][hi_x]
            if h_color == Othello3D.NOEXIST:
              break
            if h_color == l_color:
              for reversed_i_z, reversed_i_y, reversed_i_x in zip(range(z+1, hi_z), range(y-1, hi_y, -1), range(x+1, hi_x)):
                if self.board[reversed_i_z][reversed_i_y][reversed_i_x] == -l_color:
                  self.board[reversed_i_z][reversed_i_y][reversed_i_x] = l_color
                  reversed_flg = True
              break
      if x > 1:
        # ********* x-y+z+ ********* 
        if y < self.board_size-2:
          for hi_z, hi_y, hi_x in zip(range(z+1, self.board_size), range(y+1, self.board_size), range(x-1, -1, -1)):
            h_color = self.board[hi_z][hi_y][hi_x]
            if h_color == Othello3D.NOEXIST:
              break
            if h_color == l_color:
              for reversed_i_z, reversed_i_y, reversed_i_x in zip(range(z+1, hi_z), range(y+1, hi_y), range(x-1, hi_x, -1)):
                if self.board[reversed_i_z][reversed_i_y][reversed_i_x] == -l_color:
                  self.board[reversed_i_z][reversed_i_y][reversed_i_x] = l_color
                  reversed_flg = True
              break
        # ********* x-y-z+ ********* 
        if y > 1:
          for hi_z, hi_y, hi_x in zip(range(z+1, self.board_size), range(y-1, -1, -1), range(x-1, -1, -1)):
            h_color = self.board[hi_z][hi_y][hi_x]
            if h_color == Othello3D.NOEXIST:
              break
            if h_color == l_color:
              for reversed_i_z, reversed_i_y, reversed_i_x in zip(range(z+1, hi_z), range(y-1, hi_y, -1), range(x-1, hi_x, -1)):
                if self.board[reversed_i_z][reversed_i_y][reversed_i_x] == -l_color:
                  self.board[reversed_i_z][reversed_i_y][reversed_i_x] = l_color
                  reversed_flg = True
              break
    if z > 1:
      if x < self.board_size-2:
        # ********* x+y+z- ********* 
        if y < self.board_size-2:
          for hi_z, hi_y, hi_x in zip(range(z-1, -1, -1), range(y+1, self.board_size), range(x+1, self.board_size)):
            h_color = self.board[hi_z][hi_y][hi_x]
            if h_color == Othello3D.NOEXIST:
              break
            if h_color == l_color:
              for reversed_i_z, reversed_i_y, reversed_i_x in zip(range(z-1, hi_z, -1), range(y+1, hi_y), range(x+1, hi_x)):
                if self.board[reversed_i_z][reversed_i_y][reversed_i_x] == -l_color:
                  self.board[reversed_i_z][reversed_i_y][reversed_i_x] = l_color
                  reversed_flg = True
              break
        # ********* x+y-z- ********* 
        if y > 1:
          for hi_z, hi_y, hi_x in zip(range(z-1, -1, -1), range(y-1, -1, -1), range(x+1, self.board_size)):
            h_color = self.board[hi_z][hi_y][hi_x]
            if h_color == Othello3D.NOEXIST:
              break
            if h_color == l_color:
              for reversed_i_z, reversed_i_y, reversed_i_x in zip(range(z-1, hi_z, -1), range(y-1, hi_y, -1), range(x+1, hi_x)):
                if self.board[reversed_i_z][reversed_i_y][reversed_i_x] == -l_color:
                  self.board[reversed_i_z][reversed_i_y][reversed_i_x] = l_color
                  reversed_flg = True
              break
      if x > 1:
        # ********* x-y+z- ********* 
        if y < self.board_size-2:
          for hi_z, hi_y, hi_x in zip(range(z-1, -1, -1), range(y+1, self.board_size), range(x-1, -1, -1)):
            h_color = self.board[hi_z][hi_y][hi_x]
            if h_color == Othello3D.NOEXIST:
              break
            if h_color == l_color:
              for reversed_i_z, reversed_i_y, reversed_i_x in zip(range(z-1, hi_z, -1), range(y+1, hi_y), range(x-1, hi_x, -1)):
                if self.board[reversed_i_z][reversed_i_y][reversed_i_x] == -l_color:
                  self.board[reversed_i_z][reversed_i_y][reversed_i_x] = l_color
                  reversed_flg = True
              break
        # ********* x-y-z- ********* 
        if y > 1:
          for hi_z, hi_y, hi_x in zip(range(z-1, -1, -1), range(y-1, -1, -1), range(x-1, -1, -1)):
            h_color = self.board[hi_z][hi_y][hi_x]
            if h_color == Othello3D.NOEXIST:
              break
            if h_color == l_color:
              for reversed_i_z, reversed_i_y, reversed_i_x in zip(range(z-1, hi_z, -1), range(y-1, hi_y, -1), range(x-1, hi_x, -1)):
                if self.board[reversed_i_z][reversed_i_y][reversed_i_x] == -l_color:
                  self.board[reversed_i_z][reversed_i_y][reversed_i_x] = l_color
                  reversed_flg = True
              break
    
    return reversed_flg


  # **************************************** main functions ****************************************
  def make_board(self, board_size):
    self.board = []
    for _ in range(self.board_size):
      self.board.append([])
    for i in range(self.board_size):
      for _ in range(self.board_size):
        self.board[i].append([Othello3D.NOEXIST,Othello3D.NOEXIST,Othello3D.NOEXIST,Othello3D.NOEXIST, Othello3D.NOEXIST, Othello3D.NOEXIST])

    # 初期位置設定
    if self.debug:
      RED_INIT = 3
      self.board[RED_INIT][RED_INIT][RED_INIT] = Othello3D.COLOR1
      
      self.board[RED_INIT-1][RED_INIT][RED_INIT] = Othello3D.COLOR2
      self.board[RED_INIT+1][RED_INIT][RED_INIT] = Othello3D.COLOR2
      self.board[RED_INIT-1][RED_INIT-1][RED_INIT] = Othello3D.COLOR2
      self.board[RED_INIT+1][RED_INIT+1][RED_INIT] = Othello3D.COLOR2
      self.board[RED_INIT-1][RED_INIT][RED_INIT-1] = Othello3D.COLOR2
      self.board[RED_INIT+1][RED_INIT][RED_INIT+1] = Othello3D.COLOR2
      self.board[RED_INIT][RED_INIT-1][RED_INIT] = Othello3D.COLOR2
      self.board[RED_INIT][RED_INIT+1][RED_INIT] = Othello3D.COLOR2
      self.board[RED_INIT][RED_INIT][RED_INIT-1] = Othello3D.COLOR2
      self.board[RED_INIT][RED_INIT][RED_INIT+1] = Othello3D.COLOR2
      self.board[RED_INIT][RED_INIT+1][RED_INIT+1] = Othello3D.COLOR2
      self.board[RED_INIT][RED_INIT+1][RED_INIT-1] = Othello3D.COLOR2
      self.board[RED_INIT][RED_INIT-1][RED_INIT+1] = Othello3D.COLOR2
      self.board[RED_INIT][RED_INIT-1][RED_INIT-1] = Othello3D.COLOR2
      self.board[RED_INIT+1][RED_INIT+1][RED_INIT+1] = Othello3D.COLOR2
      self.board[RED_INIT+1][RED_INIT+1][RED_INIT-1] = Othello3D.COLOR2
      self.board[RED_INIT+1][RED_INIT-1][RED_INIT+1] = Othello3D.COLOR2
      self.board[RED_INIT+1][RED_INIT-1][RED_INIT-1] = Othello3D.COLOR2
      self.board[RED_INIT-1][RED_INIT+1][RED_INIT+1] = Othello3D.COLOR2
      self.board[RED_INIT-1][RED_INIT+1][RED_INIT-1] = Othello3D.COLOR2
      self.board[RED_INIT-1][RED_INIT-1][RED_INIT+1] = Othello3D.COLOR2
      self.board[RED_INIT-1][RED_INIT-1][RED_INIT-1] = Othello3D.COLOR2
      self.board[RED_INIT+1][RED_INIT][RED_INIT-1] = Othello3D.COLOR2
      self.board[RED_INIT+1][RED_INIT-1][RED_INIT] = Othello3D.COLOR2
      self.board[RED_INIT-1][RED_INIT][RED_INIT+1] = Othello3D.COLOR2
      self.board[RED_INIT-1][RED_INIT+1][RED_INIT] = Othello3D.COLOR2


    else:
      self.board[2][2][2] = Othello3D.COLOR1
      self.board[2][3][3] = Othello3D.COLOR1
      self.board[3][2][3] = Othello3D.COLOR1
      self.board[3][3][2] = Othello3D.COLOR1
      self.board[2][2][3] = Othello3D.COLOR2
      self.board[2][3][2] = Othello3D.COLOR2
      self.board[3][3][3] = Othello3D.COLOR2
      self.board[3][2][2] = Othello3D.COLOR2


  def select(self, x, y, z):
    '''選択した座標に現在のプレイヤーの石を置く'''
    self.board[z][y][x] = self.now_player_color
  
  
  def pass_(self):
    self.board[self.pointer['z']][self.pointer['y']][self.pointer['x']] = self.pointer['tmp']
    self.set_pointer(0, 0, 0)
    self.now_player_color *= -1
    if self.rec: self.record()
    self.phase += 1


  def game_end(self):
    if self.n_color1 > self.n_color2:
      for z in range(self.board_size):
        for y in range(self.board_size):
          for x in range(self.board_size):
            self.board[z][y][x] = Othello3D.COLOR1

    if self.n_color1 < self.n_color2:
      for z in range(self.board_size):
        for y in range(self.board_size):
          for x in range(self.board_size):
            self.board[z][y][x] = Othello3D.COLOR2

    if self.n_color1 == self.n_color2:
      for z in range(self.board_size//2):
        for y in range(self.board_size):
          for x in range(self.board_size):
            self.board[z][y][x] = Othello3D.COLOR1
      for z in range(self.board_size//2, self.board_size):
        for y in range(self.board_size):
          for x in range(self.board_size):
            self.board[z][y][x] = Othello3D.COLOR2
      

  def record(self):
    with open(os.path.join(self.rec_dir_path, str(self.phase)), 'wb') as f:
      pickle.dump((self.phase, self.now_player_color, self.board), f)


  def load(self, dat):
    with open(dat, 'rb') as f:
      tmp = pickle.load(f)
      self.phase = tmp[0]
      self.now_player_color = tmp[1]
      self.board = tmp[2]


  def proceed(self):
    '''ゲームのフェーズを進める'''
    if self.debug:
      if self.pointer['tmp'] == Othello3D.NOEXIST:
        tmp = deepcopy(self.board)
        self.select(self.pointer['x'], self.pointer['y'], self.pointer['z'])
        rflg = self.reverse()
        if rflg:
          self.count()
          self.record()
          self.set_pointer(0, 0, 0)
        else:
          self.board = deepcopy(tmp)
    else:
      if self.pointer['tmp'] == Othello3D.NOEXIST:
        tmp = deepcopy(self.board)
        self.select(self.pointer['x'], self.pointer['y'], self.pointer['z'])
        revflg = self.reverse()
        if revflg:
          self.count()
          self.phase += 1

          # TODO: 両プレイヤーとも置けるコマがない場合も追加する
          if self.check_full(): # game end
            self.record()
            self.game_end()

          else:  # game continue
            self.now_player_color *= -1
            self.record()
            self.set_pointer(0, 0, 0)
        else:  # no reverse
          self.board = deepcopy(tmp)

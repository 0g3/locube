import pygame
from pygame.locals import *
import serial
from time import sleep

from othello import Othello3D
from game_pad import JC_FR08TWH

SERIAL_PATH_Z01     = '/dev/tty.wchusbserial14210'
SERIAL_PATH_Z23     = '/dev/tty.wchusbserial14220'
SERIAL_PATH_Z45     = '/dev/tty.wchusbserial14240'

RATE                = 9600
INIT_SLEEP_TIME     = 2   # この待ち時間がないとシリアル通信ができない

# 現在の手番を示すしくみとして必要。
NOW_PLAYER_DIGIT_C1 = '#'
NOW_PLAYER_DIGIT_C2 = '@'


def get_serial_board(OthelloObject):
  # ******************** hwの仕様に合わせてboardを変換 ********************
  cube = []
  for z in range(SWCube.board_size):
    face = []
    for y in range(SWCube.board_size):
      byt = ''
      for x in range(SWCube.board_size):
        if SWCube.board[z][y][x] == -1: 
          byt += str(3)
        else:
          byt += str(SWCube.board[z][y][x])

      # x軸方向のリバース
      if ((z % 2 == 0) and (y % 2 == 1)) or ((z % 2 == 1) and (y % 2 == 0)):
        byt = byt[::-1]

      face.append(byt)

    if z % 2 == 1:
      face.reverse()     # y軸方向のリバース
    cube.append(face) 

  # ******************** serial通信のためのstr生成 ********************
  digit = None
  if OthelloObject.now_player_color == Othello3D.COLOR1: digit = NOW_PLAYER_DIGIT_C1
  if OthelloObject.now_player_color == Othello3D.COLOR2: digit = NOW_PLAYER_DIGIT_C2
  ret_z01 = digit
  ret_z23 = digit
  ret_z45 = digit 

  for z in [0, 1]:
    for y in range(OthelloObject.board_size):
      for x in range(OthelloObject.board_size):
        ret_z01 += cube[z][y][x]
  for z in [2, 3]:
    for y in range(OthelloObject.board_size):
      for x in range(OthelloObject.board_size):
        ret_z23 += cube[z][y][x]
  for z in [4, 5]:
    for y in range(OthelloObject.board_size):
      for x in range(OthelloObject.board_size):
        ret_z45 += cube[z][y][x]

  return (bytes(ret_z01, 'utf-8'), bytes(ret_z23, 'utf-8'), bytes(ret_z45, 'utf-8'))


def write_serial(s_z01, s_z23, s_z45):
  print('writing serial board')
  z01, z23, z45 = get_serial_board(o)
  s_z01.write(z01)
  s_z23.write(z23)
  s_z45.write(z45)


def main():
  pygame.init()
  o = Othello3D(board_size=6, first_player_color=1)
  s_z01 = serial.Serial(SERIAL_PATH_Z01, RATE)
  s_z23 = serial.Serial(SERIAL_PATH_Z23, RATE)
  s_z45 = serial.Serial(SERIAL_PATH_Z45, RATE)
  sleep(INIT_SLEEP_TIME)
  write_serial(s_z01, s_z23, s_z45)
  print('(red_num,blue_num)=({},{})'.format(o.n_color1, o.n_color2))

  # コントローラが最初に出すノイズを読み込む
  for e in pygame.event.get(): pass

  while 1:
    for e in pygame.event.get():
      if e.type == pygame.locals.JOYBUTTONDOWN:
        if e.button == JC_FR08TWH.A:
          o.proceed()
          write_serial(s_z01, s_z23, s_z45)
        if e.button == JC_FR08TWH.Y:
          o.pass_()
          write_serial(s_z01, s_z23, s_z45)
        if e.button == JC_FR08TWH.L:
          o.move_pointer('b')
          write_serial(s_z01, s_z23, s_z45)
        if e.button == JC_FR08TWH.R:
          o.move_pointer('t')
          write_serial(s_z01, s_z23, s_z45)
        if e.button == JC_FR08TWH.SELECT:
          o.game_end()
          write_serial(s_z01, s_z23, s_z45)
        if e.button == JC_FR08TWH.START:
          o = Othello3D(board_size=6, first_player_color=1)
          write_serial(s_z01, s_z23, s_z45)

      if e.type == pygame.locals.JOYAXISMOTION:
        if joys.get_axis(JC_FR08TWH.LEFT_AXIS_L) < JC_FR08TWH.BUTTON_INIT:
          o.move_pointer('l')
          write_serial(s_z01, s_z23, s_z45)
        if joys.get_axis(JC_FR08TWH.RIGHT_AXIS_G) > JC_FR08TWH.BUTTON_INIT:
          o.move_pointer('r')
          write_serial(s_z01, s_z23, s_z45)
        if joys.get_axis(JC_FR08TWH.UP_AXIS_G) > JC_FR08TWH.BUTTON_INIT:
          o.move_pointer('u')
          write_serial(s_z01, s_z23, s_z45)
        if joys.get_axis(JC_FR08TWH.DOWN_AXIS_L) < JC_FR08TWH.BUTTON_INIT:
          o.move_pointer('d')
          write_serial(s_z01, s_z23, s_z45)

    # ボタンを連打するとバグる現象の対抗策。
    # 気休め程度。値はてきとー
    sleep(0.1) 


if __name__ == '__main__':
  pygame.joystick.init()

  try:
    joys = pygame.joystick.Joystick(0) # joystickインスタンスの生成
    joys.init()
  except pygame.error:
    print('コントローラが認識されていません。')
    quit()

  main() 

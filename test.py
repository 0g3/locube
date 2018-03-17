import pygame
from pygame.locals import *
import time
import os

from othello import Othello3D
from game_pad import JC_FR08TWH

def to_hw_cube(SWCube):
  cube = []
  for z in range(SWCube.board_size):
    face = []
    for y in range(SWCube.board_size):
      byt = []
      for x in range(SWCube.board_size):
        if SWCube.board[z][y][x] == -1: 
          byt.append(-1)
        else:
          byt.append(SWCube.board[z][y][x])

      # x軸方向のリバース
      if ((z % 2 == 0) and (y % 2 == 1)) or ((z % 2 == 1) and (y % 2 == 0)):
        byt.reverse()

      face.append(byt)

    if z % 2 == 1:
      face.reverse()     # y軸方向のリバース
    cube.append(face) 
  return cube


def to_pl9823(cube):
  cube.reverse()
  for z, face in enumerate(cube):
    if z % 2 == 1:
      face.reverse()

  for z in range(len(cube)):
    for y in range(len(cube)):
      if ((z % 2 == 1) and (y % 2 == 0)) or ((z % 2 == 0) and (y % 2 == 1)):
        cube[z][y].reverse()


def to_console_cube(cube):
  c = []
  for z in range(len(cube)):
    f = []
    for y in range(len(cube)):
      r = ''
      for x in range(len(cube)):
        if cube[z][y][x] == 0:
          r += '❎ '
        if cube[z][y][x] == 1:
          r += '🐶 '
        if cube[z][y][x] == -1:
          r += '😸 '
        if cube[z][y][x] == 2:
          r += '💩 '
      f.append(r)
    c.append(f)
  return c


def main():
  pygame.init()
  o = Othello3D(board_size=6, first_player_color=1, rec=True)
  while 1:
    hw_cube = to_hw_cube(o)
    to_pl9823(hw_cube)

    hw_console_cube = to_console_cube(hw_cube)
    sw_console_cube = to_console_cube(o.board)

    # ******************** 描画 ********************
    os.system('clear')
    print('******************** PHASE: {} ********************'.format(o.phase))
    if o.now_player_color == 1:
      print('現在の手番:🐶 ')
    if o.now_player_color == -1:
      print('現在の手番:😸 ')
    
    print('🐶 の数:', o.n_color1)
    print('😸 の数:', o.n_color2)

    print('**** HW ****          **** SW ****')
    for z in range(o.board_size):
      for y in range(o.board_size):
        print(hw_console_cube[z][y], end="")
        print('----------', end="")
        print(sw_console_cube[z][y], end="")
        print()
      print()

    for e in pygame.event.get():
      if e.type == pygame.locals.JOYBUTTONDOWN:
        if e.button == JC_FR08TWH.A:
          o.proceed()
        if e.button == JC_FR08TWH.Y:
          o.pass_()
        if e.button == JC_FR08TWH.L:
          o.move_pointer('b')
        if e.button == JC_FR08TWH.R:
          o.move_pointer('t')
        if e.button == JC_FR08TWH.SELECT:
          o.game_end()
        if e.button == JC_FR08TWH.START:
          o = Othello3D(board_size=6, first_player_color=1)
      if e.type == pygame.locals.JOYAXISMOTION:
        if joys.get_axis(JC_FR08TWH.LEFT_AXIS_L) < JC_FR08TWH.BUTTON_INIT:
          o.move_pointer('l')
        if joys.get_axis(JC_FR08TWH.RIGHT_AXIS_G) > JC_FR08TWH.BUTTON_INIT:
          o.move_pointer('r')
        if joys.get_axis(JC_FR08TWH.UP_AXIS_G) > JC_FR08TWH.BUTTON_INIT:
          o.move_pointer('u')
        if joys.get_axis(JC_FR08TWH.DOWN_AXIS_L) < JC_FR08TWH.BUTTON_INIT:
          o.move_pointer('d')

    time.sleep(0.1)

if __name__ == '__main__':
  pygame.joystick.init()

  try:
    joys = pygame.joystick.Joystick(0) # joystickインスタンスの生成
    joys.init()

  except pygame.error:
    print('差し込め')
    quit()

  main()

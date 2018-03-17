class JC_FR08TWH():
  BUTTON_INIT   = -0.003936767578125
  A             = 3
  B             = 1
  X             = 2
  Y             = 0
  L             = 5
  R             = 4
  SELECT        = 6
  START         = 7

  # 以下の定数を使って十字キー判定を行う。
  # ex) LEFTの判定:
  #       if JoyStickObject.get_axis(JC_FR08TWH.LEFT_AXIS_L) < JC_FR08TWH.BUTTON_INIT:
  #         hoge()
  #
  # AXIS_LのLはLESSという意味でJC_FR08TWH.BUTTON_INITより小さいという意味
  # GはGREATERなのでJC_FR08TWH.BUTTON_INITより大きいという意味
  LEFT_AXIS_L   = 3
  RIGHT_AXIS_G  = 3
  UP_AXIS_G     = 4
  DOWN_AXIS_L   = 4

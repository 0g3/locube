#include <Adafruit_NeoPixel.h>

// ******************** config ********************
// ********* main *********
#define RGBLED_OUTPIN 2  // RGBLEDに出力するピン番号
#define NUMRGBLED     72  // Arduinoにぶら下がっているRGBLEDの個数

#define RGB_VAL 255
#define DELAY_TIME 5  // てきとーな値。

#define Z_SIZE 2
#define Y_SIZE 6
#define X_SIZE 6

char board[Z_SIZE][Y_SIZE][X_SIZE];

// ********* judgement *********
#define JUDGEMENT_OUTPIN     4  // RGBLEDに出力するピン番号
#define NOW_PLAYER_DIGIT_C1 '#'
#define NOW_PLAYER_DIGIT_C2 '@'

// ******************** RGBLEDのライブラリを生成する(色指定はRGBの並びで行う、LEDの速度は800KHzとする) ********************
Adafruit_NeoPixel RGBLED    = Adafruit_NeoPixel(NUMRGBLED, RGBLED_OUTPIN, NEO_RGB + NEO_KHZ800);
Adafruit_NeoPixel JUDGEMENT = Adafruit_NeoPixel(NUMRGBLED, JUDGEMENT_OUTPIN, NEO_RGB + NEO_KHZ800);


// ******************** set led functions ********************
void set_red(int id) {
  RGBLED.setPixelColor(id, RGB_VAL, 0, 0);
}

void set_green(int id) {
  RGBLED.setPixelColor(id, 0, RGB_VAL, 0);
}

void set_blue(int id) {
  RGBLED.setPixelColor(id, 0, 0, RGB_VAL);
}

void set_black(int id) {
  RGBLED.setPixelColor(id, 0, 0, 0);
}


// ******************** main funcitons ********************
void setup() {
  RGBLED.begin();                   // RGBLEDのライブラリを初期化する
  RGBLED.setBrightness(20);         // 明るさの指定(0-255)を行う
  JUDGEMENT.begin();                // RGBLEDのライブラリを初期化する
  JUDGEMENT.setBrightness(255);     // 明るさの指定(0-255)を行う
  Serial.begin(9600);               // シリアル通信開始
}

void loop() {
  // ******************** read serial ********************
  int check_digit = Serial.read();
  if (check_digit != -1) {
    for (int z = 0; z < Z_SIZE; z++) {
      for (int y = 0; y < Y_SIZE; y++) {
        for (int x = 0; x < X_SIZE; x++) {
          delay(DELAY_TIME);
          board[z][y][x] = Serial.read();
        }
      }
    }
  }
  // ******************** set led ********************
  int i = 0;
  for (int z = 0; z < Z_SIZE; z++) {
    for (int y = 0; y < Y_SIZE; y++) {
      for (int x = 0; x < X_SIZE; x++, i++) {
        if (i < NUMRGBLED) {
          delay(DELAY_TIME);
          if (board[z][y][x] == '0') {set_black(i);}
          if (board[z][y][x] == '1') {set_red(i);}
          if (board[z][y][x] == '2') {set_green(i);}
          if (board[z][y][x] == '3') {set_blue(i);}
        }
      }
    }
  }
  RGBLED.show();
  
  // judgementの処理
  if (check_digit == NOW_PLAYER_DIGIT_C1) {JUDGEMENT.setPixelColor(0, RGB_VAL, 0, 0);}
  if (check_digit == NOW_PLAYER_DIGIT_C2) {JUDGEMENT.setPixelColor(0, 0, 0, RGB_VAL);}
  JUDGEMENT.show();
}

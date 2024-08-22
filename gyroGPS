#include <MPU9250_WE.h>
#include <Wire.h>
#include <LedControl.h>
#include <Arduino.h>
#define MPU9250_ADDR 0x68

// Arduino Nano 에 연결
const int DIN_PIN = 11;
const int CLK_PIN = 10;
const int CS_PIN = 13;

// LED 매트릭스 연결
LedControl lc = LedControl(DIN_PIN, CLK_PIN, CS_PIN, 1);

// 방향에 따른 화살표 배열 정의
byte arrows[8][8] = {
  {0b00011000, 0b00111100, 0b01111110, 0b11111111, 0b01111110, 0b00111100, 0b00011000, 0b00011000}, // Up-위쪽
  {0b00011000, 0b00011000, 0b00111100, 0b01111110, 0b11111111, 0b01111110, 0b00111100, 0b00011000}, // Up-right
  {0b00011000, 0b00011000, 0b00011000, 0b11111111, 0b11111111, 0b00011000, 0b00011000, 0b00011000}, // Right-오른쪽
  {0b00011000, 0b00011000, 0b00111100, 0b01111110, 0b11111111, 0b01111110, 0b00111100, 0b00011000}, // Down-right
  {0b00011000, 0b00011000, 0b01111110, 0b11111111, 0b11111111, 0b01111110, 0b00011000, 0b00011000}, // Down-아래쪽
  {0b00011000, 0b00011000, 0b01111110, 0b11111111, 0b01111110, 0b00111100, 0b00011000, 0b00011000}, // Down-left
  {0b00011000, 0b00111100, 0b01111110, 0b11111111, 0b01111110, 0b00111100, 0b00011000, 0b00011000}, // Left-왼쪽
  {0b00011000, 0b00111100, 0b01111110, 0b11111111, 0b01111110, 0b00111100, 0b00011000, 0b00011000}  // Up-left
};

void displayArrow(int direction) {
  lc.clearDisplay(0);
  for (int row = 0; row < 8; row++) {
    lc.setRow(0, row, arrows[direction][row]);
  }
}

MPU9250_WE myMPU9250 = MPU9250_WE(MPU9250_ADDR);
// X와 Y축 속도 변수
float velocityX = 0.0;
float velocityY = 0.0;
unsigned long lastTime;

float g_value_x;
float g_value_y;

int r_l = 0;
int f_b = 0;
float theta = 0;

// ---------------------------

void setup() {
  lc.shutdown(0, false);      // 디스플레이 활성화
  lc.setIntensity(0, 8);      // 밝기 설정 (0~15)
  lc.clearDisplay(0);         // 디스플레이 초기화

  // ---------------------------

  Serial.begin(115200);
  Wire.begin();
  if(!myMPU9250.init()){
    Serial.println("MPU9250 does not respond");
  } else {
    Serial.println("MPU9250 is connected!");
  }

  Serial.println("Position your MPU9250 flat and don't move it - calibrating...");
  delay(1000);
  myMPU9250.autoOffsets();
  Serial.println("Done!");

  myMPU9250.setSampleRateDivider(5);
  myMPU9250.setAccelRange(MPU9250_ACC_RANGE_2G);
  myMPU9250.enableAccDLPF();
  myMPU9250.setAccDLPF(MPU9250_DLPF_6);

  lastTime = millis();
}

// ---------------------------

void loop() {
  float velocityThreshold = 0.5; // 속도 임계값, 속도가 작을 경우 정지 상태로 판단
  int movingThreshold = 3;
  for(int i=0; i<movingThreshold; i++){
    unsigned long currentTime = millis();
    float deltaTime = (currentTime - lastTime) / 1000.0; // 시간 차이 (초 단위)

    xyzFloat accRaw = myMPU9250.getAccRawValues();
    xyzFloat accCorrRaw = myMPU9250.getCorrectedAccRawValues();
    xyzFloat angle = myMPU9250.getAngles();

    velocityX += g_value_x * deltaTime;
    velocityY += g_value_y * deltaTime;
    g_value_x = accRaw.x;
    g_value_y = accRaw.y;
    lastTime = currentTime;

    delay(200);
  }

  Serial.print(velocityX);
  Serial.print(" ");
  Serial.print(" ");
  Serial.print(velocityY);
  Serial.print(" ");
  Serial.print(r_l);
  Serial.print(" ");
  Serial.println(f_b);

  if(velocityX > velocityThreshold){
    Serial.println("Moving Backward");
    f_b = 1;
  } else if(velocityX < -velocityThreshold){
    Serial.println("Moving Forward");
    f_b = -1;
  }

  if(velocityY > velocityThreshold*1.3){
    Serial.println("Moving Right");
    r_l = 1;
  } else if(velocityY < -velocityThreshold*0.6){
    Serial.println("Moving Left");
    r_l = -1;
  }

  theta = atan2f(f_b, r_l)*180/PI;

  if(-22.5<=theta && theta<22.5){
    displayArrow(0);
  } else if(22.5<=theta && theta<67.5){
    displayArrow(7);
  } else if(67.5<=theta && theta<112.5){
    displayArrow(6);
  } else if(112.5<=theta && theta<157.5){
    displayArrow(5);
  } else if(157.5<=theta || theta<-157.5){
    displayArrow(4);
  } else if(-157.5<=theta && theta<-112.5){
    displayArrow(3);
  } else if(-112.5<=theta && theta<-67.5){
    displayArrow(2);
  } else if(-67.5<=theta && theta<-22.5){
    displayArrow(1);
  }

  velocityX = 0.0;
  velocityY = 0.0;
}

#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>
//SoftwareSerial mySerial(2, 3);
DFRobotDFPlayerMini MP3Player;

SoftwareSerial mySerial(2,3);

# define Start_Byte 0x7E     // 시작 값
# define Version_Byte 0xFF   // 버전 값
# define Command_Length 0x06 // 길이 값
# define End_Byte 0xEF       // 종료 값
# define Acknowledge 0x00    // 피드백 때 수신

extern volatile unsigned long timer0_millis;

#define Magswitch_in 6       // 핀매핑
#define chargeMagswitch_in 5 // 핀매핑

long second_start;
long second_end;

void setup() {
  // put your setup code here, to run once:
  pinMode(Magswitch_in,INPUT);
  pinMode(chargeMagswitch_in,INPUT);
  mySerial.begin(9600);       // 소프트웨어 시리얼 통신 개시
  Serial.begin(4800);
  delay(2000);
  specify_Volume(25);         // 볼륨을 25로 지정
  //specify_Track(1);         // 대기링
}

int is_walking = LOW;        //0이면 나가는 상태, 1이면 들어오는 상태

void loop() {
  long walking_time;
  walking_time = second_end - second_start;
  int is_outdoor = digitalRead(Magswitch_in);
  int is_charging = digitalRead(chargeMagswitch_in);
  Serial.print("in ");

  if (is_outdoor == HIGH) { //문이 열린 상태
    Serial.println("is_outdoor HIGH");
    if (is_walking == LOW) { 
      Serial.println("is_walking LOW"); //집 안에 있는 상태
      if(is_charging == LOW) { 
        Serial.println("is_charging LOW"); //충전기에 거치된 상태
        alert_missing(); //자재함에 맞을 알림
        Serial.println("door open / charge / leaving");

        is_walking = HIGH;
        delay(10000);
      }
      // else {
      // stopwatch_start();
      // is_walking = HIGH;
      // Serial.println("door open / no charge / leaving");
      // delay(10000);
      // }
    } 
  } else if (is_walking == HIGH) { //집 안에 있는 상태
    if(is_charging == HIGH) { 
      alert_charge(); //충전기에 없는 상태
      delay(10000);
      Serial.println("door open / no charge / entering");

      is_walking = LOW;
      delay(10000);
    }
    // else {
    // stopwatch_start();
    // is_walking = LOW;
    // Serial.println("door open / no charge / entering");
    // delay(10000);
    // }
  }
  //specify_Track(1);
}

void specify_Volume(byte level)  // 볼륨 조정 함수
{
  execute_CMD(0x06, 0x00, level); //볼륨조정 명령어 0x06과 볼륨레벨 파라미터로 전달
}

void specify_Track(int16_t track) // 트랙 지정 함수
{
  execute_CMD(0x03, highByte(track), lowByte(track)); // 트랙재생 명령어 0x03과 재생할 트랙을 파라미터로 전달
}

void execute_CMD(byte CMD, byte Par1, byte Par2)  // 시리얼 통신을 통해 실제 명령어구문을 전달하는 함수
{
  int16_t checksum = -(Version_Byte + Command_Length + CMD + Acknowledge + Par1 + Par2); //체크섬계산
  byte Command_line[10] = { Start_Byte, Version_Byte, Command_Length, CMD, Acknowledge, Par1, Par2, highByte(checksum), lowByte(checksum), End_Byte};

  for (byte k=0; k<10; k++)  // 명령어 구문을 시리얼 통신을 송신
  {
    mySerial.write(Command_line[k]);
  }
}

void stopwatch_start() {
  second_start = millis()/1000;
}

void stopwatch_end() {
  second_end = millis()/1000;
}

void alert_missing() {
  specify_Track(2);
}

void alert_charge() {
  specify_Track(1);
}

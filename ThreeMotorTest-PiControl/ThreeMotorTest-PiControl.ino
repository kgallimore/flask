/* Three Motor Control, Raspberry Pi - Arduino
* Author: Andrew Amerman
* 
* Arduino code is a slave to Raspberry Pi through I2C
* Upon receiveEvent, motor controls are updated
*
*/

//#define PRINTOUTS

//use defines
#define ADC_MAX 1023
#define ADC_MIN 0
#define LC_MAX 300
#define LC_MIN 0

double wob = 0; //20.60 kg

int counter_print = 0;

const int lcReadingPin = A4; //Load Cell Input
int analogInput_LC = 0;

#include <Wire.h>

const int enaX = 17;
const int dirX = 16;
const int pulX = 13;

const int enaY = 26;
const int dirY = 23;
const int pulY = 8;

const int enaZ = 2;
const int dirZ = 3;
const int pulZ = 4;

boolean pulse = HIGH;


//Motor Control from Pi
int motorX_direction = 0; 
int motorX_speed = 0;   
int motorX_interval = 12;
int motorY_direction = 0; 
int motorY_speed = 0;   
int motorY_interval = 0;
int motorZ_direction = 0; 
int motorZ_speed = 0;
int motorZ_interval = 0;

int motorX_count = -12;
int motorY_count = 0;
int motorZ_count = 0;


void setup()
{
  Serial.begin(9600);
  pinMode(enaX, OUTPUT);
  pinMode(dirX, OUTPUT);
  pinMode(pulX, OUTPUT);
  pinMode(enaY, OUTPUT);
  pinMode(dirY, OUTPUT);
  pinMode(pulY, OUTPUT);
  pinMode(enaZ, OUTPUT);
  pinMode(dirZ, OUTPUT);
  pinMode(pulZ, OUTPUT);
  
  digitalWrite(enaX, LOW);
  digitalWrite(dirX, LOW);
  digitalWrite(pulX, HIGH);
  digitalWrite(enaY, HIGH);
  digitalWrite(dirY, LOW);
  digitalWrite(pulY, HIGH);
  digitalWrite(enaZ, HIGH);
  digitalWrite(dirZ, LOW);
  digitalWrite(pulZ, HIGH);

  Wire.begin(0x04);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
}
void loop() {

  delayMicroseconds(100);
  motorX_count++; motorY_count++; motorZ_count++;
  if(motorX_count == motorX_interval) {
    motorX_count = -motorX_interval;
    digitalWrite(pulX, HIGH);
  }
  else if (motorX_count == 0) {
    digitalWrite(pulX, LOW);
  }
  if(motorY_count == motorY_interval) {
    motorY_count = -motorY_interval;
    digitalWrite(pulY, HIGH);
  }
  else if (motorY_count == 0) {
    digitalWrite(pulY, LOW);
  }
  if(motorZ_count == motorZ_interval) {
    motorZ_count = -motorZ_interval;
    digitalWrite(pulZ, HIGH);
  }
  else if (motorZ_count == 0) {
    digitalWrite(pulZ, LOW);
  }

  counter_print++;
  if (counter_print >1000) {
    printData();
    counter_print = 0;
  }
}

void receiveEvent(int howMany) {
 // motor1 direction, motor 1speed,... for motors 2/3

 //Speed intervals
 while(Wire.available()) {
  Wire.read(); //null character
  motorX_direction = Wire.read(); 
  motorX_speed = Wire.read();   
  motorY_direction = Wire.read(); 
  motorY_speed = Wire.read();   
  motorZ_direction = Wire.read(); 
  motorZ_speed = Wire.read();  

  //X Motion
  if(motorX_direction == 1) {
    digitalWrite(dirX, LOW);
  }
  else {
    digitalWrite(dirX,HIGH);
  }
  if(motorX_speed == 0) {
    digitalWrite(enaX, HIGH);
  }
  else {
    digitalWrite(enaX, LOW);
  }
  //
  if(motorX_interval != speed_conversion(motorX_speed)) {
    motorX_interval = speed_conversion(motorX_speed);
    motorX_count = -motorX_interval;    
  }
  #ifdef PRINTOUTS
  Serial.print("MotorX Direction: ");         // print the integer
  Serial.print(motorX_direction);
  Serial.print(", speed: ");
  Serial.println(motorX_speed);
  #endif

  //Y Motion
  if(motorY_direction == 1) {
    digitalWrite(dirY, HIGH);
  }
  else {
    digitalWrite(dirY,LOW);
  }
  if(motorY_speed == 0) {
    digitalWrite(enaY, HIGH);
  }
  else {
    digitalWrite(enaY, LOW);
  }
  if(motorY_interval != speed_conversion(motorY_speed)) {
    motorY_interval = speed_conversion(motorY_speed);
    motorY_count = -motorY_interval;
  }
  #ifdef PRINTOUTS
  Serial.print("MotorY Direction: ");         // print the integer
  Serial.print(motorY_direction);
  Serial.print(", speed: ");
  Serial.println(motorY_speed);
  #endif

  //Z Motion
  if(motorZ_direction == 1) {
    digitalWrite(dirZ, HIGH);
  }
  else {
    digitalWrite(dirZ,LOW);
  }
  if(motorZ_speed == 0) {
    digitalWrite(enaZ, HIGH);
  }
  else {
    digitalWrite(enaZ, LOW);
  }   
  if(motorZ_interval != speed_conversion(motorZ_speed)) {
    motorZ_interval = speed_conversion(motorZ_speed);
    motorZ_count = -motorZ_interval;
    
  }
  #ifdef PRINTOUTS
  Serial.print("MotorZ Direction: ");         // print the integer
  Serial.print(motorZ_direction);
  Serial.print(", speed: ");
  Serial.println(motorZ_speed);
  #endif
 }
}

int speed_conversion(int motor_speed) {
  if(motor_speed == 0) {
    return 0;
  }
  else if (motor_speed < 30) {
    return 14;
  }
  else if (motor_speed < 60) {
    return 11;
  }
  else if (motor_speed < 90) {
    return 8;
  }
  else if (motor_speed < 120) {
    return 6;
  }
  else if (motor_speed < 150) {
    return 5;
  }
  else if (motor_speed < 180) {
    return 4;
  }
  else if (motor_speed < 210) {
    return 3;
  }
  else if (motor_speed < 240) {
    return 2;
  } 
  else if (motor_speed >=240) {
    return 1;
  }
}

void printData() {
  analogInput_LC = analogRead(lcReadingPin);
  wob = map(analogInput_LC, ADC_MIN, ADC_MAX, LC_MIN, LC_MAX );
  Serial.print("Wob: ");
  Serial.print(analogInput_LC);
  Serial.print(", ");
  Serial.println(wob);
}

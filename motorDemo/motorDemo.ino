#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;
const int ena = 5;
const int dir = 3; 
const int pul = 4;
const int relay_stop = 6;
const int switch1 = 2;
boolean pulse = LOW; //initial 
int interval = 100; //85 is
bool new_data = false;
void Emergency_Stop() {
  digitalWrite(ena,HIGH);
  digitalWrite(relay_stop,HIGH);
  Serial.println("Ready!");
}
void setup() {
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  pinMode(ena, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(pul, OUTPUT);
  pinMode(relay_stop, OUTPUT);
  //pinMode(switch1, INPUT);
  attachInterrupt(digitalPinToInterrupt(switch1), Emergency_Stop, LOW); //delete 
  digitalWrite(ena, LOW);
  digitalWrite(relay_stop,LOW); 
  digitalWrite(dir, HIGH); 
  digitalWrite(pul, HIGH);
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  Serial.println("Ready!");
}


void loop() {
  pulse = !pulse; //invert signal
  digitalWrite(pul, pulse);
  delayMicroseconds(interval);
}

// callback for received data
void receiveData(int byteCount){
  new_data = true;
  while(Wire.available()) {
    number = Wire.read();
    //Serial.print("data received: ");
    //Serial.println(number);
    if(number == 0){
      digitalWrite(ena, HIGH);
    }
    else {
      digitalWrite(ena, LOW);
      digitalWrite(relay_stop,LOW);
      interval = number*4;
    }
}new_data = false;
}

// callback for sending data
void sendData(){
  Wire.write(number);
}

bool motor = true; //true
const int enaL = 4;
const int dirL = 2;
const int pulL = 3;
const int enaV = 5;
const int dirV = 6;
const int pulV = 7;
const int switch1 = 10;
const int switch2 = 9;
const int switch3 = 11;
//const int switchEStop = 10;
boolean pulse = HIGH; //initial
int interval = 200; //85 is
/*void Emergency_Stop() {
  digitalWrite(ena,HIGH);
  Serial.println("Ready!");
  }*/
  
void setup()
{
  Serial.begin(9600);
  pinMode(enaL, OUTPUT);
  pinMode(dirL, OUTPUT);
  pinMode(pulL, OUTPUT);
  pinMode(enaV, OUTPUT);
  pinMode(dirV, OUTPUT);
  pinMode(pulV, OUTPUT);
  pinMode(switch1, INPUT); ///low means pressed
  pinMode(switch2, INPUT);
  pinMode(switch3, INPUT);
  //attachInterrupt(digitalPinToInterrupt(switchEStop), Emergency_Stop, LOW); //delete
  digitalWrite(enaL, LOW);
  digitalWrite(dirL, LOW);
  digitalWrite(pulL, HIGH);
  digitalWrite(enaV, LOW);
  digitalWrite(dirV, LOW);
  digitalWrite(pulV, HIGH);
  
  motor = true;
  Serial.println("Current motor: Lateral");
}
void loop() {
  if (digitalRead(switch3) == LOW) {
    while (digitalRead(switch3) == LOW) {
      //Serial.println("Waiting for button release");
      delay(200);
    }
    motor = !motor;
    if(motor ==true)
    {
      Serial.println("Current motor: Lateral");
    }
    else
    {
      Serial.println("Current motor: Vertical");
    }
  }
  if (motor) { //motor(true) = lateral motor
    if (digitalRead(switch1) == LOW || digitalRead(switch2) == LOW) {
      //Serial.println("Either Switch is pressed");
      digitalWrite(enaL, LOW);
      if (digitalRead(switch1) == LOW) {
        digitalWrite(dirL, LOW);
      }
      else {
        digitalWrite(dirL, HIGH);
      }
      pulse = !pulse; //invert signal
      digitalWrite(pulL, pulse);
    }
    else {
      //Serial.println("No button pressed"); //Neutral
      digitalWrite(enaL, HIGH);
    }
  }
  else {
    if (digitalRead(switch1) == LOW || digitalRead(switch2) == LOW) {
      //Serial.println("Either Switch is pressed");
      digitalWrite(enaV, LOW);
      if (digitalRead(switch1) == LOW) {
        digitalWrite(dirV, LOW);
      }
      else {
        digitalWrite(dirV, HIGH);
      }
      pulse = !pulse; //invert signal
      digitalWrite(pulV, pulse);
    }
    else {
      //Serial.println("No button pressed"); //Neutral
      digitalWrite(enaV, HIGH);
    }
  }
  delayMicroseconds(interval);
}

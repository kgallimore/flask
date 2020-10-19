boolean hit = LOW;

const int xLimitRight = 40;
const int xLimitLeft = 39;
const int yLimitUp = 41;
const int yLimitDown = 43;
const int zLimitUp = 38;
const int zLimitDown = 42;

String limitsPressed = "";
//const int switchEStop = 10;

/*void Emergency_Stop() {
  digitalWrite(ena,HIGH);
  Serial.println("Ready!");
  }*/

void setup()
{
  Serial.begin(9600);

  pinMode(xLimitRight, INPUT); ///low means pressed
  pinMode(xLimitLeft, INPUT); ///low means pressed
  pinMode(zLimitUp, INPUT); ///low means pressed
  pinMode(zLimitDown, INPUT); ///low means pressed
  pinMode(yLimitDown, INPUT); ///low means pressed
  pinMode(yLimitUp, INPUT); ///low means pressed
  //pinMode(switch2, INPUT);
  //pinMode(switch3, INPUT);
  //attachInterrupt(digitalPinToInterrupt(switchEStop), Emergency_Stop, LOW); //delete
  

}

void loop() {
  limitsPressed = "";
  
  if (digitalRead(xLimitRight) == hit) {
    limitsPressed += " xLimitRight";
  }
  if (digitalRead(xLimitLeft) == hit) {
    limitsPressed += " xLimitLeft";
  }
  if (digitalRead(yLimitDown) == hit) {
    limitsPressed += " yLimitDown";
  }
  if (digitalRead(yLimitUp) == hit) {
    limitsPressed += " yLimitUp";
  }
  if (digitalRead(zLimitUp) == hit) {
    limitsPressed += " zLimitUp";
  }
  if (digitalRead(zLimitDown) == hit) {
    limitsPressed += " zLimitDown";
  }
  if (limitsPressed != ""){
    limitsPressed = "Limit switches pressed:" + limitsPressed;
    Serial.println(limitsPressed);
  }
  delay(5);
}

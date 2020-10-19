const int enaX = 17;
const int dirX = 16;
const int pulX = 13;

const int enaY = 26;
const int dirY = 23;
const int pulY = 8;

const int enaZ = 2;
const int dirZ = 3;
const int pulZ = 4;

boolean motionLeft = false;
boolean motionForward = false;
boolean motionUp = false;

char rx_byte = 0;

int countX = 0;
int countY = 0;
int countZ = 0;

int intervalX = 0;
int intervalY = 0;
int intervalZ = 0;

int speedX = 5;
int speedY = 5;
int speedZ = 1;

//stepper position

int xStepCount = 0;
int yStepCount = 0;
int zStepCount = 0;
double xPos;
double yPos;
double zPos;

//xMotor: 3200 pul/rev, 8 threads/inch
const double xStepConversion = (1 / 3200.0) * (1.0) / (8.0);
const double yStepConversion = xStepConversion;
const double zStepConversion = yStepConversion;

//use defines
#define ADC_MAX 1023
#define ADC_MIN 0
#define LC_MAX 200
#define LC_MIN 0

double wob = 0; //20.60 kg @4.99V

int counter_print = 0;
int print_delay = 2000;

const int lcReadingPin = A4; //Load Cell Input
int analogInput_LC = 0;

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
  digitalWrite(enaY, LOW);
  digitalWrite(dirY, LOW);
  digitalWrite(pulY, HIGH);
  digitalWrite(enaZ, LOW);
  digitalWrite(dirZ, LOW);
  digitalWrite(pulZ, HIGH);
}
void loop() {

  if (Serial.available() > 0) {    // is a character available?
    rx_byte = Serial.read();       // get the character

    // check if a number was received
    if (rx_byte == ' ') {
      Serial.println("Emergency Stop");
      //      digitalWrite(enaX, HIGH);
      //      digitalWrite(enaY, HIGH);
      //      digitalWrite(enaZ, HIGH);
      countX = 0;
      intervalX = 0;
      countY = 0;
      intervalY = 0;
      countZ = 0;
      intervalZ = 0;
    }
    else if (rx_byte == 'a')
    {
      Serial.println("Move left");
      countX = -speedX;
      intervalX = speedX;
      motionLeft = true;
      digitalWrite(enaX, LOW);
      digitalWrite(dirX, LOW);
      digitalWrite(pulX, HIGH);
    }
    else if (rx_byte == 'd') {
      countX = -speedX;
      intervalX = speedX;
      motionLeft = false;
      Serial.println("Move right");
      digitalWrite(enaX, LOW);
      digitalWrite(dirX, HIGH);
      digitalWrite(pulX, HIGH);
    }
    else if (rx_byte == 'w')
    {
      countY = -speedY;
      intervalY = speedY;
      motionForward = true;
      Serial.println("Move forward");
      digitalWrite(enaY, LOW);
      digitalWrite(dirY, LOW);
      digitalWrite(pulY, HIGH);
    }
    else if (rx_byte == 's') {
      countY = -speedY;
      intervalY = speedY;
      motionForward = false;
      Serial.println("Move back");
      digitalWrite(enaY, LOW);
      digitalWrite(dirY, HIGH);
      digitalWrite(pulY, HIGH);
    }
    else if (rx_byte == 'q')
    {
      countZ = -speedZ;
      intervalZ = speedZ;
      motionUp = true;
      Serial.println("Move up");
      digitalWrite(enaZ, LOW);
      digitalWrite(dirZ, LOW);
      digitalWrite(pulZ, HIGH);
    }
    else if (rx_byte == 'e') {
      countZ = -speedZ;
      intervalZ = speedZ;
      motionUp = false;
      Serial.println("Move down");
      digitalWrite(enaZ, LOW);
      digitalWrite(dirZ, HIGH);
      digitalWrite(pulZ, HIGH);
    }
  }
  delayMicroseconds(100);
  countX++; countY++; countZ++;
  if (countX == intervalX) {
    countX = -intervalX;
    digitalWrite(pulX, HIGH);
    if(motionLeft) {
      xStepCount += 1;
    }
    else {
      xStepCount -= 1;
    }
  }
  else if (countX == 0) {
    digitalWrite(pulX, LOW);
  }
  if (countY == intervalY) {
    countY = -intervalY;
    digitalWrite(pulY, HIGH);
    if(motionForward) {
      yStepCount += 1;
    }
    else {
      yStepCount -= 1;
    }
  }
  else if (countY == 0) {
    digitalWrite(pulY, LOW);
  }
  if (countZ == intervalZ) {
    countZ = -intervalZ;
    digitalWrite(pulZ, HIGH);
    if(motionUp) {
      zStepCount += 1;
    }
    else {
      zStepCount -= 1;
    }
  }
  else if (countZ == 0) {
    digitalWrite(pulZ, LOW);
  }

  counter_print++;
  if (counter_print > print_delay) {
    printData(1);
    counter_print = 0;
  }
}

void updatePos() {
  xPos = xStepCount * xStepConversion;
  yPos = yStepCount * yStepConversion;
  zPos = zStepCount * zStepConversion;
}

void printData(int dataset) {
  if (dataset == 0) {
    analogInput_LC = analogRead(lcReadingPin);
    wob = map(analogInput_LC, ADC_MIN, ADC_MAX, LC_MIN, LC_MAX );
    Serial.print("WOB, adc value: ");
    Serial.print(analogInput_LC);
    Serial.print(", ");
    if (wob < 150) {
      Serial.print(wob);
      Serial.println(" N");
    }
    else if (wob >= 150) {
      Serial.print(wob);
      Serial.println(" N, EXCEEDING LIMIT OF 150 N, SLOW DOWN");
    }
  }
  else if(dataset == 1) {
    updatePos();
    Serial.print("Current distance x, inches: ");
    Serial.println(xPos);  
  }
}

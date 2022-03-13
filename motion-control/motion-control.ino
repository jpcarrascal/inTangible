#include <FlexyStepper2.h>

const int Z_STEP_PIN = 3;
const int Z_DIR_PIN = 2;
const int Z_ENABLE_PIN = 26;

const int X_STEP_PIN = 15;
const int X_DIR_PIN = 21;
const int X_ENABLE_PIN = 14;

const int X_MIN_PIN = 18;
const int Z_MIN_PIN = 20;

const int BTN_ENC = 16;
const char STOP_CHAR = ";";

bool atHome = false;
int goCount = 0;

const float xMult = 3.2;
const float yMult = -16;
const int xMax = 250;
const int yMax = 250;

const int maxXpos = 5;
const int maxYpos = 5;

int charsRead = 0;
const byte numChars = 32;
char receivedChars[numChars];

const int commandLength = 3;

boolean newData = false;
char axisToMove;
int posToMove;


FlexyStepper2 yStepper;
FlexyStepper2 xStepper;

void setup() {
  Serial.begin(115200);
  yStepper.connectToPins(Z_STEP_PIN, Z_DIR_PIN);
  xStepper.connectToPins(X_STEP_PIN, X_DIR_PIN);
  pinMode(Z_ENABLE_PIN, OUTPUT);
  pinMode(X_ENABLE_PIN, OUTPUT);
  pinMode(BTN_ENC, INPUT_PULLUP);

  pinMode(X_MIN_PIN, INPUT_PULLUP);
  pinMode(Z_MIN_PIN, INPUT_PULLUP);
  
  digitalWrite(Z_ENABLE_PIN, LOW);
  digitalWrite(X_ENABLE_PIN, LOW);
  yStepper.setSpeedInStepsPerSecond(1000*16);
  yStepper.setAccelerationInStepsPerSecondPerSecond(2000*8);
  xStepper.setSpeedInStepsPerSecond(1000*16);
  xStepper.setAccelerationInStepsPerSecondPerSecond(2000*8);
  delay(2000);
  goHome();
}

void loop() {

  int enc = digitalRead(BTN_ENC);
  if(enc == 0) {
    goCount++;
  } else {
    goCount = 0;
  }
  if(goCount > 20) {
    if(atHome) {
      yStepper.moveToPositionInMillimeters(yMax * yMult);
      xStepper.moveToPositionInMillimeters(xMax * xMult);
      atHome = false;
    } else {
      goHome();
    }
    goCount = 0;
  }

  recvWithEndMarker();
  showNewData();  
}

void goHome() {
  xStepper.moveToHomeInMillimeters(-1, 1000, 3000, X_MIN_PIN);
  yStepper.moveToHomeInMillimeters(1, 1000, 10000, Z_MIN_PIN);
  atHome = true;
  Serial.print("hdone");
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            parseCommand(ndx);
            ndx = 0;
            newData = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        //Serial.print("---This just in ... ");
        Serial.println(receivedChars);
        newData = false;
    }
}

void parseCommand(int charsRead) {
  if(charsRead == commandLength) {
    Serial.println(receivedChars);
    if(receivedChars[1] == ':') {
      axisToMove = receivedChars[0];
      posToMove = atoi(&receivedChars[2]);
      if(axisToMove == 'x') {    
        if(posToMove < maxXpos) {
          int destination = (int) (posToMove * (xMax / 5) + 25);
          xStepper.moveToPositionInMillimeters(destination * xMult);
          Serial.print("xdone");
        }
      } else if(axisToMove == 'y') {
        if(posToMove <= maxYpos) {
          int destination = (int) (posToMove * (yMax / 5));
          yStepper.moveToPositionInMillimeters(destination * yMult);
          Serial.print("ydone");
        }
      } else if(axisToMove == 'h') {
        goHome();
      } else {
        Serial.print("Not a command");
      }
    }
    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}

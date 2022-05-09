#define STEPPING 16   //valid values: 1, 2, 4 , 8, 16
#define STEP_TIME_MICROSECONDS_LOWER 450
#define STEP_TIME_MICROSECONDS_WAIT 450
#define DIRECTION_INVERT false


#define STEP_PIN D5
#define DIR_PIN D0
#define ENDSTP_PIN D1

#define MS1_PIN D8
#define MS2_PIN D7
#define MS3_PIN D6

bool homing = false;
float currentAngle = 0.0f;
float targetAngle = 0.0f;
int STEP_TIME_MULT = 3;
int STEP_DELAY = 10;

void setup() {
  pinMode(STEP_PIN,OUTPUT); 
  pinMode(DIR_PIN,OUTPUT);
  pinMode(MS1_PIN,OUTPUT);
  pinMode(MS2_PIN,OUTPUT);
  pinMode(MS3_PIN,OUTPUT);
  pinMode(ENDSTP_PIN, INPUT);

  #if STEPPING == 1
  digitalWrite(MS1_PIN, LOW);
  digitalWrite(MS2_PIN, LOW);
  digitalWrite(MS3_PIN, LOW);
  #elif STEPPING == 2
  digitalWrite(MS1_PIN, HIGH);
  digitalWrite(MS2_PIN, LOW);
  digitalWrite(MS3_PIN, LOW);
  #elif STEPPING == 4
  digitalWrite(MS1_PIN, LOW);
  digitalWrite(MS2_PIN, HIGH);
  digitalWrite(MS3_PIN, LOW);
  #elif STEPPING == 8
  digitalWrite(MS1_PIN, HIGH);
  digitalWrite(MS2_PIN, HIGH);
  digitalWrite(MS3_PIN, LOW);
  #elif STEPPING == 16
  digitalWrite(MS1_PIN, HIGH);
  digitalWrite(MS2_PIN, HIGH);
  digitalWrite(MS3_PIN, HIGH);
  #else
  #error "Invalid microstepping set"
  #endif

  attachInterrupt(digitalPinToInterrupt(ENDSTP_PIN), endstopInt, RISING);
  
  Serial.begin(115200);
  Serial.println("ayy");
  
  doHome();
}
void loop() {
  static long lastCommand;
  if (Serial.available()){
    String recieveString = Serial.readStringUntil('\n');
    if (recieveString.startsWith("A")) {
      
      setAngle(recieveString.substring(1).toFloat());
    }
    if (recieveString.startsWith("B")) {
      
      int tgtAngle = recieveString.substring(1).toInt();
      if (tgtAngle == 360){
        setAngle(360.0f);
        currentAngle = 0.0f;
        targetAngle = 0.0f;
      }
      else{
        setAngle(recieveString.substring(1).toFloat());
      }
      
    }

    if (recieveString.startsWith("C")) {
      doHome();
    }

    if (recieveString.startsWith("D")) {
      STEP_TIME_MULT = recieveString.substring(1).toInt();
      }
     if (recieveString.startsWith("E")) {
     STEP_DELAY = recieveString.substring(1).toInt();
     }
   
   lastCommand = millis();
   Serial.println("R");
  }

  if(millis() - lastCommand > 1000){
    Serial.println("R");
  }
  
}

void setAngle(float angle){
  targetAngle = angle;

  /*Serial.print("current:");
    Serial.println(currentAngle);
    Serial.print("target:");
    Serial.println(targetAngle);
  Serial.print("delta:");
    Serial.println(targetAngle - currentAngle);
     Serial.println();
     */
  rotateAngle(targetAngle - currentAngle);
}

void rotateAngle(float angle){
  bool dir = angle > 0;
  for(int i = 0; i < abs(angle)/(1.8/STEPPING); i++){
    doStep(dir);
    yield();
    delayMicroseconds(STEP_DELAY);
  }
  if(targetAngle != currentAngle){
    currentAngle += angle;
  }
}

void doStep(bool dir){
digitalWrite(DIR_PIN, dir == DIRECTION_INVERT);
digitalWrite(STEP_PIN,HIGH);
delayMicroseconds(STEP_TIME_MICROSECONDS_LOWER/STEPPING * STEP_TIME_MULT);
digitalWrite(STEP_PIN,LOW);
delayMicroseconds(STEP_TIME_MICROSECONDS_WAIT/STEPPING * STEP_TIME_MULT);
}

ICACHE_RAM_ATTR void endstopInt(){
static long lastTime;
  if(digitalRead(ENDSTP_PIN)){
    if(millis() - lastTime > 500){
      if (homing)
      currentAngle = 0.0f;
    }
  } 
  lastTime = millis();
}

void doHome(){
  homing = true;
  currentAngle = 1.0f;
  for(int i = 0; i < 250*STEPPING; i++){
    if(currentAngle == 0.0f) break;
    doStep(true);
    if(currentAngle == 0.0f) break;    
  }
  homing = false;
}

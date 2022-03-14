#define STEPPING 2
#define STEP_TIME_MULT 1
#define STEP_TIME_MICROSECONDS_LOWER 450
#define STEP_TIME_MICROSECONDS_WAIT 450



#define STEP_PIN 11
#define DIR_PIN 12
#define ENDSTP_PIN 10

bool endstopState = false;
float currentAngle = 0.0f;
float targetAngle = 0.0f;

void setup() {
  // Sets the two pins as Outputs
  pinMode(STEP_PIN,OUTPUT); 
  pinMode(DIR_PIN,OUTPUT);
  pinMode(ENDSTP_PIN, INPUT);

  Serial.begin(115200);

  doHome();
}
void loop() {
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

   
  }
}

void setAngle(float angle){
  targetAngle = angle;

  Serial.print("current:");
    Serial.println(currentAngle);
    Serial.print("target:");
    Serial.println(targetAngle);
  Serial.print("delta:");
    Serial.println(targetAngle - currentAngle);
     Serial.println();
  rotateAngle(targetAngle - currentAngle);
}

void rotateAngle(float angle){
  bool dir = angle > 0;
  for(int i = 0; i < abs(angle)/(1.8/STEPPING); i++){
    doStep(dir);
  }
  if(targetAngle != currentAngle){
    currentAngle += angle;
  }
}

void doStep(bool dir){
digitalWrite(DIR_PIN, dir);
digitalWrite(STEP_PIN,HIGH);
delayMicroseconds(STEP_TIME_MICROSECONDS_LOWER * STEP_TIME_MULT);
digitalWrite(STEP_PIN,LOW);
delayMicroseconds(STEP_TIME_MICROSECONDS_WAIT * STEP_TIME_MULT);
}

void doHome(){
  for(int i = 0; i < 200*STEPPING; i++){
    doStep(true);
    if(digitalRead(ENDSTP_PIN)){
      break;
    }
  }
  currentAngle = 0.0f;
}

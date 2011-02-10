 /* google_earth
  * tangible interface
  *
  * 2 NO switches connected to microcontroller digital inputs 2, 3 
  * with 10K pull-down resistors
  */
  
int switchPin2 = 2;
int switchPin3 = 3;
int val2a;
int val2b;
int val3a;
int val3b;
int state;

void setup()
{
  Serial.begin(9600);
  pinMode(switchPin2, INPUT);
  pinMode(switchPin3, INPUT);
}

void loop()
{
  val2a = digitalRead(switchPin2);      
  val3a = digitalRead(switchPin3);      
  delay(10);                         
  val2b = digitalRead(switchPin2);
  val3b = digitalRead(switchPin3);
  if (val2a == val2b && val2a == 1) {    
    state = 2;
    delay(10);
  }
  if (val3a == val3b && val3a == 1) {
    state = 3; 
    delay(10);
  }
  Serial.println(state);
}

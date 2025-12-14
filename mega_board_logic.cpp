#include <Servo.h>

Servo xServo;
Servo yServo;


const int TRIG_PIN = 11;
const int ECHO_PIN = 10;
const int SERVO_X_PIN = 9;
const int SERVO_Y_PIN = 8;


const int Y_START = 45;
const int Y_END = 135;
const int Y_STEP = 2;

const int X_START = 60;
const int X_END = 120;
const int X_STEP = 2;


int tab[46][31]; 

void setup() {
  xServo.attach(SERVO_X_PIN);
  yServo.attach(SERVO_Y_PIN);
  
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT); 
  
  Serial.begin(9600);
  Serial.println("Arduino Mega: Start skanowania...");
  

  yServo.write(Y_START);
  xServo.write(X_START);
  delay(1000); 
}

void loop() {
  
  
  int rowIndex = 0;

  for(int i = Y_START; i <= Y_END; i += Y_STEP)
  {
    yServo.write(i);
    delay(50);
    
    Serial.print("Skanowanie wiersza: ");
    Serial.println(rowIndex);

    int colIndex = 0;
    
    for (int j = X_START; j <= X_END; j += X_STEP)
    {
      xServo.write(j);
      delay(30);
      
      digitalWrite(TRIG_PIN, LOW);
      delayMicroseconds(2);
      digitalWrite(TRIG_PIN, HIGH);
      delayMicroseconds(10);
      digitalWrite(TRIG_PIN, LOW);

      long duration = pulseIn(ECHO_PIN, HIGH, 30000); 
      
      int distance = duration * 0.034 / 2;
      
      if(rowIndex < 46 && colIndex < 31) {
          tab[rowIndex][colIndex] = distance;
      }

      colIndex++;
    }
    rowIndex++;
  }

  
  Serial.println("\n--- MAPA WYNIKÓW ---"); 

  for(int i = 0; i < 46; i++)
  {
    for (int j = 0; j < 31; j++)
    {
      Serial.print(tab[i][j]);
      Serial.print("\t"); 
    }
    Serial.println(); 
  }
  Serial.println("--- Koniec ---");

  
  Serial.println("Koniec skanowania. Czekam 10 sekund...");
  delay(10000);
}

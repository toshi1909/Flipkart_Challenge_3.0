#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>

Servo myservo;
RF24 radio(8, 48); // CE, CSN
const byte address[6] = "00001";
int led_pin = 3;
boolean button_state = 0;
int mh11 = 24;
int mh12 = 26;
int mh21 = 28;
int mh22 = 30;
int mh1e = 4;
int mh2e = 5;

int mv11 = 44;
int mv12 = 38;
int mv21 = 40;
int mv22 = 42;
int mv1e = 6;
int mv2e = 7;

int servo = 3;
int count=0;

int pos;
int pwm1;
int pwm2;
void setup() {
  myservo.attach(3);
  myservo.write(0);
  pinMode(mh11, OUTPUT);
  pinMode(mh12, OUTPUT);
  pinMode(mh21, OUTPUT);
  pinMode(mh22, OUTPUT);
  pinMode(mh1e, OUTPUT);
  pinMode(mh2e, OUTPUT);


  pinMode(mv11, OUTPUT);
  pinMode(mv12, OUTPUT);
  pinMode(mv21, OUTPUT);
  pinMode(mv22, OUTPUT);
  pinMode(mv1e, OUTPUT);
  pinMode(mv2e, OUTPUT);

  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);   //Setting the address at which we will receive the data
  radio.setPALevel(RF24_PA_MIN);       //You can set this as minimum or maximum depending on the distance between the transmitter and receiver.
  radio.startListening();              //This sets the module as receiver
}


void loop() {
  // put your main code here, to run repeatedly:
  if (radio.available())              //Looking for the data.
  {
    char text[3] = "";                 //Saving the incoming data
    int i = 0;
    while (i < 3) {
      text[i] = '\0';
      i++;
    }
    Serial.println("text-" + String(text));
    radio.read(&text, sizeof(text));    //Reading the data
    //radio.read(&button_state, sizeof(button_state));    //Reading the data

    Serial.println(text);
    i = 0;
    int check = 0;
    while (i < 3) {
      Serial.print((int)(text[i]));
      if ((int)text[i] == 0) {
        Serial.println("CORRUPT");
        check = 1;
      }
      i++;
    }


    if (check == 0) {

      if(text[0]=='4'){
        if(text[2]=='0'){
          digitalWrite(mh11, LOW);
          digitalWrite(mh12, LOW);
          digitalWrite(mh21, LOW);
          digitalWrite(mh22, LOW);
  
          digitalWrite(mv11, LOW);
          digitalWrite(mv12, LOW);
          digitalWrite(mv21, LOW);
          digitalWrite(mv22, LOW);

            if(text[1]=='T' && count==0){
              Serial.print("throw");
              delay(2000);
              myservo.write(0);
              for (pos = 0; pos <= 70; pos += 1) {
                myservo.write(pos);              // tell servo to go to position in variable 'pos'
                delay(5);                       // waits 15ms for the servo to reach the position
              }
              for (pos = 70; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
                myservo.write(pos);              // tell servo to go to position in variable 'pos'
                delay(5);                       // waits 15ms for the servo to reach the position
              }
              delay(2000);
              count++;
            }
        }
        else if(text[1]=='D'){
          Serial.println("D");
          digitalWrite(mv11, LOW);
          digitalWrite(mv12, HIGH);
          digitalWrite(mv21, LOW);
          digitalWrite(mv22, HIGH);

          digitalWrite(mh11, LOW);
          digitalWrite(mh12, LOW);
          digitalWrite(mh21, LOW);
          digitalWrite(mh22, LOW);

          if(text[2]=='1'){
            pwm1=40;
            pwm2=40;
          }
          else if(text[2]=='2'){
            pwm1=65 ;
            pwm2=52;
          }
          else if(text[2]=='3'){
            pwm1=35;
            pwm2=35;
          }
          pwm1 = (pwm1 * 255) / 100;
          pwm2 = (pwm2 * 255) / 100;
          analogWrite(mv1e, pwm1);
          analogWrite(mv2e, pwm2);
        }
        else if(text[1]=='U'){
          Serial.println("U");
          digitalWrite(mv11, HIGH);
          digitalWrite(mv12, LOW);
          digitalWrite(mv21, HIGH);
          digitalWrite(mv22, LOW);

          digitalWrite(mh11, LOW);
          digitalWrite(mh12, LOW);
          digitalWrite(mh21, LOW);
          digitalWrite(mh22, LOW);
          
          if(text[2]=='1'){
            pwm1=45;
            pwm2=33;
          }
          else if(text[2]=='2'){
            pwm1=62;
            pwm2=55;
          }
          else if(text[2]=='3'){
            pwm1=35;
            pwm2=35;
          }
          
          pwm1 = (pwm1 * 255) / 100;
          pwm2 = (pwm2 * 255) / 100;
          
          analogWrite(mv1e, pwm1);
          analogWrite(mv2e, pwm2);
        }
        else if(text[1]=='L'){
          Serial.println("L");
          digitalWrite(mh11, HIGH);
          digitalWrite(mh12, LOW);
          digitalWrite(mh21, HIGH);
          digitalWrite(mh22, LOW);

          digitalWrite(mv11, LOW);
          digitalWrite(mv12, LOW);
          digitalWrite(mv21, LOW);
          digitalWrite(mv22, LOW);
          
          if(text[2]=='1'){
            pwm1=40;
            pwm2=40;
          }
          else if(text[2]=='2'){
            pwm1=60;
            pwm2=54;
          }
          else if(text[2]=='3'){
            pwm1=35;
            pwm2=35;
          }
          pwm1 = (pwm1 * 255) / 100;
          pwm2 = (pwm2 * 255) / 100;
          
          analogWrite(mh1e, pwm1);
          analogWrite(mh2e, pwm2);
        }
        else if(text[1]=='R'){
          Serial.println("R");
          digitalWrite(mh11, LOW);
          digitalWrite(mh12, HIGH);
          digitalWrite(mh21, LOW);
          digitalWrite(mh22, HIGH);

          digitalWrite(mv11, LOW);
          digitalWrite(mv12, LOW);
          digitalWrite(mv21, LOW);
          digitalWrite(mv22, LOW);

          if(text[2]=='1'){
            pwm1=40;
            pwm2=40;
          }
          else if(text[2]=='2'){
            pwm1=60;
            pwm2=56;
          }
          else if(text[2]=='3'){
            pwm1=35;
            pwm2=35;
          }
          pwm1 = (pwm1 * 255) / 100;
          pwm2 = (pwm2 * 255) / 100;

          analogWrite(mh1e, pwm1);
          analogWrite(mh2e, pwm2);
        }
        
      }

      Serial.println("END");
      Serial.println("");
      Serial.println("");
    }
  }
}

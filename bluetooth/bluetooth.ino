#include <Arduino.h>
// Altered by MW
/*
* Bluetooh Basic: LED ON OFF - Avishkar
* Coder - Mayoogh Girish
* Website - http://bit.do/Avishkar
* Download the App : https://github.com/Mayoogh/Arduino-Bluetooth-Basic
* This program lets you to control a LED on pin 13 of arduino using a bluetooth module
*/


char data = 0;            //Variable for storing received data
void test();

void setup()
{
    Serial.begin(9600);   //Sets the baud for serial data transmission
    pinMode(13, OUTPUT);  //Sets digital pin 13 as output pin
    pinMode(12, OUTPUT);
}

void loop()
{
   if(Serial.available() > 0)      // Send data only when you receive data:
   {
      data = Serial.read();        //Read the incoming data & store into data
      Serial.print(data);          //Print Value inside data in Serial monitor
      Serial.print("\n");

      switch (data){
        case '1':                    // Checks whether value of data is equal to 1
         //digitalWrite(13, HIGH);   //If value is 1 then LED turns ON
         digitalWrite(13, HIGH);   //If value is 1 then LED turns ON
         break;

        case '0':         //  Checks whether value of data is equal to 0
          digitalWrite(13, LOW);    //If value is 0 then LED turns OFF
          break;

        case '2':
          test();
          break;

        case '3':
          digitalWrite(12, HIGH);   //If value is 1 then relay turns ON
          break;

        case '4':
          digitalWrite(12, LOW);   //If value is 1 then relay turns OFF
          break;
     }
   }
}

void test()
{
  Serial.println("Blocking while running the routine.");
  for (int i = 0; i< 20; i++)
  {
    Serial.print(i);
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
  }
  Serial.println("\nRoutine compleetd.");

}


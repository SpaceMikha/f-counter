#include <Arduino.h>
#include "f_controller.h"


// Definir pines para LEDs
const int FController::LED_PINS[5] ={2, 3, 4, 5, 6};

// Constructor
FController::FController() : currentFCount(0) {}


// Iniciar
void FController::begin() {
  for (int i = 0; i < NUM_LEDS; i++) {

    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW);
  }
  Serial.println("Controlador de dedos inicializado.");
}

// Contador
void FController::setFCount(int count){
  if (count >= 0 && count <=5){
    currentFCount = count;
    updateLEDs();
  }
}

// Establecer la cantidad de dedos
void FController::updateLEDs(){
  for (int i = 0; i < NUM_LEDS; i++) {
    if (i < currentFCount) {
      digitalWrite(LED_PINS[i], HIGH);
    }else {
      digitalWrite(LED_PINS[i], LOW);
    }
  }
}

// Test de LEDs
void FController::testLEDs() {
  Serial.println("Probando LEDs...");
  for(int i = 0; i <= 5; i++) {
    setFCount(i);
    delay(500);
  }
  setFCount(0);
  Serial.println("Test de LEDs completada. ");
}

// Getter
int FController::getCurrentFCount() const {
  return currentFCount;
}

// Variable globales 
FController fController;
String inputString = "";
bool stringComplete = false;

void setup() {
  Serial.begin(9600);
  Serial.println("--- Contador Arduino ---");

  fController.begin();

  Serial.println("Listo para recibir los datos.");
  Serial.println("Comandos: 0-5, 'test'");
}

void loop() {
  // Procesar los datos del puerto de serie
  if (stringComplete) {
    inputString.trim();

    if(inputString == "test"){
      fController.testLEDs();
    } else {
      int fCount = inputString.toInt();
      if (fCount >= 0 && fCount <= 5){
        fController.setFCount(fCount);
        Serial.println("Cuento de dedos puesto en: ");
        Serial.println(fCount);
      } else {
          Serial.println("Cuenta de dedos invalida. Utilice apenas entre 1 a 5 dedos.");
      }
    }

    //Limpiar string
    inputString = "";
    stringComplete = false;
  }
}

// Evento de recepcion de serie
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    }else {
      inputString += inChar;
    }
  }
}
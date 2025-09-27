#ifndef F_CONTROLLER_H
#define F_CONTROLLER_H

#include <Arduino.h>

class FController {
private:
    static const int LED_PINS[5];
    static const int NUM_LEDS = 5;
    int currentFCount;

public:
    FController();
    void begin();
    void setFCount(int count);
    void updateLEDs();
    void testLEDs();

    int getCurrentFCount() const;
};

#endif
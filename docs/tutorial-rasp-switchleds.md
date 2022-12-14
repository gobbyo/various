---
title: Light up an LED 
description: #Required; article description that is displayed in search results. 
author: jbeman@hotmail.com
---

# Tutorial: Light up an LED bar

![lnk_switchleds]

<!-- 3. Tutorial outline 
Required. Use the format provided in the list below.
-->

In this tutorial, you learn how to:

- Connect an ..
- Test the ...

## Prerequisites

Completed the 

Supplies:

|Quantity  |Item  |
|:---:|:---|
|1     | Breadboard |
|6     | Male to male jumper wires |
|2    | LEDs |
|1 | Momentary Push Button 4Pin Switch |
|1     | 1kΩ Resistor |
|1     | 10kΩ Resistor |
|1     | (optional) GPIO Extension Board |
|1     | (optional) 40 pin GPIO cable |

Below is the circuit we'll construct.

![lnk_schematicswitchleds]

## Wire your Switch and LEDs

In this section you'll wire your Raspberry Pi to light up an LED display bar by using the following diagram.

1. From the Raspberry Pi, connect the LED display bar to your breadboard so the cathode pins (-) are on the left of the breadboard separation line and the anode pins (+) on the right. Note that anode (+) pins on the LED display bar are located on the same side as the printed identifier.

   [todo]

1. Connect a lead from each 220Ω resistor to each LED display bar cathode pin and the other resistor lead connected to the breadboard's bus (rail) strip.
1. Connect a jumper wire from the resistor's rail strip to a ground pin on your Raspberry Pi.
1. Connect one end of the jumper wire to a terminal strip that corresponds to each Raspberry GPIO Pins #8, #12, #16, #18, #22, #24, #26, #32, #36, and #38.
1. For each jumper wire, connect each GPIO pin to each anode pin on your LED display bar. Note the order is important--the jumper to pin #8 connected to the first anode pin on the LED display bar, the jumper to pin #12 to the second anode pin, etc.

![lnk_raspledbar]

## Create Code to Turn Sequentially Switch On or Off the LED Graph
<!-- Introduction paragraph -->
1. [Connect to your Raspberry Pi](https://code.visualstudio.com/docs/remote/ssh#_connect-to-a-remote-host) using Visual Studio Code.
1. Create a file `ledbar.py` in your cloned GitHub under the `python/raspberrypi` directory, for example `~/repos/IoT/python/raspberrypi/ledbar.py`
1. Copy and paste the following import statement

    ```python
    import RPi.GPIO as GPIO
    import time
    ```

1. Copy and paste the following method to obtain basic information about your Raspberry Pi. [todo] explain this!

    ```python
    def main():
        LED_pins = [8,12,16,18,22,24,26,32,36,38]
    
        GPIO.setmode(GPIO.BOARD)
    
        for p in LED_pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, GPIO.HIGH)
    
        try:
            on = True
            while True:
                for p in LED_pins:
                    if on:
                        GPIO.output(p, GPIO.LOW)
                    else:
                        GPIO.output(p, GPIO.HIGH)
                    time.sleep(0.25)
                if(on):
                    on = False
                else:
                    on = True
                time.sleep(2)
        except KeyboardInterrupt:
            print("Program shut down")
        finally:
            GPIO.cleanup()
            print("Cleaning up and shutting down")
    
    if __name__ == "__main__":
        main()
    ```

## Run It
<!-- Introduction paragraph -->
1. Start the debugger in Visual Studio Code
1. Verify your LEDs in the bar graph sequentially turn on and off.

## More to Explore

1. Produce different patterns of turning on and off your LED bar display.
1. Reverse the polarity of your LED bar graph:
    - Flip the LED bar graph to have the anode (+) pins connected to the resistors
    - Change the jumper lead from ground to a 3.3v pin
    - Change all occurrences in the code from GPIO.LOW to GPIO.HIGH and GPIO.HIGH to GPIO.LOW

## Next steps

[Tutorial: Remotely Control an LED Bar Graph](tutorial-rasp-remoteled.md)

<!--images-->

[lnk_switchleds]: media/tutorial-rasp-switchleds/switchleds.gif
[lnk_schematicswitchleds]: media/tutorial-rasp-switchleds/schematicswitchleds.png

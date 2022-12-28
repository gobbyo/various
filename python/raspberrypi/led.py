try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

def printInfo():
    print("Manufacturer = %s"%GPIO.RPI_INFO['MANUFACTURER'])
    print("Processor = %s"%GPIO.RPI_INFO['PROCESSOR'])
    print("-------")

def main():
    LED_channel = 17

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_channel, GPIO.OUT)
    GPIO.output(LED_channel, GPIO.LOW)

    print("Press Ctrl-C to quit'")

    try:
        while True:
            s = input("Type 'On', 'Off', or 'Info': ")
            if s == 'On':
                GPIO.output(LED_channel, GPIO.HIGH)
                print("On")
            elif s == 'Info':
                printInfo()
            else:
                GPIO.output(LED_channel, GPIO.LOW)
                print("Off")
            print("-----")
    except KeyboardInterrupt:
        print("Program shut down by user")
    finally:
        GPIO.cleanup()
        print("Cleaning up and shutting down")

if __name__ == "__main__":
    main()
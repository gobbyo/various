---
title: Remotely Control an LED 
description: #Required; article description that is displayed in search results. 
author: jbeman@hotmail.com
---

# Tutorial: Remotely Control an LED

In this tutorial, you learn how to:

- Connect your Raspberry Pi to IoT Hub using the Device Provisioning Service
- Use custom properties to set the LED
- Receive a remote command and use the message custom properties to set the LED state

Following the diagram below.

1. You'll use Visual Studio Code to remotely connect to your Raspberry Pi and create listener code to receive messages and change the state of the LED.
1. When you start the code, your Raspberry Pi will use the Device Provisioning Service to create an IoT device client.
1. You'll use the IoT device client to connect to IoT Hub and await for incoming messages.
1. You'll use a local instance of Visual Studio Code to send a message to your Raspberry Pi.
1. The listener program receives the incoming message.
1. The listener program reads the custom LED property (on or off) then changes the state of the LED accordingly.

    ![lnk_ledremotemsg]

## Prerequisites

- Completed the tutorial to [Light up an LED](tutorial-rasp-led.md)

## Code your Raspberry Pi to Receive Messages to Light the LED

1. [Remotely connect to your Raspberry Pi](tutorial-rasp-connect.md#set-up-remote-ssh-with-visual-studio-code).
1. Create a file `remoteled.py` and save it in the `python/rasberrypi` directory from your GitHub forked clone, for example `~/repos/IoT/python/raspberrypi/remoteled.py`. This is a message listener program that runs on your Raspberry Pi.
1. Copy and paste the following import statements into your `remoteled.py` file.

    ```python
    import RPi.GPIO as GPIO
    import asyncio
    import time
    from decouple import config
    from azure.iot.device import Message, X509
    from azure.iot.device.aio import ProvisioningDeviceClient, IoTHubDeviceClient
    ```

1. Copy and paste the following variables following your import statements from the previous step. Note the `DPS_HOST`, `DPS_SCOPEID`, and `DPS_REGISTRATIONID` will need to be added to your [`.env` file](howto-connectionstrings.md), see the following table for details.

    ```python
    LED_channel = 17
    provisioning_host = config("DPS_HOST")
    id_scope = config("DPS_SCOPEID")
    registration_id = config("DPS_REGISTRATIONID")
    ```

    | **Connection Variable Name**  | **Value Found in portal.azure.com**  | **Details about finding the value**  |
    |:---------|:---------|:---------|
    | DPS_HOST | Device Provisioning Service > Overview > Service Endpoint | For example, "dpsztputik7h47qi.azure-devices-provisioning.net" |
    | DPS_SCOPEID | Device Provisioning Service > Overview > ID Scope | For example, "0ne008D45AC" |
    | DPS_REGISTRATIONID | Device Provisioning Service > Settings > Manage enrollments > Individual Enrollments | This is the value you provided in the tutorial [Create a x509 Certificate and Enroll Your Device](tutorial-dpsx509deviceenrollment.md) |

1. Copy and paste the following function. Note the code `message.custom_properties['LED']` gets the LED value of `On` or `Off`.

    ```python
    def message_handler(message):
        print("--Message Received--")
        try:
            s = message.custom_properties['LED']
            if s == 'On':
                GPIO.output(LED_channel, GPIO.HIGH)
                print("On")
            else:
                GPIO.output(LED_channel, GPIO.LOW)
                print("Off")
        finally:
            print("--Message Processed--")
    ```

1. Copy and paste the main function. You should be familiar with all the code as presented in previous tutorials.

    ```python
    async def main():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_channel, GPIO.OUT)
        GPIO.output(LED_channel, GPIO.LOW)
    
        print("Ctrl-C to quit'")
        print("Creating x509 cert object from file. Code id = e28c4236-60bb-4d45-adad-2a1b5cd0302e")
        x509 = X509(
            cert_file=config("X509_CERT_FILE"),
            key_file=config("X509_KEY_FILE"),
            pass_phrase=config("X509_PASS_PHRASE"),
        )
    
        print("Creating provisioning client from certificate. Code id = 7dc43b15-f17b-4f17-9446-8d26b1e188d2")
        provisioning_device_client = ProvisioningDeviceClient.create_from_x509_certificate(
            provisioning_host=provisioning_host,
            registration_id=registration_id,
            id_scope=id_scope,
            x509=x509,
        )
    
        print("Registering provisioning client. Code id = 4d906cc4-61a9-4fe2-ab6e-4e397f63a702")
        registration_result = await provisioning_device_client.register()
    
        if registration_result.status == "assigned":
            device_client = IoTHubDeviceClient.create_from_x509_certificate(
                x509=x509,
                hostname=registration_result.registration_state.assigned_hub,
                device_id=registration_result.registration_state.device_id,
            )
    
        print("Connecting client to IoT hub. Code id = 6893e706-291e-44f5-8623-fea84046866a")
        await device_client.connect()
    
        device_client.on_message_received = message_handler
    
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            print("Program shut down by user")
        finally:
            GPIO.cleanup()
            await device_client.shutdown()
            print("Cleaning up and shutting down")
    
    if __name__ == "__main__":
        asyncio.run(main())
    ```

1. Run the message listener on your Raspberry Pi from Visual Studio Code.

    ```python
    $ ~/repos/IoT $ /bin/python /home/me/repos/IoT/python/raspberrypi/remoteled.py
    /home/me/repos/IoT/python/raspberrypi/remoteled.py:28: RuntimeWarning: This channel is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.
      GPIO.setup(LED_channel, GPIO.OUT)
    Ctrl-C to quit'
    Creating x509 cert object from file. Code id = e28c4236-60bb-4d45-adad-2a1b5cd0302e
    Creating provisioning client from certificate. Code id = 7dc43b15-f17b-4f17-9446-8d26b1e188d2
    Registering provisioning client. Code id = 4d906cc4-61a9-4fe2-ab6e-4e397f63a702
    Connecting client to IoT hub. Code id = 6893e706-291e-44f5-8623-fea84046866a
    ```

## Send a Remote Command to Turn the LED On or Off

In this section you'll create a program that runs locally to send a command to IoT Hub. Note the command to turn the LED on or off is sent as a custom property and not using the payload.

1. From your windows machine, create a file `c2dsendmsg.py` in your cloned GitHub under the `python\raspberrypi` directory, for example `c:\repos\IoT\python\c2dsendmsg.py`
1. Copy and paste the following import statement

    ```python
    from uuid import uuid4
    from azure.iot.hub import IoTHubRegistryManager
    import os
    ```

1. Copy and paste the following main function to send a message to your device from the cloud.

    ```python
    def main():
        deviceId = input("Device id: ")
        s = input("On or Off: ")
        # Add any json to the payload as the content type is set to json
        payload = '{ "remote call": "Update LED" }'
        props={}
    
        try:
            registry_manager = IoTHubRegistryManager(os.getenv("IOTHUB_CONNECTION_STRING"))
            
            # assign system properties
            props.update(messageId = "{0}".format(uuid4()))
            props.update(contentType = "application/json")
            # assign 
            props.update(LED = s)
    
            registry_manager.send_c2d_message(deviceId, payload, props)
        except Exception as ex:
            print ( "Unexpected error {0}" % ex )
    
    if __name__ == "__main__":
        main()
    ```

<!-- Introduction paragraph -->
1. Run the program from Visual Studio Code, provide your device id, then type 'On' when prompted in the `TERMINAL`. For example,

    ```azurecli
    PS C:\repos\IoT> & C:/Users/me/AppData/Local/Microsoft/WindowsApps/python3.10.exe c:/repos/IoT/python/c2dsendmsg.py
    Device id: raspberrypi2
    On or Off: On
    ```

1. Verify your LED turns on when prompted and note the print statement from the code running on your Raspberry Pi.  For example,

    ```azurecli
    --Message Received--
        On
    --Message Processed--
    ```

## More to Explore

1. Change the message listener and sender code so the LED state is passed using the message payload instead of a custom property.
1. Set up the listener as a cron job that starts when your Raspberry Pi starts up or is rebooted.
1. Add Green, Yellow, and Red LEDs to your Raspberry Pi and remotely control them by color

## Next steps

[Tutorial: Light up an LED bar](tutorial-rasp-ledbar.md)

<!--images-->

[lnk_ledremotemsg]: media/tutorial-rasp-remoteled/ledremotemsg.png

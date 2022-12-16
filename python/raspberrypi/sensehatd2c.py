from datetime import datetime
from decouple import config
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import exceptions
from sense_hat import SenseHat
import os
import logging
import datetime

def main():
    try:
        sense = SenseHat()
        client = IoTHubDeviceClient.create_from_connection_string(config("IOTHUB_DEVICE_CONNECTION_STRING"))
        success = True
        f = (sense.temperature * 9/5) + 32
        msg = '{ "sent_utc":"%sZ", "fahrenheit":"%3.0f", "humidity":"%3.0f", "pressure":"%3.0f" }'%(datetime.utcnow().isoformat(),f,sense.humidity,sense.pressure)
        client.send_message(msg)
        
        path = os.getcwd() + '/log{0}.txt'.format(datetime.datetime.utcnow().strftime("%Y%m%d"))
        logging.basicConfig(filename=path, filemode='a', level=logging.DEBUG)
        logging.info(msg)

    except exceptions as e:
        logging.error(e)
    finally:
        # Graceful exit
        sense.clear()

if __name__ == "__main__":
    main()
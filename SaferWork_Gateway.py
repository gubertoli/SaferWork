#
# Dragonboard 410c - SaferWork 4.0 Gateway
#
# Receives JSON packages through UART using a HC-12 chip
#
# Required python-serial and requests:
#   sudo apt-get install python-pip
#   sudo pip install pyserial
#   sudo pip install requests
#


import serial
import time
import requests
import json
from GPIOProcessor import GPIOProcessor

ser = serial.Serial('/dev/tty96B0',baudrate=9600)

# dweet.io configuration
thingname = "SaferWork_Prototype"
dweet_url = "https://dweet.io:443/dweet/for/"

def config():
    # HC-12 Configuration
    # Using UART port from Low Speed Connector (PINs 5 and 7)
    
    time.sleep(2)
    
    GP = GPIOProcessor()
                        
    SETPin = GP.getPin29()      # HC-12 SET Pin connected to DB410C LS pin 29
    
    SETPin.out()                # Defined as output
    print ">> SET PIN ---> " + SETPin.getDirection()
    print ">> SET PIN ---> LOW (AT Command)"
    SETPin.low()                # Enter to AT Command
    print ">> HC-12 Set to Default (FU3 / 9600bps / CH1 433.4MHz)"
    ser.write("AT+DEFAULT")     # SET HC-12 Default Configuration
    time.sleep(1)
    SETPin.high()               # Enter Transparent Mode
    print ">> SET PIN ---> HIGH (Transparent Mode)"
    time.sleep(2)
    print ">> HC-12 Setup OK!"

    # Usage
    ser.write("[rf_msg] Dragonboard (Gateway) to Device")
    GP.cleanup()
    time.sleep(2)

# procedure to send data to dweet.io
def send_data(thingname, data):
    rqsString = dweet_url+thingname+'?'+str(data)
    print rqsString
    try:
        rqs = requests.get(rqsString, timeout=10)
        print rqs.status_code
    except requests.exceptions.RequestException as e:
        print e
    except KeyboardInterrupt:
        raise

def main():
    config()
    # Infinite Loop for Data Receiver (Gateway)
    while True:
        jsonPackage = ser.readline()
        data = json.loads(jsonPackage)
        deviceId = data['DeviceID']
        temp = data['data'][1]
        humidity = data['data'][0]
        mq2 = data['data'][2]
        mq9 = data['data'][3]
        mq135 = data['data'][4]
        jsonPackage = "deviceId="+str(deviceId)+"&temp="+str(temp)+"&humidity="+str(humidity)+"&mq2="+str(mq2)+"&mq9="+str(mq9)+"&mq135="+str(mq135)
        send_data(thingname,jsonPackage)
    
    ser.close()

if __name__ == "__main__":
    main()


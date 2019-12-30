import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import paho.mqtt.client as mqtt # Import paho MQTT Client library
import ssl    # Import SSL for Security Certificates
import base64 # Import base64 library for base64 string
import json   # Import JSON library of Python for json data
import time   # Import time module for time-related task
import os     # Import os moduledor interacting with file system
import cv2
import sys
from MFRC522_python import MFRC522
import signal
from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)

#Function to rotate the motor 
def SetAngle(angle):
        pwm.start(0)
        duty = angle / 18 + 2
        GPIO.output(3, True)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(3, False)
        print("in")
        pwm.ChangeDutyCycle(0)
    


def end_read(signal,frame):
        global continue_reading
        print ("Ctrl+C captured, ending read.")
        continue_reading = False
        GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)


id=0           
rfflag=0 #define the radio_frequecy flag
mflag=0  #define the message flag
MIFAREReader = MFRC522.MFRC522()

#The functon to defined to get the RFID of detected card 
def get_rfid():
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
                print ("Card detected")
        
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

                # Print UID
                print ("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
        
                # This is the default key for authentication
                c_id=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
                print(c_id)
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                d={
                "rfid":str(c_id)
                }
                j=json.dumps(d)
                c.publish("candy_data_fetch",j)
                mflag=0
                for i in range(10):
                c.loop()
        
                return c_id
                
                # Select the scanned tag
        
        return 0
        

GPIO.setwarnings(False)  # Ignore warning for now
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(29,GPIO.OUT)   # GPIO pin 7 set for output LED
GPIO.setup(31,GPIO.OUT)  # GPIO pin 11 set for output LED
GPIO.setup(33,GPIO.OUT)  # GPIO pin 13 set for output LED
GPIO.setup(36,GPIO.OUT)  # GPIO pin 13 set for output LED
GPIO.setup(37,GPIO.OUT)  # GPIO pin 13 set for output LED
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING) # Setup event on pin 10 rising edge

#connection to AWS
rootca=r'root-CA.crt' #define the variable for root certificate
keyfile=r'be40cc8234-private.pem.key' #define the variable for private key
certificate=r'be40cc8234-certificate.pem.crt' #define the variable for certificate
c=mqtt.Client() #define variable to connect with MQTT Client

c.tls_set(rootca,certfile=certificate,keyfile=keyfile,cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLSv1_2,ciphers=None) #Enable SSL/TLS connection
c.connect('your-thing-arn',8883) #Connect with the thing on AWS

c.subscribe("emotion_data") #Subscribe to the topic on MQTT
c.subscribe("candy_data")    #Subscribe to the topic in lambda function


        
#The callback for when the client receives a CONNACK response from the server.
def onc(c,userdata,flags,rc):
        print("Succesfully connected to Amazon with RC",rc)
        c.subscribe("emotion_data")
    
# The callback for when a PUBLISH message is received from the server.
def onm(c,userdata,msg):
                
        m=msg.payload.decode()
        
        global rfflag
        global mflag
        mflag=1
        if(msg.topic=="candy_data"):
                if(m=="data not found"):
                rfflag=1

                print("THE RFID IS OF INVALID USER")
                        
                else:
                print("Hello, "+str(m))
                rfflag=0
        
                
                
                
        if m== 'HAPPY':
                print ("SMILE ALWAYS AND BE HAPPY")
                GPIO.output(29,GPIO.HIGH)
                time.sleep(3)
                GPIO.output(29,GPIO.LOW)
                time.sleep(1)
                SetAngle(25)
                
        elif m== 'SAD':
                print("DONT BE SAD HAVE A SMILE")
                GPIO.output(31,GPIO.HIGH)
                time.sleep(3)
                GPIO.output(31,GPIO.LOW)
                time.sleep(1)
                SetAngle(50)
        elif m== 'CALM':
                print("STAY CALM AND HAVE PATIENCE")
                GPIO.output(33,GPIO.HIGH)
                time.sleep(3)
                GPIO.output(33,GPIO.LOW)
                time.sleep(1)
                SetAngle(90)
        elif m== 'ANGRY':
                print("DONT BE ANGRY BE CALM")
                GPIO.output(36,GPIO.HIGH)
                time.sleep(3)
                GPIO.output(36,GPIO.LOW)
                time.sleep(1)
                SetAngle(115)
        elif m== 'DISGUSTED':
                print("DONT BE MANSI")
                GPIO.output(37,GPIO.HIGH)
                time.sleep(3)
                GPIO.output(37,GPIO.LOW)
                time.sleep(1)
                SetAngle(140)
        
           
    
c.on_message=onm

#The core algorithm starts


while(True):

        #k=0
        while get_rfid()==0:
                pass
        
        #print(k)
        while(rfflag==0):
                #print("in")
                if GPIO.event_detected(10):
                        video = cv2.VideoCapture(0)
                        print('BUTTON IS PRESSED')
                        success, image = video.read()
                        cv2.imwrite('s.jpg', image)
                        f=open("s.jpg","rb")
                        if(f):
                                str1 = base64.b64encode(f.read())

                        d={
                                'm':str1.decode('utf-8')
                        }
                        j=json.dumps(d)
                        c.publish("emotion_fetch",j)
                        
                        
                        video.release()
                        for i in range(0,10):
                                c.loop()
                        break
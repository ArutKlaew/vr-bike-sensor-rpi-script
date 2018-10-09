import RPi.GPIO as GPIO
import time
import socket
from random import randint
from config import IP, PORT
from time import sleep


class Broadcaster:
    def __init__(self):
        self.position = 0
        self.zVelocity = 0
        self.BroadcasterState = 0
        self.connection = socket.socket()

    def connectToSever(self,ipAdress,port):
        self.connection.connect((ipAdress,port))

    def setId(self, i):
        self.id = i
        
    ###################
    ## PUBLIC GETTER ##
    ###################

    def tagClient(self):
        command = '"tagClient",\n'
        command = command.encode("utf-8")
        self.connection.send(command)
        
    def getFrequency(self,i):
        command = '"getFrequency",'+str(i)+'\n'
        command = command.encode("utf-8")
        self.connection.send(command)
        result = self.connection.recv(1024)
        result = result.decode("utf-8")
        return result
    
    def getVelocity(self):
        command = '"getVelocity",'+str(self.id)+'\n'
        command = command.encode("utf-8")
        self.connection.send(command)
        result = self.connection.recv(1024)
        result = result.decode("utf-8")
        return result

    def getPosition(self):
        command = '"getPosition",'+str(self.id)+'\n'
        command = command.encode("utf-8")
        self.connection.send(command)
        result = self.connection.recv(1024)
        result = result.decode("utf-8")
        
        return result

    def getBroadcasterState(self):
        command = '"getBroadcasterState",'+str(self.id)+'\n'
        command = command.encode("utf-8")
        self.connection.send(command)
        result = self.connection.recv(1024)
        result = result.decode("utf-8")
        return result

    ###################
    ## PUBLIC SETTER ##
    ###################
    def setFrequency(self,frequency,sensor_num):
        command = "'setFrequency'," + str(frequency)+','+str(sensor_num)+'\n'
        command = command.encode("utf-8")
        self.connection.send(command)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

first_input_pin = 20
second_input_pin = 21

GPIO.setup(first_input_pin, GPIO.IN)
GPIO.setup(second_input_pin, GPIO.IN)
        
p1 = Broadcaster()
p1.setId(0)

hostName = socket.gethostbyname(IP)
p1.connectToSever(hostName,PORT)
##p1.tagClient()
##
def calculate_frequency(_id,pin, pfs=[0,0,0], readtime1=[time.time() for i in range(3)], readtime2=[0,0,0],frequency = [0,0,0],counter=[0,0,0]):
    previous_frame_status = pfs
    sensorReadDetected = bool(GPIO.input(pin) == GPIO.HIGH)
    statusJustChanged = (previous_frame_status[_id] != sensorReadDetected)
    print("GPIO status: ", sensorReadDetected)
    if(not statusJustChanged):
        frequency[_id] = frequency[_id] - 0.21
        if(frequency[_id] <= 0):
            frequency[_id] = 0
        print("Status unchanged: ", frequency[_id], _id)
        p1.setFrequency(frequency[_id],_id)
        counter[_id] = time.time()
    else:
        if(statusJustChanged):
            if(previous_frame_status[_id] == True):
                readtime2[_id] = time.time()
                period = readtime2[_id]-readtime1[_id]
                frequency[_id] = 1/period #frequency celcolatte hyahhh
                readtime1[_id] = readtime2[_id]
                p1.setFrequency(frequency[_id],_id)
                print("Status changed: ", frequency[_id], _id)
                counter[_id] = time.time()
        previous_frame_status[_id] = sensorReadDetected

while True:
    try:
        calculate_frequency(2, first_input_pin)
        calculate_frequency(1, second_input_pin)
        sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()

    

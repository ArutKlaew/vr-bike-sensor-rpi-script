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

    def connectToSever(self, ipAdress, port):
        self.connection.connect((ipAdress, port))

    def setId(self, i):
        self.id = i

    ###################
    ## PUBLIC GETTER ##
    ###################

    def tagClient(self):
        command = '"tagClient",\n'
        command = command.encode("utf-8")
        self.connection.send(command)

    def getFrequency(self, i):
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
    def setFrequency(self, frequency, sensor_num):
        command = "'setFrequency'," + str(frequency)+','+str(sensor_num)+'\n'
        command = command.encode("utf-8")
        self.connection.send(command)

# p1.tagClient()
##




def update_frequency(input_pin, sensor_num, previous_frequency, last_time_active, broadcaster):

    input_status = GPIO.input(input_pin)
    print("Sensor Number:",sensor_num)


    if input_status == 1:
        active_time = time.time()
        period = active_time - last_time_active
        frequency = 1 / period
        print("New Frequency:", frequency / 2000 * 7.5)
        broadcaster.setFrequency(frequency / 2000 * 7.5, sensor_num)
        return frequency, active_time
    else:
        
        frequency = (previous_frequency - 0.2) if previous_frequency - 0.2 > 0 else 0
        print("Old Frequency:", frequency / 2000 * 7.5)
        broadcaster.setFrequency(frequency / 2000 * 7.5, sensor_num)
        return frequency, last_time_active


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

first_input_pin = 20
second_input_pin = 21

GPIO.setup(first_input_pin, GPIO.IN)
GPIO.setup(second_input_pin, GPIO.IN)

first_broadcaster = Broadcaster()
first_broadcaster.setId(0)

second_broadcaster = Broadcaster()
second_broadcaster.setId(1)

hostName = socket.gethostbyname(IP)

first_broadcaster.connectToSever(hostName, PORT)
second_broadcaster.connectToSever(hostName, PORT)

active_time = time.time()
frequencies = [0,0]
active_times = [active_time, active_time]
sensor_nums = [0,1]
pins = [first_input_pin, second_input_pin]
broadcasters = [first_broadcaster, second_broadcaster]


while True:
    try:
        for i in range(2):
            frequencies[i], active_times[i] = update_frequency(pins[i], sensor_nums[i], frequencies[i], active_times[i], broadcasters[i])
        sleep(0.0001)
    except KeyboardInterrupt:
        GPIO.cleanup()

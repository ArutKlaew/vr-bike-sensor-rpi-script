import socket
from time import sleep, time
import RPi.GPIO as GPIO
from config import PORT, IP


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


def update_frequency(input_pin, sensor_num, previous_frequency, last_time_active, broadcaster):

    input_status = GPIO.input(input_pin)
    print("Sensor Number:", sensor_num)

    if input_status == 1:
        active_time = time()
        period = active_time - last_time_active
        frequency = 1 / period
        print("New Frequency:", frequency / 2000 * 7.5)
        broadcaster.setFrequency(frequency / 2000 * 7.5, sensor_num)
        return frequency, active_time
    else:

        frequency = (previous_frequency -
                     0.2) if previous_frequency - 0.2 > 0 else 0
        print("Old Frequency:", frequency / 2000 * 7.5)
        broadcaster.setFrequency(frequency / 2000 * 7.5, sensor_num)
        return frequency, last_time_active


def main():
     # RPI Mode setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Specify pin number by admin. Use either pin-21 or pin-20
    pin = int(input("Please input pin number (21 or 20): "))
    GPIO.setup(pin, GPIO.IN)

    #Initialize communication using Broadcaster socket Adapter
    broadcaster = Broadcaster()

    #Specify player ID by admin. User either 0 or 1
    player_id = int(input("Specify player ID (0 or 1): "))
    broadcaster.setId(player_id)
    hostname = socket.gethostbyname(IP)
    broadcaster.connectToSever(hostname, PORT)

    frequency = 0
    active_time = time()

    # Reading cycle starts
    while True:
        try:
            frequency, active_time = update_frequency(pin, player_id, frequency, active_time, broadcaster)
        except KeyboardInterrupt:
            GPIO.cleanup()

main()
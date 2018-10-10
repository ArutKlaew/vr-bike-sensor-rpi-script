# vr-bike-sensor-rpi-script

This is the repository containing sensor scripts for KMITL-VR-Bike.

## Getting Started

These are the instructions those are required in order to operate the VR-Bike

### Run the server script.
#### 1. Within the RPI terminal run this command.
```
cd /Desktop/bike-server/sources/
python3 _main.py
```
### Run the sensor script for a specific player.
#### 1. Open a new terminal console.
#### 2. Run this follwing command.
```
cd /Desktop/bike-server/sources/
python3 main_sensor.py
```
Make sure that you have already download the "main_sensor.py" for this repository and put it in /Desktop/bike-server/sources/

#### 3. Input a pin number and a playder ID respectively regarding to the poped-up instructions.
#### 4. In the server console, there should display that a client is joined.

## Suggestion

  Getting started section also be done by using SSH. Please ensures that game clients; Mobile devices, Monitor and sensors,
subscribe to the same IP address and PORT and connect to the same Wifi access point. 
  To configure IP and PORT, please do it in config.py.

# Raspberry PI Temperature with Watson IoT - Docker Container

The goal of this project is to provide a very simple method of getting started with Watson IoT and an MQTT client using a real sensor.  I have selected a DHT11 Temperature and Humidity sensor given the simplicity of how to wire the solution.  This solution is also packaged as a docker container which is a flexible means of deploying to many different environments and the foundation of many "edge" solutions.  This package demonstrates how to build and create the docker container from the ground up.

**This is not meant to be an all-inclusive tutorial to Watson IoT connectivity or how to build docker containers`, but a simple "getting started".  To learn aout the platform and other options for connectivity, please refer to the Watson IoT documentation or Docker documentation**

**Special thanks for the code already included in this repository that helps read the sensor values from the DHT11**
https://github.com/szazo/DHT11_Python.git

Raspberry PI Dependencies

1.  Docker

```console
sudo docker --version
```

## Step 1:  Wire the DHT 11 Sensor to your PI

Follow the instructions here:
https://www.instructables.com/id/DHT11-Raspberry-Pi/

Some hints:
1.  You can do this with simply the DHT11 and 3 Female to Female jumper wires
2.  If you hold the raspberry pi such that the USB inputs are on the right and the Pins are on the top:
    * Wire the first pin on the bottom row to the VCC of the DHT11 - This is 3.3V power
    * Wire the second pin on the top row to the ground (GND) of the DHT11 - this is the ground 
    * Wire the third pin on the 6th pin on the bottom row to the DATA of the DHT11 - this is GPIO Pin 17

## Step 2:  Verify the DHT 11 is working properly

Run the following command to verify that you are receiving values:

```console
python3 dht11_example.py
```

Verify that the temperature and humidity readings are displayed.


```console
Last valid input: 2019-12-17 10:33:59.947765
Temperature: 18.3 C
Temperature: 64.9 F
Humidity: 39.0 %
```

## Step 3:  Sign up for IBM Cloud and Create an IoT Service

1. Sign up for the IBM cloud from this link: 
https://www.ibm.com/cloud
2. After you go through the registration process, login with your IBM ID.
3. Create an instance of the IoT service by clicking "Create Resource" and searchign for IoT
4.  Select "Internet of Things Platform" and a pricing plan (Lite plan or Free works fine to get started)
5.  Launch the Internet of Things platform dashboard.      
**Important:  Take note of your Organization ID which is a 6 character identifier in the upper right hand corner above your name**

## Step 4:  Create a Device Type called "pitemp"

1.  Navigate to Devices and "Create a Device Type".    
**You can name it whatever you want, but the program here uses the device type called "pitemp"**

## Step 5:  Create a new Device called "pi1"

1.  Create a Device Type called "pi1" which is of type "pitemp"
**Again, you can name it whatever you want, but this program assumes the device identifier of "pi1"**

2.  As you walk through the work flow to create a device, it will ask you to generate a device token or type one.  It is generally safer and more secure to have the system automatically create one, but for this exercise just type "12345678".  This token is embedded in the program and is part of the authentication part of the process.  

## Step 6:  Customize your Configuration Values in the Python Script

1.  Edit the program and put it in your specific credentials.  
    * The path to the cert. This must be an absolute path - where you are running this program on the PI
    * Your organization:  The 6 character identification
    * The device token if different than 12345678

```python
# device credentials
ca_absolute_path = '/home/pi/dev/iot-temp/pitemp-wiot-basic/messaging.pem'
iotidentifier = 'pi1'
iotorg = 'cg3orm'
iottype = 'pitemp'

device_id        = 'use-token-auth'      # * set your device id (will be the MQTT client username)
device_secret = '12345678'
random_client_id = 'd:'+iotorg+':'+iottype+':'+iotidentifier      # * set a random client_id (max 23 char)
```

## Step 7:  Run the Program
 

```console
python3 iot-temp.py
```

## Step 8:  Monitor Results in Watson IoT

1.  Navigate to your device under Devices.  Verify that the device shows "Connected"
2.  Navigate to "Recent events" to watch the live JSON IoT data arrive

## Step 9:  Build and Run as Docker Image

**Note:  If you must now change the "ca_absolute_path" variable in the python program to "/app/messaging.pem" since you are running in a docker container now **

```console
docker build --tag iot-temp-wiot .
```
Verify the image has been created using the following command:
```console
docker images
```
You should see something like this:
```console
REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
iot-temp-wiot       latest              10e4e9e338b2        About a minute ago   78.3MB
python              alpine3.7           8888f45dc683        10 months ago        71.8MB
```

If for any reason you want to completely clean up and start over, you can delete everything with this command (but be sure you really want to do it):
```console
docker system prune -a
```

Let's test the image to verify that we can access the DHT11 sensor. The container needs to be run in "privileged" mode to be able to access the GPIO pins.  
```console
docker run --privileged -i -t --rm iot-temp-wiot python3 dht11_example.py
```
This should yield the same output as before, but just running in a docker container.

Let's start the image in a container as a daemon and startup the iot-temp.py, which connects to Watson IoT andsends temperature readings.
```console
docker run --privileged --name iot-temp-wiot -d iot-temp-wiot python3 iot-temp.py
```
To look at the logs in the container to verify there are no errors, use this command:
```console
docker logs -f iot-temp-wiot
```

To look at the running containers, use this command to get the container ID which can be used for start and stop:

```console
docker ps -a
# Example output
CONTAINER ID        IMAGE               COMMAND                 
2365e31e1027        iot-temp-wiot       "python3 iot-temp.py"  
```
Note the container id.  You can use this to start and stop the container now.  See examples below using the container id from above.
```console
docker stop 2365e31e1027
docker start 2365e31e1027
```

Enjoy!

Matt Rothera


## License

This project is licensed under the terms of the MIT license.

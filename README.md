# Angelzzz
A sleep and (hopefully) seizure detector for kids with Angelman Syndrome using a beddit 1 sensor

# Challenge
The challange is to build a sleep and seizure for kids with Angelman Syndrome, the device has to be not worn, becaue kids with Angelman Syndrome are senstive to touch

# Hardware
* Beddit 1 sensor that sends bluooth 2 information. 
* Raspberrypi 3/2 with bluetooth/wifi

# Setup Overview
[Here is a video of how you should assemble evreything](https://www.youtube.com/watch?v=UTEvhdu6E9Q)

# Installation
1) Set up a raspberrypi with Raspbian that is conencted to the internet

2) Run:

~~~
cd /home/pi
git clone https://github.com/Tikkun-olam/angelzzz.git
cd angelzzz/src
bash ./install_deps.sh
~~~

3) Pair your beddit to your raspberrypi using

~~~
sudo bluetoothctl 
# power on
# agent on
# default-agent
# scan on
# pair [beddit MAC]
# trust [beddit MAC]
# connect [beddit MAC]
~~~

4) Place your beddit mac in ``src/config.ini`` (take a look at ``src/config.ini.example`` for example.

5) select your relay type to turn the beddit on and off in the ``[beddit]`` section in ``src/config.ini``

6) To start logging run: ``src/angelzzz_server.py``

7) You can create a service for startup using ``src/add_startup_service.sh``

## Viewing logged data
To output a csv-readable file our of the database stored in ``/home/pi/angelzzz.sql`` run:
``read_results.py > output.csv``

## Control relay setup

The beddit has this bug that it dies after about an hour of recording, and you need to plug out and in to work. To workaround this probolem you can use a digital power socket to do this. There are two types: one controled from a RaspberryPi GPIO and the [Orvibo S20 Wifi Power Socket](https://www.amazon.com/Orvibo-Socket-Electronics-Anywhere-WiWo-S20/dp/B00KT50HK4).

### Set up a Orvibo S20 Wifi Power Socket

To set it up download the app for it and pair it to the same network your Pi is connected to.
Then in ``config.ini``.
For example:

```
[beddit]
mac=00:07:80:17:CD:3D
relay=orvibo
relay_mac=ac:cf:23:97:9b:bc
relay_ip=10.0.0.4
```
Make sure you have both the beddit set up, your relay set to orvibo, relay MAC and relay IP.


### Set up a RaspberryPi GPIO Controlled Power Socket

Make sure to select in the ``config.ini``:

```
[beddit]
relay=gpio
```

1. Set pin 23 to turn on to transmit the on signal
2.  Set pin 24 to turn on to transmit the off signal
These pin settings can be changed in the python script ``src/raspberrypi_gpio.py``

# Specs
* [Beddit protocol](https://github.com/sliedes/beddit-driver/blob/master/protocol.txt)
* [The officlal repo we found](https://github.com/beddit/beddit-python-bt)

# Analysis

# Need Knower information
* Hear trate changes when having a seasure
* Ticking in the head
* Movement of the jaw
* Tempreture change
* Bad sleep habits (on top of the regular ones)


# Old Files
* Currently have a [file that saves all the data to a .csv.gz file](https://github.com/Tikkun-olam/angelzzz/blob/devel/src/bedditbt.py)
* [File to analize the data from the sensor](https://github.com/Tikkun-olam/angelzzz/blob/devel/src/analize_events.py)

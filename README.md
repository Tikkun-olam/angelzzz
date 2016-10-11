# Angelzzz
A sleep and (hopefully) seizure detector for kids with Angelman Syndrome using a beddit 1 sensor

# Challenge
The challange is to build a sleep and seizure for kids with Angelman Syndrome, the device has to be not worn, becaue kids with Angelman Syndrome are senstive to touch

# Hardware
* Beddit 1 sensor that sends bluooth 2 information. 
* Raspberrypi 3/2 with bluetooth/wifi

# Installation
TBD, we are still hacking it together

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


# Files
* Currently have a [file that saves all the data to a .csv.gz file](https://github.com/Tikkun-olam/angelzzz/blob/devel/src/bedditbt.py)
* [File to analize the data from the sensor](https://github.com/Tikkun-olam/angelzzz/blob/devel/src/analize_events.py)

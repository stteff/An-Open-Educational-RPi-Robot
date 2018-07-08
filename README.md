# [OpEdRo] An-Open-Educational-(RPi)-Robot
An Educational Robotic Platform, Raspberry Pi based, using Open Technologies, remote controled from Scratch

***
*`This project is in active development. Additions will be taking place on a regular basis`*
***
### `OpEdRo:-----`
List of main components used:
  * A robot chassis appropriate to host the rest of the parts
  * A Rapsberry Pi 3 model B
  * 2 micro servo motors fitable to robot chassis
  * 2 photoelectric sensors
  * 2 encoder disks
  * 1 battery holder for 4xAA to power the servos
  * 1 power bank for Raspberry Pi
  * 1 small portable speaker with 3.5 mm jack (for the speech engine)
  
  
Raspberry Pi Software used: 

  * Operating system
    * Raspbian Jessie Lite (Lite version uses lower computer resources)
  * Python 2.7.x
  * Python packages / modules
    * [RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/ "RPi.GPIO Wiki") (a class to control the GPIO on a Raspberry Pi, included with OS)
    * [pigpio](http://abyz.me.uk/rpi/pigpio/index.html "The pigpio Documentation") (a library supporting hardware timed servo pulses)
    * [scratchpy](https://github.com/pilliq/scratchpy) (a python client for Scratch)
    * [espeak](http://espeak.sourceforge.net/ "espeak Documentation") (a text to speech engine)
  
### `The Control computer:-----`
  * Any computer capable to run Scratch 1.4 (the version supporting the [Mesh](https://en.scratch-wiki.info/wiki/Mesh) method)
  * Connected to the same LAN as Raspberry Pi

***
***
## Installing and Setting up Raspberry Pi's Operating System
  1. Download [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) image file
  2. Unzip the compressed file
  3. Use the [Etcher](https://etcher.io/) SD card utility (or a similar one) to transfer the Raspbian to the SD card
  4. Connect Raspberry Pi to an internet network using an Ethernet cable and boot
  5. Log in as *pi* user
  6. Invoke the configuration utility *raspi-config*, by typing at the command line interface:
  ```
  sudo raspi-config
  ```
  7. Enable remote command line using ssh, in order to allow remote access to the robot:
  
     7a. Select *Interfacing Options:*
     ![Step 7a](/docs/images/2.png)
     
     7b. Select *SSH:*
     ![Step 7b](/docs/images/3.png)

  8. Set WiFi SSID and pass phrase of the network where robot will be connected:
  
     8a. Select *Network Options:*
     ![Step 8a](/docs/images/4.png)
     
     8b. Select *Wi-fi:*
     
     ![Step 8b](/docs/images/6.png)
   9. Check the wlan (wireless lan) IP assigned. Exit raspi-config and type:
      ```
      ifconfig
      ```
      At the *wlan0:* part of the command output, the new IP should appear
      ![Step 9](/docs/images/7.png)
  10. [Optional] Set a Static IP for the Raspberry Pi
  
      You will need:
  
          i. a valid static IP address (at the example below, *192.168.2.200*)
      
          ii. the router's and domain_name_servers' IP addresses (usually same IP for both, at the example below *192.168.2.1*)
      
      At the command line type:
      ```
      sudo nano /etc/dhcpcd.conf
      ```
      Go to the end of the file and type (adjust accordingly to your IPs):
      ```
      interface wlan0
      static ip_address=192.168.2.200/24
      static routers=192.168.2.1
      static domain_name_servers=192.168.2.1
      ```
      Save changes, exit nano and reboot by typing:
      
      `ctlr+o` + [enter] to confirm write to the file
      
      `ctrl+x` to exit the nano editor
      
      `sudo reboot` reboot for changes to take effect
  
### Remote Access Rapsberry Pi's Command Line, from the Control Computer


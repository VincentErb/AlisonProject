# Hardware requirements

The Alison System requires three main hardware components to function :  

- An android phone with Android version 5.0 Lollipop or later  
  
- A [Philips Hue](https://www2.meethue.com/fr-fr) system with multi-color lightbulb (both lightbulb AND bridge)  
  
- A [Raspberry Pi 3B+](https://www.raspberrypi.org/products) (other versions may be functional but have not yet been tested)  

# Raspberry Pi Software Installation 

## Prerequisites

Your Raspberry Pi must run the latest version of Raspbian available.  
[More info about Raspbian here](https://raspbian.org/ "Raspbian- Main page")

## Installing the Respeaker 4-Mic
- Get the seeed voice card source code
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install swig libpulse-dev libasound2-dev libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh
sudo reboot
```
- Select the headphone jack on Raspberry Pi for audio output
```
sudo raspi-config
Select 7 Advanced Options
Select A4 Audio
Select 1 Force 3.5mm ('headphone') jack
Select Finish
```
- Install the respeaker library
```
sudo apt install python3-pip
pip install pocketsphinx webrtcvad
pip install pyaudio respeaker --upgrade
pip install -U https://github.com/respeaker/respeaker_python_library/archive/master.zip
```
## Packages to install
```
sudo pip install numpy scipy matplotlib soundfile resampy audioread phue netifaces
sudo apt-get install python-tk
```
## Setup DHCP on Ethernet port to connecte with Philips Hue bridge
- Assign a static IP address to the Ethernet port (eth0)
```
sudo nano /etc/dhcpcd.conf
```
Uncomment the following lines at the bottom of the document:
```
interface eth0
static ip_address=192.168.4.100/24
static domain_name_servers= ....
```
Then reboot the Raspberry Pi using:
```
sudo reboot
```
Check that the IP address of eth0 has been changed to 198.162.4.100 using:
```
ifconfig eth0|grep ‘inet ‘
```
## Install the DHCP daemon (isc-dhcp-server)
```
sudo apt-get update
sudo apt-get install isc-dhcp-server
sudo nano /etc/dhcp/dhcpd.conf
```
At the bottom of the file that opens, write the following lines:
```
option subnet-mask 255.255.255.0;
option routers 192.168.4.100;
subnet 192.168.4.0 netmask 255.255.255.0 {
	range 192.168.4.50 192.168.4.99;
}
```
Then : 
```
sudo nano /etc/defaults/isc-dhcp-server
```
In the file that opens, uncomment the following lines and add eth0 on the last one:
```
DHCPD_CONF=/etc/dhcp/dhcpd.conf
DHCPD_PID=/var/run/dhcpd.pid
INTERFACES="eth0"
```

# Companion App installation

## Requirements

The app requires an Android device version 5.0 (Lollipop) or higher with a functioning bluetooth connectivity.

## Installation

The app isn't available on the Google Play Store yet. Simply download the apk from our [website](https://alisonproject.ml) and that's it !   You're now ready to use the Alison System !

# Using the app to record sounds 

With the Raspberry Pi set-up and connected, get into the companion app and start recording sounds that you want to recognize, and associating a color with each sound.   
  
The system is now fully operational ! It will detect sounds in real time, and you can add or remove a given sound any time using the app.  
  
 
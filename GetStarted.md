# Get Started
Follow all these steps in order to set up your raspberry pi so it can run the needed programs. Make sure you have the latest build of Rasbian.

## Installing the Respeaker 4-Mic
- Get the seeed voice card source code
```
sudo apt-get update
sudo apt-get upgrade
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
##Setup DHCP on Ethernet port to connecte with Philips Hue bridge
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

# CONFIGURATION NECESSAIRE

## Mettre à jour le service bluetooth bluez à la version 5.50


+ Paquets à installer avant la mise à jour de Bluez
```
sudo apt-get update
sudo apt-get install libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev -y
```

+ Télécharger, compiler et installer bluez v5.50

```
wget  www.kernel.org/pub/linux/bluetooth/bluez-5.50.tar.xz
tar xvf bluez-5.50.tar.xz && cd bluez-5.50
./configure --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var --enable-experimental 
make -j4
sudo make install
sudo reboot
```


## Installer PyBluez via pip
+ paquets utlisés par pip pour compiler pybluez

```
sudo apt-get install libbluetooth-dev
sudo apt-get install  python-dev
```

+ Installer pybluez
```
sudo pip install pybluez
```

## Si le serveur vous affiche une erreur disant **No such file or directory** 
Il faudra faire quelques modifications afin d'activer la communication SPP sur la raspberry Pi ([source](https://www.raspberrypi.org/forums/viewtopic.php?t=133263&p=887944))
+ Modifier le fichier 
` /lib/systemd/system/bluetooth.service` en tant qu'administrateur et rajouter ` -C` à la fin de la ligne `ExecStart=/usr/lib/bluetooth/bluetoothd`

+ Ensuite redémarrer et activer SPP
```
sudo reboot
sudo sdptool add SP
```
## Lancer le serveur

`sudo python server.py`
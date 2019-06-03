from phue import Bridge
import time
import netifaces as ni

TIME_OUT = 5


def turn_on_alert(led_num, alert_type):  #Turns on an alert

    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    b = Bridge('192.168.4.50')
    b.connect()
    b.get_api()

    b.set_light(led_num, 'on', True)
    b.set_light(led_num, 'bri', 150)

    if (alert_type == 1):  #turns on led as bright as possible
        #b.set_light(led_num,'bri',254)
        b.set_light(led_num, 'hue', 0)
        time.sleep(TIME_OUT)
    elif (alert_type == 2):  #turns on a led but less brightly
        b.set_light(led_num, 'hue', 25500)
        time.sleep(TIME_OUT)
    elif (alert_type == 3):  #slow blink
        b.set_light(led_num, 'hue', 46920)
        time.sleep(TIME_OUT)
        #while(time.time()<timeout):
        #        b.set_light(led_num,'on',False)
        #        time.sleep(1.5)
        #        b.set_light(led_num,'on',True)
        #        time.sleep(1.5)
    elif (alert_type == 4):
        b.set_light(led_num, 'hue', 10000)
        time.sleep(TIME_OUT)
        #while(time.time()<timeout):                     #fast blink
        #       b.set_light(led_num,'on',False)
        #      time.sleep(0.5)
        #     b.set_light(led_num,'on',True)
        #    time.sleep(0.5)

    b.set_light(led_num, 'on', False)


def turn_off_led(led_num):
    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    b = Bridge('192.168.4.50')
    b.connect()
    b.get_api()

    b.set_light(led_num, 'on', False)


def turn_on_led(led_num):
    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    b = Bridge('192.168.4.50')
    b.connect()
    b.get_api()

    b.set_light(led_num, 'on', True)

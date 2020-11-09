import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import time
import datetime
from tqdm import tqdm
import RPi.GPIO as GPIO


# ポート番号の定義
Full_red_pin = 11
Full_blue_pin = 12
Full_green_pin = 13

red_pin = 17


# GPIOの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(Full_red_pin, GPIO.OUT)
GPIO.setup(Full_blue_pin, GPIO.OUT)
GPIO.setup(Full_green_pin, GPIO.OUT)

GPIO.setup(red_pin, GPIO.OUT)

# pwmモード？に設定する
full_red_led = GPIO.PWM(Full_red_pin, 100)
full_blue_led = GPIO.PWM(Full_blue_pin, 100)
full_green_led = GPIO.PWM(Full_green_pin, 100)

red_led = GPIO.PWM(red_pin, 100)

full_color_led = (full_red_led, full_blue_led, full_green_led)

# start
for led in full_color_led:
    led.start(0)

red_led.start(0)

try:
    while True:
        for led in full_color_led:
            for dc in range(0, 100, 5):
                led.ChangeDutyCycle(dc)
                time.sleep(0.05)
                # led.ChangeDutyCycle(0)
                # time.sleep(0.05)
        for led in full_color_led[::-1]:
            for dc in range(100, 0, -5):
                led.ChangeDutyCycle(dc)
                time.sleep(0.05)
                # led.ChangeDutyCycle(0)
                # time.sleep(0.05)
except KeyboardInterrupt:
    full_red_led.stop()
    full_blue_led.stop()
    full_green_led.stop()
    red_led.stop()
    GPIO.cleanup()
    sys.exit()

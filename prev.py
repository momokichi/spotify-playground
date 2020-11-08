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

# set your info
client_id = ""
client_secret = ""
redirect_uri = ""
scope = ""
username = ""


auth_manager = SpotifyOAuth(
    client_id, client_secret, redirect_uri, scope=scope, username=username
)
sp = spotipy.Spotify(auth_manager=auth_manager)

song_name = ""
artist_name = ""
is_playing = "paused"
progress_ms = 0
duration_ms = 0
id = ""

try:
    while True:
        result = sp.currently_playing("JP")

        song_name = result["item"]["name"]
        artist_name = result["item"]["album"]["artists"][0]["name"]
        is_playing = "playing" if result["is_playing"] else "paused"
        progress_ms = result["progress_ms"]
        duration_ms = result["item"]["duration_ms"]

        id = result["item"]["id"]
        features = sp.audio_features(id)

        print(song_name, "by", artist_name)
        print("state: ", is_playing)
        print(progress_ms, "/", duration_ms, "ms")
        print(features[0]["tempo"])
        print()

        if is_playing == "playing":
            GPIO.output(red_pin, GPIO.HIGH)
        else:
            GPIO.output(red_pin, GPIO.LOW)

        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()

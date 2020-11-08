import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import time
import datetime
import RPi.GPIO as GPIO
import threading
import config


class LedService:
    # ポート番号の定義
    Full_red_pin = 11
    Full_blue_pin = 12
    Full_green_pin = 13

    red_pin = 17

    def __init__(self):
        # GPIOの設定
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Full_red_pin, GPIO.OUT)
        GPIO.setup(self.Full_blue_pin, GPIO.OUT)
        GPIO.setup(self.Full_green_pin, GPIO.OUT)

        GPIO.setup(self.red_pin, GPIO.OUT)

    def switch_red_led(self, is_turnon):
        if is_turnon:
            GPIO.output(self.red_pin, GPIO.HIGH)
        else:
            GPIO.output(self.red_pin, GPIO.LOW)

    def blinking_led(self):
        while True:
            self.switch_red_led(True)
            time.sleep(0.5)
            self.switch_red_led(False)
            time.sleep(0.5)

    # 終了時にはこれを呼び出す
    def cleanup(self):
        GPIO.cleanup()


class Client:
    # set scope
    scope = "user-read-currently-playing"

    song_name = ""
    artist_name = ""
    is_playing = "paused"
    progress_ms = 0
    duration_ms = 0
    id = ""

    def __init__(self):
        auth_manager = SpotifyOAuth(
            config.CLIENT_ID,
            config.CLIENT_SECRET,
            config.REDIRECT_URI,
            scope=self.scope,
            username=config.USERNAME,
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_currently_playing(self):
        return self.sp.currently_playing("JP")

    def fetch_worker(self):
        while True:
            result = self.sp.currently_playing("JP")
            self.song_name = result["item"]["name"]
            self.artist_name = result["item"]["album"]["artists"][0]["name"]
            self.is_playing = "playing" if result["is_playing"] else "paused"
            self.progress_ms = result["progress_ms"]
            self.duration_ms = result["item"]["duration_ms"]
            time.sleep(3)

    def get_audio_features(self, id):
        return self.sp.audio_features(id)

    def print_info(self):
        print(datetime.datetime.now())
        print(self.song_name, "by", self.artist_name)
        print("state: ", self.is_playing)
        print(self.progress_ms, "/", self.duration_ms, "ms")
        print()

    def print_worker(self):
        while True:
            self.print_info()
            time.sleep(3)


if __name__ == "__main__":
    client = Client()
    ledService = LedService()

    # データの取得とプリントはスレッドへ
    t1 = threading.Thread(target=client.fetch_worker)
    t2 = threading.Thread(target=client.print_worker)

    # デーモンにする
    # メインスレッドが終了したときに自動で止まってくれます
    t1.setDaemon(True)
    t2.setDaemon(True)

    t1.start()
    t2.start()

    try:
        # ledを点滅させる
        ledService.blinking_led()
    except KeyboardInterrupt:
        # ctrl+c でcleanupして終了
        ledService.cleanup()
        print("interrupted!")
        sys.exit()

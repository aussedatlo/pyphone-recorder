#!/usr/bin/env python3
import signal
import sys
import RPi.GPIO as GPIO
import alsaaudio as audio
import wave

BUTTON_GPIO = 3

JINGLE_FILE = "../audio/messagebip.wav"

AUDIO_FRAMERATE = 44100
AUDIO_OUTPUT_DEVICE = "hw:0,0"
AUDIO_INPUT_DEVICE = "hw:1,0"
AUDIO_FORMAT = audio.PCM_FORMAT_S16_LE
AUDIO_PERIOD_SIZE = 160


def play_jingle():
    print("play_jingle start")
    f = wave.open(JINGLE_FILE)
    message_bip_bytes = f.readframes(f.getnframes())

    out = audio.PCM(audio.PCM_PLAYBACK, device=AUDIO_OUTPUT_DEVICE, channels=2,
                    rate=AUDIO_FRAMERATE, format=AUDIO_FORMAT, periodsize=AUDIO_PERIOD_SIZE)

    i = 0
    while (i + AUDIO_PERIOD_SIZE < len(message_bip_bytes)) and (not GPIO.input(BUTTON_GPIO)):
        out.write(message_bip_bytes[i:i + AUDIO_PERIOD_SIZE])
        i = i + AUDIO_PERIOD_SIZE
    print("play_jingle stop")

    return not (i + AUDIO_PERIOD_SIZE < len(message_bip_bytes))


def record():
    print("record start")
    print("record stop")


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def gpio_evt_callback(channel):
    print("gpio_evt_callback!")
    ret = play_jingle()

    if ret:
        record()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.BOTH,
                          callback=gpio_evt_callback, bouncetime=100)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

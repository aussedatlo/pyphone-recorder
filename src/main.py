#!/usr/bin/env python3
import signal
import sys
import RPi.GPIO as GPIO


BUTTON_GPIO = 3


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def falling_callback(channel):
    print("falling_callback!")


def rising_callback(channel):
    print("rising_callback!")


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING,
                          callback=rising_callback, bouncetime=100)

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING,
                          callback=falling_callback, bouncetime=100)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

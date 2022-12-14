#!/usr/bin/env python3
import sys
import click
from pyphone_recorder import phone_recorder as PR

BUTTON_GPIO = 3

JINGLE1 = "/home/pi/jingle1.wav"
JINGLE2 = "/home/pi/jingle2.wav"

AUDIO_OUTPUT_DEVICE = "hw:4,0"
OUTPUT_PATH = "/home/pi/record/"


@click.command()
@click.option("--audio-output-device", default=AUDIO_OUTPUT_DEVICE,
              help="audio output device in alsa format.")
@click.option("--jingle1", default=JINGLE1, help="jingle before recording.")
@click.option("--jingle2", default=JINGLE2, help="jingle after recording.")
@click.option("--gpio", default=BUTTON_GPIO, help="gpio button to know when to play or stop")
@click.option("--output-path", default=OUTPUT_PATH, help="output path to save records.")
def run(
        audio_output_device,
        jingle1, jingle2, gpio, output_path):
    pr = PR.PhoneRecorder(audio_output_device,
                          jingle1, jingle2, gpio, output_path)
    pr.run()


if __name__ == "__main__":
    run(sys.argv)

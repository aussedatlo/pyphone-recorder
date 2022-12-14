#!/usr/bin/env python3
import sys
import click
from pyphone_recorder import phone_recorder as PR

BUTTON_GPIO = 3

AUDIO_OUTPUT_DEVICE = "hw:4,0"


@click.command()
@click.option("--audio-output-device", default=AUDIO_OUTPUT_DEVICE,
              help="audio output device in alsa format.")
@click.option("--jingle1", default="jingle1.wav", help="jingle 1.")
@click.option("--jingle2", default="jingle2.wav", help="jingle 2.")
@click.option("--gpio", default=BUTTON_GPIO, help="gpio")
def run(
        audio_output_device,
        jingle1, jingle2, gpio):
    pr = PR.PhoneRecorder(audio_output_device,
                          jingle1, jingle2, gpio)
    pr.run()


if __name__ == "__main__":
    run(sys.argv)

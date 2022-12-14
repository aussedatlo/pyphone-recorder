#!/usr/bin/env python3
import sys
import click
from phone_recorder import PhoneRecorder as PR

BUTTON_GPIO = 3

JINGLE_FILE = "../audio/messagebip.wav"

AUDIO_OUTPUT_DEVICE = "hw:0,0"


@click.command()
@click.option("--audio-output-device", default=AUDIO_OUTPUT_DEVICE,
              help="audio output device in alsa format.")
@click.option("--jingle", default=JINGLE_FILE, help="audio period size.")
@click.option("--gpio", default=BUTTON_GPIO, help="gpio")
def run(
        audio_output_device,
        jingle, gpio):
    pr = PR(audio_output_device,
            jingle, gpio)
    # pr.run()
    pr.record()


def exec_command_line(argv):
    run(argv)


if __name__ == "__main__":
    run(sys.argv)
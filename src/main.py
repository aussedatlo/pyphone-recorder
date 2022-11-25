#!/usr/bin/env python3
import click
from phone_recorder import PhoneRecorder as PR

BUTTON_GPIO = 3

JINGLE_FILE = "../audio/messagebip.wav"

AUDIO_OUTPUT_DEVICE = "hw:0,0"
AUDIO_INPUT_DEVICE = "hw:1,0"


@click.command()
@click.option("--audio-output-device", default=AUDIO_OUTPUT_DEVICE,
              help="audio output device in alsa format.")
@click.option("--audio-input-device", default=AUDIO_INPUT_DEVICE,
              help="audio input device in alsa format.")
@click.option("--jingle", default=JINGLE_FILE, help="audio period size.")
@click.option("--gpio", default=BUTTON_GPIO, help="gpio")
def run(
        audio_output_device, audio_input_device,
        jingle, gpio):
    pr = PR(audio_output_device, audio_input_device,
            jingle, gpio)
    pr.run()


if __name__ == '__main__':
    run()

import signal
import sys
import RPi.GPIO as GPIO
import alsaaudio as audio
import wave

AUDIO_FRAMERATE = 44100
AUDIO_FORMAT = audio.PCM_FORMAT_S16_LE
AUDIO_PERIOD_SIZE = 160


class PhoneRecorder:
    def __init__(self,
                 audio_output_device, audio_input_device,
                 jingle, gpio):
        """constructor"""
        self.audio_output_device = audio_output_device
        self.audio_input_device = audio_input_device
        self.jingle = jingle
        self.gpio = gpio

    def run(self):
        """start the process and listen to event on gpio"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.gpio, GPIO.FALLING,
                              callback=self.gpio_evt_callback, bouncetime=500)

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()

    def play_jingle(self):
        """play jingle, stop if gpio status change"""
        print("play_jingle start")
        f = wave.open(self.jingle)
        message_bip_bytes = f.readframes(f.getnframes())

        out = audio.PCM(
            audio.PCM_PLAYBACK, device=self.audio_output_device, channels=2,
            rate=AUDIO_FRAMERATE, format=AUDIO_FORMAT,
            periodsize=AUDIO_PERIOD_SIZE)

        i = 0
        while (i + AUDIO_PERIOD_SIZE < len(message_bip_bytes)) and (not GPIO.input(self.gpio)):
            out.write(message_bip_bytes[i:i + AUDIO_PERIOD_SIZE])
            i = i + AUDIO_PERIOD_SIZE
        print("play_jingle stop")

        return not (i + AUDIO_PERIOD_SIZE < len(message_bip_bytes))

    def record(self):
        """record audio, stop if gpio status change"""
        print("record start")
        print("record stop")

    def signal_handler(self, sig, frame):
        """cleanup gpio state on signal"""
        GPIO.cleanup()
        sys.exit(0)

    def gpio_evt_callback(self, channel):
        """callback used when gpio state change"""
        print("gpio_evt_callback!")
        ret = self.play_jingle()

        if ret:
            self.record()

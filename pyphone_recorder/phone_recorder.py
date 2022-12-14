import signal
import sys
# import RPi.GPIO as GPIO
import alsaaudio as audio
import wave
from yaspin import yaspin
import pyaudio
import time

AUDIO_FRAMERATE = 44100
AUDIO_FORMAT = audio.PCM_FORMAT_S16_LE
AUDIO_PERIOD_SIZE = 160
RECORD_SECONDS = 120


class PhoneRecorder:
    def __init__(self, audio_output_device, jingle1, jingle2, gpio):
        """constructor"""
        self.audio_output_device = audio_output_device
        self.jingle1 = jingle1
        self.jingle2 = jingle2
        self.gpio = gpio

        self.audio = pyaudio.PyAudio()

    def run(self):
        """start the process and listen to event on gpio"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.gpio, GPIO.FALLING,
                              callback=self.gpio_evt_callback, bouncetime=500)

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()

    def play_jingle(self, jingle):
        """play jingle, stop if gpio status change"""
        with yaspin(text="Playing jingle", color="cyan") as sp:
            f = wave.open(jingle)
            message_bip_bytes = f.readframes(f.getnframes())

            out = audio.PCM(
                audio.PCM_PLAYBACK, device=self.audio_output_device, channels=2,
                rate=AUDIO_FRAMERATE, format=AUDIO_FORMAT,
                periodsize=AUDIO_PERIOD_SIZE)

            i = 0
            while (i + AUDIO_PERIOD_SIZE < len(message_bip_bytes)) and (not GPIO.input(self.gpio)):
                out.write(message_bip_bytes[i:i + AUDIO_PERIOD_SIZE])
                i = i + AUDIO_PERIOD_SIZE

            finished = not (i + AUDIO_PERIOD_SIZE < len(message_bip_bytes))
            if (finished):
                sp.write("> done")
                sp.ok("✔")
            else:
                sp.write("> cancelled")
                sp.ok("✕")

            return finished

    def record(self):
        """record audio, stop if gpio status change"""
        with yaspin(text="Recording", color="cyan") as sp:
            ret = True
            inp = self.audio.open(
                format=pyaudio.paInt16, channels=1, rate=AUDIO_FRAMERATE,
                input=True, frames_per_buffer=AUDIO_PERIOD_SIZE)

            frames = []
            for i in range(
                    0, int(AUDIO_FRAMERATE / AUDIO_PERIOD_SIZE * RECORD_SECONDS)):
                if (not GPIO.input(self.gpio)):
                    ret = False
                    break
                data = inp.read(AUDIO_PERIOD_SIZE)
                frames.append(data)

            inp.stop_stream()
            inp.close()

            f = wave.open('record-{}.wav'.format(time.time()), 'wb')
            f.setnchannels(1)
            f.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            f.setframerate(AUDIO_FRAMERATE)
            f.writeframes(b''.join(frames))
            f.close()
            sp.write("> done")
            sp.ok("✔")
            return ret

    def signal_handler(self, sig, frame):
        """cleanup gpio state on signal"""
        GPIO.cleanup()
        sys.exit(0)

    def gpio_evt_callback(self, channel):
        """callback used when gpio state change"""
        ret = self.play_jingle(self.jingle1)

        if ret:
            ret = self.record()

        if ret:
            self.play_jingle(self.jingle2)

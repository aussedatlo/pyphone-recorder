#!/usr/bin/env python3
import alsaaudio as audio
import wave

# arecord -D hw:2,0 -r 44100 recording.wav
# sox recording.wav -c 2 recording_2channel.wav
# aplay -D hw:2,0 recording_2channel.wav

message_bip = "./messagebip.wav"

audioframerate = 44100
audiodevice = "hw:4,0"
hwdevice = "hw:1,0"
audioformat = audio.PCM_FORMAT_S16_LE
audioperiodsize = 160


class PhoneRecording:
    def __init__(self):
        # Check that message_bip file exists
        f = wave.open(message_bip)
        self.message_bip_bytes = f.readframes(f.getnframes())

        # Create recorded folder if it doesn't exists
        self.state = "STOP"

        self.inp = audio.PCM(audio.PCM_CAPTURE, device=hwdevice)
        self.inp.setrate(audioframerate)
        self.inp.setformat(audioformat)

        self.out = audio.PCM(audio.PCM_PLAYBACK, device=audiodevice)
        self.out.setchannels(2)
        self.out.setrate(audioframerate)
        self.out.setformat(audioformat)
        self.out.setperiodsize(audioperiodsize)

    def start(self):
        self.state = "STARTING"

        i = 0
        while i + audioperiodsize < len(self.message_bip_bytes):
            self.out.write(self.message_bip_bytes[i:i + audioperiodsize])
            i = i + audioperiodsize

        self.state = "START"
        # Record

    def stop(self):
        self.state = "STOPING"
        # stop recording
        # save file in recorded folder
        self.state = "STOP"


phone = PhoneRecording()
phone.start()

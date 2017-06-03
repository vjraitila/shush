"""A dogsitter in Python"""
import sys
import sounddevice as sd
import soundfile as sf
import numpy as np
import logging as log
import os
import random

THRESHOLD = 0.2
CHUNK_SIZE = 1024
RATE = 16000

def terminal_width():
    """Determines the current width in the terminal."""
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w

def show_indicator(lvl):
    """Displays a sound level indicator."""
    width = terminal_width() - 2
    bar = int(lvl * width)
    res = width - bar
    sys.stdout.write('\r[' + '#' * bar + ' ' * res + ']')
    sys.stdout.flush()

def is_silent(lvl):
    """Determine whether there is a sound."""
    return lvl < THRESHOLD

def shush():
    """Play a random sound from recordings."""
    # print('SHUSH')
    sounds = os.listdir('sounds')
    if len(sounds) > 0:
        rnd_sound = 'sounds/' + random.choice(sounds)
        log.info('Playing {}'.format(rnd_sound))
        data, fs = sf.read(rnd_sound, dtype='float32')
        sd.play(data, fs)
        sd.wait()
    else:
        log.warn('Sounds directory is empty - nothing to play')

def start_listening():
    """Monitor for sounds exceeding a threshold."""
    log.info('Started listening...')

    heard_something = False
    last_noise = 0.0

    while True:
        snd_data = sd.rec(CHUNK_SIZE, samplerate=RATE, channels=1, blocking=True)
        rms = np.sqrt(np.mean(snd_data**2))

        show_indicator(rms)

        if not is_silent(rms):
            heard_something = True
            last_noise = rms

        if heard_something and is_silent(rms):
            log.info('Heard a sound {}/{}'.format(last_noise, THRESHOLD))
            shush()
            heard_something = False

if __name__ == '__main__':
    log.basicConfig(filename='events.log', level=log.INFO, format='%(asctime)s %(message)s')
    start_listening()

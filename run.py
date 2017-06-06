"""A dogsitter in Python"""
import os
import random
import time
import signal
import logging as log
import numpy as np
import sounddevice as sd
import soundfile as sf

THRESHOLD = 0.06
CHUNK_SIZE = 1024
RATE = 16000

def is_silent(lvl):
    """Determine whether there is a sound."""
    return lvl < THRESHOLD

def play_sound(filename):
    """Play a sound using the default sound device."""
    log.info('Playing %s', filename)
    data, samplerate = sf.read('sounds/' + filename, dtype='float32')
    sd.play(data, samplerate)
    sd.wait()

def shush():
    """Play a random sound from recordings."""
    sounds = filter(lambda f: f.startswith('shush'), os.listdir('sounds'))
    if sounds:
        rnd_sound = random.choice(sounds)
        play_sound(rnd_sound)
    else:
        log.warn('Sounds directory is empty - nothing to play')

def handler_stop_signals(signum, frame):
    global run
    run = False

run = True

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

if __name__ == '__main__':
    log.basicConfig(filename='history.log', level=log.INFO, format='%(asctime)s %(message)s')
    log.info('Started listening')
    play_sound('welcome.wav')

    noise_started = 0

    while run:
        snd_data = sd.rec(CHUNK_SIZE, samplerate=RATE, channels=1, blocking=True)
        rms = np.sqrt(np.mean(snd_data**2))

        if not noise_started and not is_silent(rms):
            noise_started = time.time()
            log.info('Noise started (rms: %.3f, threshold: %.3f)', rms, THRESHOLD)

        if noise_started > 0 and is_silent(rms):
            log.info('Noise stopped (duration: %.3fs)', time.time() - noise_started)
            # print('shush()')
            shush()
            noise_started = 0

    play_sound('goodbye.wav')
    log.info('Stopped listening')


"""A dogsitter in Python"""
import os
import random
import time
import logging as log
import numpy as np
import sounddevice as sd
import soundfile as sf

THRESHOLD = 0.1
CHUNK_SIZE = 1024
RATE = 16000

def is_silent(lvl):
    """Determine whether there is a sound."""
    return lvl < THRESHOLD

def shush():
    """Play a random sound from recordings."""
    sounds = os.listdir('sounds')
    if sounds:
        rnd_sound = 'sounds/' + random.choice(sounds)
        log.info('Playing %s', rnd_sound)
        data, samplerate = sf.read(rnd_sound, dtype='float32')
        sd.play(data, samplerate)
        sd.wait()
    else:
        log.warn('Sounds directory is empty - nothing to play')

def start_listening():
    """Monitor for sounds exceeding a threshold."""
    log.info('Started listening...')

    noise_started = 0

    while True:
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

if __name__ == '__main__':
    log.basicConfig(filename='shush_events.log', level=log.INFO, format='%(asctime)s %(message)s')
    start_listening()

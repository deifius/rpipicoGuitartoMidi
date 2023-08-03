#!/usr/bin/env python3

from machine import Pin, ADC, Timer
from ulab import numpy as np
from midi_methods import *

# Constants for Audio Sampling
TARGET_FREQUENCY = 2093.12  # Nyquist frequency for a sample rate of 4186.24 Hz
SAMPLE_RATE = 4186.24  # Hz
WINDOW_SIZE = 64
ADC_PIN = 26

# Initialize ADC
adc = ADC(Pin(ADC_PIN))

# Global variable to track the current note
current_note = None

# Circular buffer for samples
samples = [0] * WINDOW_SIZE
index = 0

def read_adc() -> int:
    """Reads a value from the ADC."""
    return adc.read_u16()

def frequency_to_midi(frequency: float) -> (int, float):
    """Maps a frequency to a corresponding MIDI note number and calculates the difference for pitch bend."""
    midi_note_number = 69 + 12 * np.log2(frequency / 440.0)
    rounded_midi_note = int(round(midi_note_number))
    difference = midi_note_number - rounded_midi_note
    return rounded_midi_note, difference

def calculate_pitch_bend(difference: float) -> int:
    """Calculates the MIDI pitch bend value."""
    return int(difference * 4096) + 4096  # Assuming a pitch bend range of +/- 1 semitone

def analyze_pitch_and_send_midi():
    """Analyzes pitch using FFT and sends corresponding MIDI messages."""
    global current_note

    # Perform FFT
    fft_result = np.fft.fft(samples)
    
    # Calculate magnitude and find the peak
    magnitude = np.abs(fft_result)
    peak_index = np.argmax(magnitude)
    peak_frequency = peak_index * SAMPLE_RATE / WINDOW_SIZE

    # Map frequency to MIDI note and calculate the difference
    midi_note_number, difference = frequency_to_midi(peak_frequency)
    pitch_bend_value = calculate_pitch_bend(difference)

    # Additional code to handle MIDI messages
    # ...

def sample_timer(t):
    global index
    samples[index] = read_adc()
    index = (index + 1) % WINDOW_SIZE

# Set up a timer to call sample_timer at the sample rate
timer = Timer(freq=SAMPLE_RATE)
timer.init(period=1000000 // SAMPLE_RATE, mode=Timer.PERIODIC, callback=sample_timer)

# Main loop
while True:
    analyze_pitch_and_send_midi()
    # ...

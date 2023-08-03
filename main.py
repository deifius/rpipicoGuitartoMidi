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
    """Maps a frequency to a corresponding MIDI note number.
    
    Args:
        frequency (float): The frequency to be mapped.

    Returns:
        int: Corresponding MIDI note number, float: difference in cents from the midi int
    """
    midi_note_number = 69 + 12 * np.log2(frequency / 440.0)
    rounded_midi_note = int(round(midi_note_number))
    difference = midi_note_number - rounded_midi_note
    return rounded_midi_note, difference

def calculate_pitch_bend(difference: float) -> int:
    """Calculates the MIDI pitch bend value for a given frequency and MIDI note.
    
    Args:
        difference (between -1:1, actual pitch distance from midi int)

    Returns:
        int: Pitch bend value (0-16383).
    """
    return int(difference * 4096) + 4096  # Assuming a pitch bend range of +/- 1 semitone

def calculate_relative_spl(magnitude: np.array) -> float:
    """Calculates the relative Sound Pressure Level (SPL) from an FFT magnitude spectrum.
    
    Args:
        magnitude (np.array): Magnitude spectrum from FFT.

    Returns:
        float: Relative SPL value.
    """
    # Implementation depends on specific requirements
    return magnitude.max()

def calculate_velocity(relative_spl: float) -> int:
    """Calculates the MIDI velocity based on relative SPL.
    
    Args:
        relative_spl (float): Relative SPL value.

    Returns:
        int: Corresponding MIDI velocity (0-127).
    """
    velocity = int(relative_spl * 127)
    return min(max(velocity, 0), 127)
    
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

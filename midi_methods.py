#!/usr/bin/en python3

"""
MIDI Methods for Raspberry Pi Pico

This module provides functions to send MIDI messages from the Raspberry Pi Pico via UART. It includes functions to send Note On, Note Off, Pitch Bend, and Aftertouch messages, allowing for expressive control over connected MIDI devices or software.

Functions:
    send_midi_note(note: int, velocity: int = VELOCITY) -> None
        Sends a MIDI Note On message for the specified note and velocity.

    send_midi_note_off(note: int, velocity: int = 0) -> None
        Sends a MIDI Note Off message for the specified note.

    send_midi_pitch_bend(bend_value: int) -> None
        Sends a MIDI Pitch Bend message with the specified bend value.

    send_midi_aftertouch(pressure: int) -> None
        Sends a MIDI Aftertouch (Channel Pressure) message with the specified pressure value.

Constants:
    NOTE_ON, NOTE_OFF, PITCH_BEND, AFTERTOUCH: MIDI command bytes for different message types.
    CHANNEL: MIDI channel to use (0-15).
    VELOCITY: Default velocity for Note On messages.
    MIDI_BAUD_RATE: Baud rate for MIDI communication over UART (31250).

Example:
    from midi_methods import send_midi_note

    # Send a Note On message for Middle C (MIDI note 60) with velocity 64
    send_midi_note(60)

Note:
    Ensure that the UART pins on the Raspberry Pi Pico are correctly connected to the MIDI interface, and that the connected MIDI device is configured to use the same channel as specified in this module.
"""


from machine import UART

# Constants for MIDI
NOTE_ON = 0x90
NOTE_OFF = 0x80
PITCH_BEND = 0xE0
AFTERTOUCH = 0xD0
CHANNEL = 0
VELOCITY = 64
MIDI_BAUD_RATE = 31250

# Initialize UART
uart = UART(0, baudrate=MIDI_BAUD_RATE)

def send_midi_note(note: int, velocity: int = VELOCITY) -> None:
    """Sends a MIDI Note On message."""
    command = NOTE_ON | CHANNEL
    uart.write(bytes([command, note, velocity]))

def send_midi_note_off(note: int, velocity: int = 0) -> None:
    """Sends a MIDI Note Off message."""
    command = NOTE_OFF | CHANNEL
    uart.write(bytes([command, note, velocity]))

def send_midi_pitch_bend(bend_value: int) -> None:
    """Sends a MIDI Pitch Bend message."""
    command = PITCH_BEND | CHANNEL
    bend_bytes = divmod(bend_value & 0x3FFF, 128)  # 14-bit value, split into two 7-bit bytes
    uart.write(bytes([command, bend_bytes[1], bend_bytes[0]]))

def send_midi_aftertouch(pressure: int) -> None:
    """Sends a MIDI Aftertouch message."""
    command = AFTERTOUCH | CHANNEL
    uart.write(bytes([command, pressure]))

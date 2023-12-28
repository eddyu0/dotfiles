#!/usr/bin/python3
# -*- coding: utf-8 -*-

# taken from Aurélien Cibrario https://askubuntu.com/a/717658

"""
Sort of mini driver.
Read a specific InputDevice (logitech_g403_hero),
monitoring for special thumb button
Use uinput (virtual driver) to create a mini keyboard
Send ctrl keystroke on that keyboard
"""

import uinput
from evdev import InputDevice  # , categorize, ecodes

# Initialize keyboard, choosing used keys
ctrl_keyboard = uinput.Device(
    [
        uinput.KEY_KEYBOARD,
        uinput.KEY_LEFTCTRL,
        uinput.KEY_F4,
    ]
)
shift_keyboard = uinput.Device([uinput.KEY_KEYBOARD, uinput.KEY_LEFTSHIFT])

# Sort of initialization click (not sure if mandatory)
# ( "I'm-a-keyboard key" )
ctrl_keyboard.emit_click(uinput.KEY_KEYBOARD)
shift_keyboard.emit_click(uinput.KEY_KEYBOARD)

# Useful to list input devices
# for i in range(0, 15):
#     dev = InputDevice("/dev/input/event{}".format(i))
#     print(dev)

# Declare device patch.
# I made a udev rule to assure it's always the same name
dev = InputDevice("/dev/logitech_g403_hero")
# print(dev)
ctrl_key_on = False
shift_key_on = False

# Infinite monitoring loop
for event in dev.read_loop():
    # My thumb button code (use "print(event)" to find)
    # forward: 276
    # backward: 275
    if event.code == 276:
        # Button status, 1 is down, 0 is up
        if event.value == 1:
            ctrl_keyboard.emit(uinput.KEY_LEFTCTRL, 1)
            ctrl_key_on = True
        elif event.value == 0:
            ctrl_keyboard.emit(uinput.KEY_LEFTCTRL, 0)
            ctrl_key_on = False
    elif event.code == 275:
        # Button status, 1 is down, 0 is up
        if event.value == 1:
            shift_keyboard.emit(uinput.KEY_LEFTSHIFT, 1)
            shift_key_on = True
        elif event.value == 0:
            shift_keyboard.emit(uinput.KEY_LEFTSHIFT, 0)
            shift_key_on = False

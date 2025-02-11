import asyncio
import board
import digitalio
import random
import usb_hid
import busio

from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Onboard LED on Raspberry PI Pico 
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# GPIO #28. Pin #34. Refer: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#pico-1-technical-specification
b1 = digitalio.DigitalInOut(board.GP28)
b1.direction = digitalio.Direction.INPUT
b1.pull = digitalio.Pull.UP
b1_toggle_enabled = False

# GPIO #27. Pin #32. Refer: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#pico-1-technical-specification
b2 = digitalio.DigitalInOut(board.GP27)
b2.direction = digitalio.Direction.INPUT
b2.pull = digitalio.Pull.UP
b2_toggle_enabled = False

# GPIO #16. Pin #21. Refer: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#pico-1-technical-specification
b3 = digitalio.DigitalInOut(board.GP16)
b3.direction = digitalio.Direction.INPUT
b3.pull = digitalio.Pull.UP
b3_toggle_enabled = False

# Init UART to receive data from another PICO W which receives data from BLE and send it to HID
# GPIO #08. Pin #11.
# GPIO #09. Pin #12.
uart = busio.UART(board.GP8, board.GP9, baudrate=9600)

# Initialize Keyboard HID
keyboard = Keyboard(usb_hid.devices)
keycodes = [
    Keycode.A, Keycode.B, Keycode.C, Keycode.D, Keycode.E,
    Keycode.F, Keycode.G, Keycode.H, Keycode.I, Keycode.J,
    Keycode.K, Keycode.L, Keycode.M, Keycode.N, Keycode.O,
    Keycode.P, Keycode.Q, Keycode.R, Keycode.S, Keycode.T,
    Keycode.U, Keycode.V, Keycode.W, Keycode.X, Keycode.Y,
    Keycode.Z, Keycode.SPACE, Keycode.ENTER, Keycode.BACKSPACE
]

# Keyboard layout.
layout = KeyboardLayoutUS(keyboard)

# Button 1 click function. Enables/Disables Random mouse movements.
async def exec_b1():
    global b1_toggle_enabled
    b1_toggle_enabled = not b1_toggle_enabled
    await blink_led()
    if b1_toggle_enabled:
        print("b1 toggle on")
        asyncio.create_task(mouse_move())
    else:
        print("b1 toggle off")
    await pause_while_pressed(b1)

# Button 2 click funtion. Enables/Disables Random key presses send to connected device    
async def exec_b2():
    global b2_toggle_enabled
    b2_toggle_enabled = not b2_toggle_enabled
    await blink_led()
    if b2_toggle_enabled:
        print("b2 toggle on")
        asyncio.create_task(keyboard_input())
    else:
        print("b2 toggle off")
    await pause_while_pressed(b2)

# Button 3 click funtion. Enables/Disables receiving data over UART from another PICO W    
async def exec_b3():
    global b3_toggle_enabled
    b3_toggle_enabled = not b3_toggle_enabled
    await blink_led()
    if b3_toggle_enabled:
        print("b3 toggle on")
        asyncio.create_task(uart_input())
    else:
        print("b3 toggle off")
    await pause_while_pressed(b3)

# Stops execution when button is pressed after registering for the first time    
async def pause_while_pressed(btn):
    while not btn.value:
        await asyncio.sleep(0.1)

# Blinks the onboard LED
async def blink_led():
    led.value = True
    await asyncio.sleep(0.05)
    led.value = False

# Random mouse movements
async def mouse_move():
    global b1_toggle_enabled
    mouse = Mouse(usb_hid.devices)
    start = 1
    stop = 50
    mid = 25
    while b1_toggle_enabled:
        dxn = random.randrange(start, stop)
        dyn = random.randrange(start, stop)
        dx = random.randrange(start, stop)
        dy = random.randrange(start, stop)
        if dxn < mid and dyn < mid:
            mouse.move(-dx, -dy)
        elif dxn > mid and dyn < mid:
            mouse.move(dx, -dy)
        elif dxn > mid and dyn > mid:
            mouse.move(dx, dy)
        elif dxn < mid and dyn > mid:
            mouse.move(-dx, dy)
        await asyncio.sleep(1)

# Random keyboard inputs        
async def keyboard_input():
    global b2_toggle_enabled
    global keyboard
    global keycodes
    while b2_toggle_enabled:
        random_keycode = random.choice(keycodes)  # Pick a random keycode
        keyboard.send(random_keycode)  # Send the selected keycode
        await asyncio.sleep(random.random())

# Process events received over UART from another PICO W which transmits data received from Bluetooth LE
# Currently supports only keyboard input
async def uart_input():
    global b3_toggle_enabled
    global uart
    global keyboard
    global keycodes
    global layout
    while b3_toggle_enabled:
        data = uart.read(128)
        if data is None:
            await asyncio.sleep(0.05)
            continue
        message = data.decode("utf-8")
        action = message.split(" ")[0]
        seq = message.split(" ")[1]
        if action.upper() == "KEYBOARD":
            layout.write(seq)
            
# Main event loop
async def main():
    while True:
        if not b1.value:
            await exec_b1()
        elif not b2.value:
            await exec_b2()
        elif not b3.value:
            await exec_b3()
        await asyncio.sleep(0.1)  # Allow other tasks to run

# Execute the event loop using asyncio
asyncio.run(main())


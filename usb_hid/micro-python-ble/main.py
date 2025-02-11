from machine import Pin, UART
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from ble_actions import BLEActions

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)
actions = BLEActions()

# Create a Pin object for the onboard LED, configure it as an output
led = Pin("LED", Pin.OUT)

# Initialize the LED state to 0 (off)
led_state = 0

# Initial UART for communicating with another pico running usb_hid
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# Define a callback function to handle received data
def on_rx(data):
    print("Data received: ", data)  # Print the received data
    global led_state  # Access the global variable led_state
    str = data.decode('utf-8').strip()
    if str == 'toggle':  # Check if the received data is "toggle"
        led.value(not led_state)  # Toggle the LED state (on/off)
        led_state = 1 - led_state  # Update the LED state
    else:
        action, seq = actions.process(str)
        if(action is None and seq is None):
            return
        uart1.write(action + " " + seq)
        print("wrote to uart1")

# Start an infinite loop
while True:
    if sp.is_connected():  # Check if a BLE connection is established
        sp.on_write(on_rx)  # Set the callback function for data reception
# PICO-H (Circuit Python) USB HID with Bluetooth inputs from another PICO-WH (Micro Python) (Optional)

## Hardware Required
1. USB A/C Male to Micro USB Male data cable
2. Raspberry Pi Pico H
3. Raspberry Pi Pico WH (Optional)
4. Breadboards
5. Jumper wires
6. 3 4-pin switch

## Circuit Diagram
![Circuit diagram](./images/USB_HID_BLE-schematic.svg)

## Setup
On Raspberry Pi Pico H flash the latest Circuit Python Firmware from [https://circuitpython.org/board/raspberry_pi_pico/](https://circuitpython.org/board/raspberry_pi_pico/)  
Once installed, follow these steps
1. Copy the [./circuit-python-hid/boot.py](./circuit-python-hid/boot.py) to the root of your pico. The filename should be boot.py
2. Copy the [./circuit-python-hid/code.py](./circuit-python-hid/code.py) to the root of your pico. The filename should be code.py
3. Copy over entire directory [./circuit-python-hid/lib/](./circuit-python-hid/lib/) to the root of your pico. The directory name should be lib

On Raspberry Pi Pico WH flash the latest Micro Python Firmware from [https://micropython.org/download/RPI_PICO_W/](https://micropython.org/download/RPI_PICO_W/)  
Once installed, follow these steps
1. Copy all the files from [./micro-python-ble/](./micro-python-ble/) to the root of your pico.

> **Why does the Picos have different firmwares?**
>
> While technically this can be achieved with a single firmware, there are couple of things to consider.
> 
> 1. This is to learn about communication between two microcontrollers via UART
> 2. Circuit Python firmware for Pico W/WH does not support Bluetooth yet. Refer issue: [https://github.com/adafruit/circuitpython/issues/7693](https://github.com/adafruit/circuitpython/issues/7693)
> 3. Learn more about Circuit Python and Micro Python
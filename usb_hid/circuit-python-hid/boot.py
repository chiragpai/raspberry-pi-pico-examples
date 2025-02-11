import usb_hid
import usb_cdc
import board
import digitalio
import storage

# Registers the connected as a Consumer Control HID device
usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     usb_hid.Device.CONSUMER_CONTROL)
)

# Enables the USB storage and CDC
def enable_storage_cdc():
    storage.enable_usb_drive()
    usb_cdc.enable(console=True, data=True)

# Disables the USB storage and CDC    
def disable_storage_cdc():
    storage.disable_usb_drive()
    usb_cdc.disable()

# GPIO #15. Pin #20    
btn = digitalio.DigitalInOut(board.GP15)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

# USB storage and CDC should be enabled or disabled during boot. Cannot be changed later.
# By default USB Storage and CDC is enabled if this code is executed.
if not btn.value:
    # GP15 is connected to GND, enable storage
    enable_storage_cdc()
else:
    disable_storage_cdc()

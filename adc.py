import smbus, threading, csv

# Initialize global variables to be kept track of
# Initialize smbus, for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)
# Check PCF8591 address by typing in 'sudo i2cdetect -y -1' in terminal.
address = 0x48


def read(chn):
    """Returns sensor value of specific channel"""
    try:
        if chn == 0:
            bus.write_byte(address, 0x40)
        if chn == 1:
            bus.write_byte(address, 0x41)
        if chn == 2:
            bus.write_byte(address, 0x42)
        if chn == 3:
            bus.write_byte(address, 0x43)
        bus.read_byte(address)  # dummy read to start conversion
    except (Exception):
        print("Address: %s" % address)
    return bus.read_byte(address)


def write(val):
    """Writes set numerical representation of voltage out to adc out pin"""
    try:
        temp = val  # move string value to temp
        # print temp to see on terminal else comment out
        bus.write_byte_data(address, 0x40, int(temp))
    except:
        print("Error: Device address: 0x%2X" % address)


# Clears the ADC
def destroy():
    """Clears analog output of adc"""
    write(0)

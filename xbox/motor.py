import smbus
bus = smbus.SMBus(1)

def writeNumber(value):
    try:
        if value > 20:
            bus.write_byte(0x04, value)
        else:
            bus.write_byte(0x04, 0)
    except:
        return False
    finally:
        return True


def writeBlock(block):
    try:
        bus.write_i2c_block_data(0x04, 0, block)
    except:
        return False
    finally:
        return True


def readNumber():
    number = None
    try:
        number = bus.read_byte(0x04)
    except:
        return -1
    finally:
        return number

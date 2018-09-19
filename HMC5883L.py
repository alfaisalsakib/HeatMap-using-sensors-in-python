import smbus

# Device Address and I2C Bus Port
Bus = smbus.SMBus(1)  # Specify the I2C port to use
Device_Address = 0x1E # Use "sudo i2cdetect -y 1" to get the address of this device on the I2C bus

# Assign names to the necessary HMC5883L Registers
CONFIG_A   = 0x00
CONFIG_B   = 0x01
MODE       = 0x02
MAG_XOUT_H = 0x03
MAG_YOUT_H = 0x07
MAG_ZOUT_H = 0x05

# Initialize the HMC5883L Sensor
def HMC5883L_Initialize():
    print("Initializing the Handheld Magnetometer. . .", end="")
    Bus.write_byte_data(Device_Address, CONFIG_A, 24)
    Bus.write_byte_data(Device_Address, CONFIG_B, 224)
    Bus.write_byte_data(Device_Address, MODE, 0)

    print(" Success!")
    return

# Return the value from the register at the specified address
def Read_Register_Data(address):
    # The onboard DSP outputs 16-bit values for the magnetometer which are stored in two 8-bit registers
    # Register names ending in "H" hold the Higher 8 bits
    # Register names ending in "L" hold the Lower 8 bits
    higher_order_bits = Bus.read_byte_data(Device_Address, address)
    lower_order_bits = Bus.read_byte_data(Device_Address, (address+1))
    
    # Concatenate the higher order bits with the lower order bits
    higher_order_bits = higher_order_bits << 8    # Shift Left Logical by 8 bits
    readout = higher_order_bits | lower_order_bits # Perform logical OR operation
    
    # Convert to a signed value
    if (readout > 32768):
        readout = readout - 65536
        
    return readout

# Returns the uncalibrated raw magnetometer data readouts
def Read_Raw_Magnetometer_Data():
    return Read_Register_Data(MAG_XOUT_H), Read_Register_Data(MAG_YOUT_H), Read_Register_Data(MAG_ZOUT_H)

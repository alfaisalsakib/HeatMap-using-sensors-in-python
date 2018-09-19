import smbus

# Device Address and I2C Bus Port
Bus = smbus.SMBus(1)  # Specify the I2C port to use
Device_Address = 0x0D # Use "sudo i2cdetect -y 1" to get the address of this device on the I2C bus

# Assign names to the necessary QMC5883L Registers
DATA_OUTPUT_X_MSB_REGISTER = 0x01 # This register stores the most recent magnetometer measurement from channel x
DATA_OUTPUT_Y_MSB_REGISTER = 0x03 # This register stores the most recent magnetometer measurement from channel y
DATA_OUTPUT_Z_MSB_REGISTER = 0x05 # This register stores the most recent magnetometer measurement from channel z
CONTROL_REGISTER_1         = 0x09 # This register controls the Operational Modes (MODE), Output Data update Rate (ODR), Magnetic field measurement range or sensitivity of the sensors (RNG) and Over Sampling Rate (OSR)
CONTROL_REGISTER_2         = 0x0A # This register controls the Interrupt Pin Enable (INT_ENB), Point Roll Over function Enable (POL_PNT) and Soft Reset (SOFT_RST)
SET_RESET_PERIOD_REGISTER  = 0x0B # This register controls the Set/Reset period of the device

# Initialize the QMC5883L Sensor
def QMC5883L_Initialize():
    # OSR  : 512
    # RNG  : 8G
    # ODR  : 200Hz
    # MODE : Continuous
    Bus.write_byte_data(Device_Address, CONTROL_REGISTER_1, 29)

    # SOFT_RST : Normal
    # ROL_PNT  : Normal
    # INT_ENB  : Normal
    Bus.write_byte_data(Device_Address, CONTROL_REGISTER_2, 0)

    # It is recommended by the manufacturer that this register is written by 0x01
    Bus.write_byte_data(Device_Address, SET_RESET_PERIOD_REGISTER, 1)
    
    return

# Return the value from the register at the specified address
def Read_Register_Data(address):
    # The onboard DSP outputs 16-bit values from the magnetometer which are stored in two 8-bit registers
    higher_order_bits = Bus.read_byte_data(Device_Address, address)
    lower_order_bits = Bus.read_byte_data(Device_Address, (address-1))
    
    # Concatenate the higher order bits with the lower order bits
    higher_order_bits = higher_order_bits << 8    # Shift Left Logical by 8 bits
    readout = higher_order_bits | lower_order_bits # Perform logical OR operation
    
    # Convert to a signed value
    if (readout > 32768):
        readout = readout - 65536
        
    return readout

# Returns the uncalibrated raw magnetometer data readouts
def Read_Raw_Magnetometer_Data():
    return Read_Register_Data(DATA_OUTPUT_X_MSB_REGISTER), Read_Register_Data(DATA_OUTPUT_Y_MSB_REGISTER), Read_Register_Data(DATA_OUTPUT_Z_MSB_REGISTER)

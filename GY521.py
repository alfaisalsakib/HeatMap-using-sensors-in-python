import Calibration
import Parameters
import State
import smbus

# Device Address and I2C Bus Port
Bus = smbus.SMBus(1)  # Specify the I2C port to use
Device_Address = 0x68 # Use "sudo i2cdetect -y 1" to get the address of this device on the I2C bus

# Assign names to the necessary MPU-6050 Registers
SMPLRT_DIV   = 0x19 # Sample Rate Divider. This register specifies the divider from the gyroscope output rate used to generate the Sample Rate for the MPU-6050
CONFIG       = 0x1A # Configuration. This register configures the external Frame Synchronization (FSYNC) pin sampling and Digital Low Pass Filter (DLPF) setting for both the gyroscopes and accelerometers
GYRO_CONFIG  = 0x1B # Gyroscope Configuration. This register is used to trigger gyroscope self-test and configure the gyroscopes' full scale range
ACCEL_CONFIG = 0x1C # Accelerometer Configuration. This register is used to trigger accelerometer self-test and configure the accelerometers' full scale range. This register also configures the Digital High Pass Filter (DHPF)
INT_ENABLE   = 0x38 # Interrupt Enable. This register enables interrupt generation by interrupt sources
ACCEL_XOUT_H = 0x3B # Accelerometer X-axis Output, higher order bits. This register stores the most recent accelerometer measurement along the x-axis
ACCEL_YOUT_H = 0x3D # Accelerometer Y-axis Output, higher order bits. This register stores the most recent accelerometer measurement along the y-axis
ACCEL_ZOUT_H = 0x3F # Accelerometer Z-axis Output, higher order bits. This register stores the most recent accelerometer measurement along the z-axis
GYRO_XOUT_H  = 0x43 # Gyroscope X-axis Output, higher order bits. This register stores the most recent gyroscope measurement along the x-axis
GYRO_YOUT_H  = 0x45 # Gyroscope Y-axis Output, higher order bits. This register stores the most recent gyroscope measurement along the y-axis
GYRO_ZOUT_H  = 0x47 # Gyroscope Z-axis Output, higher order bits. This register stores the most recent gyroscope measurement along the z-axis
PWR_MGMT_1   = 0x6B # Power Management 1. This register allows the user to configure the power mode and clock source. It also provides a bit for resetting the entire device and a bit for disabling the temperature sensor

# Initialize the MPU-6050 Sensor
def MPU6050_Initialize():
    print("Initializing the Handheld Accelerometer-Gyroscope. . .", end="")
    # Set the internal 8MHz oscillator as the functional internal clock for the device
    Bus.write_byte_data(Device_Address, PWR_MGMT_1, 0)
    
    # Gyroscope Output Rate = 8kHz
    # Accelerometer Output Rate = 1kHz
    #
    # Formula:
    #          Sample Rate = Gyroscope Output Rate / (1 + SMPLRT_DIV)
    #
    # Set the Sample Rate to 1kHz because the accelerometer operates at 1kHz
    Bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    # This is a stand-alone device so FSYNC needs to be disabled while the DLPF is configured to have a 5Hz bandwidth
    Bus.write_byte_data(Device_Address, CONFIG, 6)
    
    # Skip the self-test routine for all three gyroscope axes
    # Set the Gyroscopes' Full Scale Range to +/- 2000 degree/second
    # It may be possible to tweak the precision of the gyroscopes by changing their Full Scale Range value. Refer to the Register Map/Description for more information
    Bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    # Skip the self-test routine for all three accelerometer axes
    # Set the Accelerometers' Full Scale Range to +/- 8g
    # It may be possible to tweak the precision of the accelerometers by changing their Full Scale Range value. Refer to the Register Map/Description for more information
    Bus.write_byte_data(Device_Address, ACCEL_CONFIG, 16)
    
    # Enable interrupt generation
    Bus.write_byte_data(Device_Address, INT_ENABLE, 1)

    print(" Success!")
    return

# Return the value from the register at the specified address
def Read_Register_Data(address):
    # The onboard DSP outputs 16-bit values for the accelerometer and gyroscope which are stored in two 8-bit registers
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

# Returns the uncalibrated raw accelerometer data readouts
def Read_Raw_Accelerometer_Data():
    return Read_Register_Data(ACCEL_XOUT_H)*Parameters.ACCELEROMETER_X_GAIN, Read_Register_Data(ACCEL_YOUT_H)*Parameters.ACCELEROMETER_Y_GAIN, Read_Register_Data(ACCEL_ZOUT_H)*Parameters.ACCELEROMETER_Z_GAIN

# Returns the uncalibrated and processed accelerometer data readouts
def Read_Processed_Accelerometer_Data():
    gain=1.0
    multiplier = gain*8*9.80665/32768.0
    Ax, Ay, Az = Read_Raw_Accelerometer_Data()
    
    Ax *= multiplier
    Ay *= multiplier
    Az *= multiplier
    
    return Ax, Ay, Az

# Shell function
def Probe_Accelerometer():
    return Read_Processed_Accelerometer_Data()

# Returns the uncalibrated raw gyroscope data readouts
def Read_Raw_Gyroscope_Data():
    return Read_Register_Data(GYRO_XOUT_H), Read_Register_Data(GYRO_YOUT_H), Read_Register_Data(GYRO_ZOUT_H)

# Returns the calibrated raw gyroscope data readouts
def Read_Calibrated_Gyroscope_Data():
    # Check if the gyroscope has been calibrated or not
    sentinel = (State.RAW_BIAS_GYROSCOPE_X==0) & (State.RAW_BIAS_GYROSCOPE_Y==0) & (State.RAW_BIAS_GYROSCOPE_Z==0)
    if sentinel:
        Calibration.Calibrate_Raw_Gyroscope_Data() # Calibrate the gyroscope if it's not already calibrated
    
    Gx, Gy, Gz = Read_Raw_Gyroscope_Data() # Read the raw data
    
    # Adjust the raw data to compensate for bias
    Gx -= State.RAW_BIAS_GYROSCOPE_X
    Gy -= State.RAW_BIAS_GYROSCOPE_Y
    Gz -= State.RAW_BIAS_GYROSCOPE_Z
    
    return Gx, Gy, Gz

# Returns the calibrated and processed gyroscope data readouts
def Read_Processed_Gyroscope_Data():
    gain = 2.80 # Found experimentally
    multiplier = gain*1000/32768.0
    Gx, Gy, Gz = Read_Calibrated_Gyroscope_Data()
    
    Gx *= multiplier
    Gy *= multiplier
    Gz *= multiplier
    
    return Gx, Gy, Gz

# Shell function
def Probe_Gyroscope():
    return Read_Processed_Gyroscope_Data()

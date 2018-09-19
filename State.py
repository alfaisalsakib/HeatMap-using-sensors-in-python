HUMIDITY = 0 # Stores the current humidity as measured by the sensor
TEMPERATURE = 0 # Stores the current temperature as measured by the sensor

# Stores the mean angular velocity value for each of the gyroscope axes that is obtained from the Calibrate_Raw_Gyroscope_Data() function
# These serve as the raw bias values for the gyroscope
RAW_BIAS_GYROSCOPE_X = 0
RAW_BIAS_GYROSCOPE_Y = 0
RAW_BIAS_GYROSCOPE_Z = 0

# Stores the current orientation of the accelerometer
ORIENTATION_ACCELEROMETER_X = 0
ORIENTATION_ACCELEROMETER_Y = 0

# Stores the current orientation of the magnetometer
ORIENTATION_MAGNETOMETER_Z = 0

# Stores the current orientation of the gyroscope
DELTA_ORIENTATION_GYROSCOPE_X = 0
DELTA_ORIENTATION_GYROSCOPE_Y = 0
DELTA_ORIENTATION_GYROSCOPE_Z = 0

REFERENCE_ORIENTATION_Z = 0 # Stores the initial Z-Orientation of the sensor array for use as the orientation of the reference frame

# Stores the current orientation of the sensor array, corrected for noise and drift
ORIENTATION_X = 0
ORIENTATION_Y = 0
ORIENTATION_Z = 0

DISCRETE_ORIENTATION_Z = 0 # Stores the current discretized Z-Orientation of the sensor array

GRAVITIONAL_ACCELERATION = 0
ACCELERATION_MAGNITUDE = 0 # Stores the current acceleration value, adjusted for gravitional acceleration, for the sensor array

VELOCITY_MAGNITUDE = 0

GRAVITIONAL_ACCELERATION_2 = 0
FOOTSTEP_COUNT = 0
TIME_STAMP = 0

X_POSITION = 0
Y_POSITION = 0

ERROR_FLAG_1 = False
ERROR_FLAG_2 = False
ERROR_FLAG_3 = False